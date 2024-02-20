from loguru import logger
from utils.gas_checker import check_gas
from utils.helpers import retry, sleep
from .account import Account
from typing import Dict


class Blockframe(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info=wallet_info, chain="zksync")

    @retry
    @check_gas
    async def mint(self, contracts: Dict[str, float], sleep_from, sleep_to):
        logger.info(f"[{self.account_id}][{self.address}] Mint {len(contracts)} nfts on Blockframe")

        for contract_address, value in contracts.items():
            contract = self.w3.to_checksum_address(contract_address)
            tx_data = await self.get_tx_data(self.w3.to_wei(value, "ether"))

            data = "0x1ff7712f000000000000000000000000000000000000000000000000000000000000000" \
                   "1000000000000000000000000000000000000000000000000000000000000006000000000" \
                   "0000000000000000000000000000000000000000000000000000000100000000000000000" \
                   "00000000000000000000000000000000000000000000000"

            tx_data.update({"data": data, "to": contract})

            signed_txn = await self.sign(tx_data)
            txn_hash = await self.send_raw_transaction(signed_txn)
            await self.wait_until_tx_finished(txn_hash.hex())

            await sleep(sleep_from, sleep_to)
