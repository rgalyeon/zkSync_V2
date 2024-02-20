import asyncio
import random

from eth_typing import ChecksumAddress
from loguru import logger
from web3 import AsyncWeb3, AsyncHTTPProvider
from web3.middleware import async_geth_poa_middleware
from tabulate import tabulate
from utils.password_handler import get_wallet_data

from config import RPC


async def get_nonce(address: str):
    w3 = AsyncWeb3(
        AsyncHTTPProvider(random.choice(RPC["zksync"]["rpc"])),
        middlewares=[async_geth_poa_middleware],
    )

    address = w3.to_checksum_address(address)

    nonce = await w3.eth.get_transaction_count(address)

    return nonce


async def check_tx():
    tasks = []

    logger.info("Start transaction checker")

    accounts = [(address, data['id']) for address, data in get_wallet_data().items()]
    for address, name in accounts:
        tasks.append(asyncio.create_task(get_nonce(address), name=name))

    await asyncio.gather(*tasks)

    table = [[k, i.get_name(), i.result()] for k, i in enumerate(tasks, start=1)]

    headers = ["#", "Address", "Nonce"]

    print(tabulate(table, headers, tablefmt="github"))
