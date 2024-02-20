import random

from config import (
    SYNCSWAP_CONTRACTS,
    MUTE_CONTRACTS,
    SPACEFI_CONTRACTS,
    PANCAKE_CONTRACTS,
    WOOFI_CONTRACTS,
    ZKSYNC_TOKENS
)
from utils.gas_checker import check_gas
from utils.helpers import retry
from utils.sleeping import sleep
from .account import Account


class MultiApprove(Account):
    def __init__(self, wallet_info) -> None:
        super().__init__(wallet_info, chain="zksync")

    @retry
    @check_gas
    async def start(self, amount: int, sleep_from: int, sleep_to: int):
        contract_list = [
            SYNCSWAP_CONTRACTS["router"],
            MUTE_CONTRACTS["router"],
            SPACEFI_CONTRACTS["router"],
            PANCAKE_CONTRACTS["router"],
            WOOFI_CONTRACTS["router"],
        ]
        token_list = list(ZKSYNC_TOKENS)

        random.shuffle(contract_list)
        random.shuffle(token_list)

        for contract_address in contract_list:
            for _, token in enumerate(token_list):
                if token in ["ETH", "WETH"]:
                    continue

                await self.approve(amount, ZKSYNC_TOKENS[token], contract_address)

                await sleep(sleep_from, sleep_to)
