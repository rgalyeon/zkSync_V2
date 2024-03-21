from loguru import logger
from config import BASILISK_CONTRACTS, BASILISK_ABI
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class Basilisk(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info, chain="zksync")

        self.contract = self.get_contract(BASILISK_CONTRACTS["landing"], BASILISK_ABI)

    async def router(self, min_amount,
                     max_amount,
                     decimal,
                     sleep_from,
                     sleep_to,
                     make_withdraw,
                     all_amount,
                     min_percent,
                     max_percent):

        amount_wei, amount, balance = await self.get_amount(
            "ETH",
            min_amount,
            max_amount,
            decimal,
            all_amount,
            min_percent,
            max_percent
        )

        await self.deposit(amount_wei, amount, balance)
        if make_withdraw:
            await sleep(sleep_from, sleep_to)
            await self.withdraw()

    async def get_deposit_amount(self):
        amount = await self.contract.functions.balanceOfUnderlying(self.address).call()
        return amount

    @retry
    @check_gas
    async def deposit(self, amount_wei, amount, balance):

        logger.info(f"[{self.account_id}][{self.address}] Make deposit on Basilisk | {amount} ETH")

        tx_data = await self.get_tx_data(amount_wei)

        transaction = await self.contract.functions.mint().build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def withdraw(self):
        amount = await self.get_deposit_amount()

        if amount > 0:
            logger.info(
                f"[{self.account_id}][{self.address}] Make withdraw from Basilisk | " +
                f"{self.w3.from_wei(amount, 'ether')} ETH"
            )

            tx_data = await self.get_tx_data()

            transaction = await self.contract.functions.redeemUnderlying(amount).build_transaction(tx_data)

            signed_txn = await self.sign(transaction)

            txn_hash = await self.send_raw_transaction(signed_txn)

            await self.wait_until_tx_finished(txn_hash.hex())
        else:
            logger.error(f"[{self.account_id}][{self.address}] Deposit not found")

    @retry
    @check_gas
    async def enable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Enable collateral on Basilisk")

        contract = self.get_contract(BASILISK_CONTRACTS["collateral"], BASILISK_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.enterMarkets(
            [self.w3.to_checksum_address(BASILISK_CONTRACTS["landing"])]
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())

    @retry
    @check_gas
    async def disable_collateral(self):
        logger.info(f"[{self.account_id}][{self.address}] Disable collateral on Basilisk")

        contract = self.get_contract(BASILISK_CONTRACTS["collateral"], BASILISK_ABI)

        tx_data = await self.get_tx_data()

        transaction = await contract.functions.exitMarket(
            self.w3.to_checksum_address(BASILISK_CONTRACTS["landing"])
        ).build_transaction(tx_data)

        signed_txn = await self.sign(transaction)

        txn_hash = await self.send_raw_transaction(signed_txn)

        await self.wait_until_tx_finished(txn_hash.hex())
