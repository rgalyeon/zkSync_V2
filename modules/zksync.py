import random
from typing import List
from loguru import logger
from config import ZKSYNC_DEPOSIT_ABI, ZKSYNC_WITHDRAW_ABI, ZKSYNC_BRIDGE_CONTRACT, ZKSYNC_TOKENS, WETH_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from .transfer import Transfer


class ZkSync(Transfer):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info)

    @retry
    @check_gas
    async def deposit(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int,
            save_funds: List[float],
            check_balance_on_dest: bool,
            check_amount: float,
            min_required_amount: float
    ):
        self.bridge_logic = self.deposit_logic

        await self.transfer_eth(from_chains=['ethereum'],
                                min_amount=min_amount, max_amount=max_amount,
                                decimal=decimal, all_amount=all_amount,
                                min_percent=min_percent, max_percent=max_percent,
                                save_funds=save_funds, check_balance_on_dest=check_balance_on_dest,
                                check_amount=check_amount,
                                min_required_amount=min_required_amount, destination_chain='zksync')

    async def deposit_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(f"[{self.account_id}][{self.address}] Bridge to ZkSync | {amount} ETH")

        gas_limit = random.randint(700000, 1000000)

        contract = self.get_contract(ZKSYNC_BRIDGE_CONTRACT, ZKSYNC_DEPOSIT_ABI)
        base_cost = await contract.functions.l2TransactionBaseCost(await self.w3.eth.gas_price, gas_limit, 800).call()

        tx_data = await self.get_tx_data(amount_wei + base_cost)

        transaction = await contract.functions.requestL2Transaction(
            self.address,
            self.w3.to_wei(amount, "ether"),
            "0x",
            gas_limit,
            800,
            [],
            self.address
        ).build_transaction(
            tx_data
        )

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def withdraw(
            self,
            min_amount: float, max_amount: float, decimal: int,
            all_amount: bool, min_percent: int, max_percent: int,
            save_funds: List[float], check_balance_on_dest: bool, check_amount: float,
            min_required_amount: float
    ):
        self.bridge_logic = self.withdraw_logic

        await self.transfer_eth(from_chains=['zksync'],
                                min_amount=min_amount, max_amount=max_amount,
                                decimal=decimal, all_amount=all_amount,
                                min_percent=min_percent, max_percent=max_percent,
                                save_funds=save_funds, check_balance_on_dest=check_balance_on_dest,
                                check_amount=check_amount,
                                min_required_amount=min_required_amount, destination_chain='ethereum')

    async def withdraw_logic(self, source_chain, destination_chain, amount_wei, amount, balance):
        logger.info(f"[{self.account_id}][{self.address}] Bridge {amount} ETH to Ethereum")

        if amount_wei < balance:
            contract = self.get_contract("0x000000000000000000000000000000000000800A", ZKSYNC_WITHDRAW_ABI)

            tx_data = await self.get_tx_data(amount_wei)

            contract_txn = await contract.functions.withdraw(
                self.address,
            ).build_transaction(tx_data)

            signed_txn = await self.sign(contract_txn)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"Withdraw transaction to L1 network failed | error: insufficient funds!")

    @retry
    @check_gas
    async def wrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(ZKSYNC_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Wrap {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await weth_contract.functions.deposit().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def unwrap_eth(
            self,
            min_amount: float,
            max_amount: float,
            decimal: int,
            all_amount: bool,
            min_percent: int,
            max_percent: int
    ):
        amount_wei, amount, balance = await self.get_amount(
            "WETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        weth_contract = self.get_contract(ZKSYNC_TOKENS["WETH"], WETH_ABI)

        logger.info(f"[{self.account_id}][{self.address}] Unwrap {amount} ETH")

        tx_data = await self.get_tx_data()

        transaction = await weth_contract.functions.withdraw(amount_wei).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
