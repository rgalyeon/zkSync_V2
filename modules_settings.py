import asyncio
from modules import *


async def deposit_zksync(wallet_info):
    """
    Deposit from official bridge
    ______________________________________________________
    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 1
    max_percent = 1

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0

    zksync_inst = ZkSync(wallet_info)
    await zksync_inst.deposit(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
        save_funds, check_balance_on_dest, check_amount, min_required_amount
    )


async def withdraw_zksync(wallet_info):
    """
    Withdraw from official bridge
    ______________________________________________________
    Description: look at deposit_zksync
    """

    min_amount = 0.01
    max_amount = 0.015
    decimal = 4

    all_amount = False

    min_percent = 10
    max_percent = 10

    check_balance_on_dest = False
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0

    zksync_inst = ZkSync(wallet_info)
    await zksync_inst.withdraw(
        min_amount, max_amount, decimal, all_amount, min_percent, max_percent,
        save_funds, check_balance_on_dest, check_amount, min_required_amount
    )


async def withdraw_okx(wallet_info):
    """
    Withdraw ETH from OKX

    ______________________________________________________
    min_amount - min amount (ETH)
    max_amount - max_amount (ETH)
    chains - ['zksync', 'arbitrum', 'linea', 'base', 'optimism']
    terminate - if True - terminate program if money is not withdrawn
    skip_enabled - If True, the skip_threshold check will be applied; otherwise, it will be ignored
    skip_threshold - If skip_enabled is True and the wallet balance is greater than or equal to this threshold,
                     skip the withdrawal
    """
    token = 'ETH'
    chains = ['arbitrum', 'zksync', 'linea', 'base', 'optimism']

    min_amount = 0.0070
    max_amount = 0.0072

    terminate = False

    skip_enabled = False
    skip_threshold = 0.00327

    wait_unlimited_time = False
    sleep_between_attempts = [10, 20]  # min, max

    okx_exchange = Okx(wallet_info, chains)
    await okx_exchange.okx_withdraw(
        min_amount, max_amount, token, terminate, skip_enabled, skip_threshold,
        wait_unlimited_time, sleep_between_attempts
    )


async def transfer_to_okx(wallet_info):
    from_chains = ["optimism"]

    min_amount = 0.0012
    max_amount = 0.0012
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    save_funds = [0.0001, 0.00012]
    min_required_amount = 0.002

    bridge_from_all_chains = False
    sleep_between_transfers = [1, 1]

    transfer_inst = Transfer(wallet_info)
    await transfer_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent,
        max_percent, save_funds, False, 0, min_required_amount,
        bridge_from_all_chains=bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers
    )


async def bridge_orbiter(wallet_info):
    """
    Bridge from orbiter
    ______________________________________________________
    from_chains – source chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one or more
                  If more than one chain is specified, the software will check the balance in each network and
                  select the chain with the highest balance.
    to_chain – destination chain - ethereum, polygon_zkevm, arbitrum, optimism, zksync | Select one

    min_amount - the minimum possible amount for sending
    max_amount - maximum possible amount to send
    decimal - to which digit to round the amount to be sent

    all_amount - if True, percentage values will be used for sending (min_percent, max_percent
                 instead of min_amount, max_amount).

    min_percent - the minimum possible percentage of the balance to be sent
    max_percent - the maximum possible percentage of the balance to send

    check_balance_on_dest - if True, it will check the balance in the destination network.
    check_amount - amount to check the balance in the destination network. if the balance is greater than this amount,
                   the bridge will not be executed.
    save_funds - what amount to leave in the outgoing network [min, max], chosen randomly from the range
    min_required_amount - the minimum required balance in the network to make the bridge.
                          if there is no network with the required balance, the bridge will not be made
    bridge_from_all_chains - if True, will be produced from all chains specified in the parameter from_chains
    sleep_between_transfers - only if bridge_from_all_chains=True. sleep between few transfers
    """

    from_chains = ["arbitrum", "optimism", "base", "linea"]
    to_chain = "zksync"

    min_amount = 0.005
    max_amount = 0.0051
    decimal = 6

    all_amount = True

    min_percent = 98
    max_percent = 100

    check_balance_on_dest = True
    check_amount = 0.005
    save_funds = [0.0011, 0.0013]
    min_required_amount = 0.005

    bridge_from_all_chains = False
    sleep_between_transfers = [120, 300]

    orbiter_inst = Orbiter(wallet_info)
    await orbiter_inst.transfer_eth(
        from_chains, min_amount, max_amount, decimal, all_amount, min_percent, max_percent, save_funds,
        check_balance_on_dest, check_amount, min_required_amount, to_chain, bridge_from_all_chains,
        sleep_between_transfers=sleep_between_transfers
    )


async def wrap_eth(wallet_info):
    """
    Wrap ETH
    ______________________________________________________
    all_amount - wrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 5
    max_percent = 5

    zksync_inst = ZkSync(wallet_info)
    await zksync_inst.wrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def unwrap_eth(wallet_info):
    """
    Unwrap ETH
    ______________________________________________________
    all_amount - unwrap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4

    all_amount = True

    min_percent = 100
    max_percent = 100

    zksync_inst = ZkSync(wallet_info)
    await zksync_inst.unwrap_eth(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_syncswap(wallet_info):
    """
    Make swap on SyncSwap

    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer – Don't use stable coin in from and to token | from_token USDC to_token USDT DON'T WORK!!!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 1
    max_amount = 2
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    syncswap_inst = SyncSwap(wallet_info)
    await syncswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def liquidity_syncswap(wallet_info):
    """
    Add liqudity on SyncSwap

    amount in ETH, USDC amount not need (auto swap)
    """
    min_amount = 0.01
    max_amount = 0.02
    decimal = 6

    all_amount = True

    min_percent = 50
    max_percent = 50

    syncswap_inst = SyncSwap(wallet_info)
    await syncswap_inst.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_mute(wallet_info):
    """
    Make swap on Mute
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    mute_inst = Mute(wallet_info)
    await mute_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                         max_percent)


async def swap_spacefi(wallet_info):
    """
    Make swap on SpaceFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, USDC, USDT, BUSD, OT, MATIC, WBTC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    spacefi_inst = SpaceFi(wallet_info)
    await spacefi_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                            max_percent)


async def liquidity_spacefi(wallet_info):
    """
    Add liqudity on SpaceFi
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6

    all_amount = True

    min_percent = 1
    max_percent = 1

    spacefi_inst = SpaceFi(wallet_info)
    await spacefi_inst.add_liquidity(min_amount, max_amount, decimal, all_amount, min_percent, max_percent)


async def swap_pancake(wallet_info):
    """
    Make swap on PancakeSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    pancake_inst = Pancake(wallet_info)
    await pancake_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                            max_percent)


async def swap_woofi(wallet_info):
    """
    Make swap on WooFi
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 60
    max_percent = 80

    woofi_inst = WooFi(wallet_info)
    await woofi_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_odos(wallet_info):
    """
    Make swap on Odos
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, MAV, OT, MATIC, WBTC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    odos_inst = Odos(wallet_info)
    await odos_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_zkswap(wallet_info):
    """
    Make swap on ZkSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    zkswap_inst = ZKSwap(wallet_info)
    await zkswap_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_xyswap(wallet_info):
    """
    Make swap on XYSwap
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, OT | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, OT | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    xyswap_inst = XYSwap(wallet_info)
    await xyswap_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                           max_percent)


async def swap_openocean(wallet_info):
    """
    Make swap on OpenOcean
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD, MAV, OT, WBTC | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD, MAV, OT, WBTC | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "WETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    openocean_inst = OpenOcean(wallet_info)
    await openocean_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def swap_inch(wallet_info):
    """
    Make swap on 1inch
    ______________________________________________________
    from_token – Choose SOURCE token ETH, WETH, USDC, USDT, BUSD | Select one
    to_token – Choose DESTINATION token ETH, WETH, USDC, USDT, BUSD | Select one

    Disclaimer - If you use True for use_fee, you support me 1% of the transaction amount
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 1
    max_percent = 1

    inch_dex = Inch(wallet_info)
    await inch_dex.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                        max_percent)


async def swap_maverick(wallet_info):
    """
    Make swap on Maverick
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "USDC"
    to_token = "ETH"

    min_amount = 0.001
    max_amount = 0.002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 100
    max_percent = 100

    maverick_inst = Maverick(wallet_info)
    await maverick_inst.swap(from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent,
                             max_percent)


async def swap_vesync(wallet_info):
    """
    Make swap on VeSync
    ______________________________________________________
    from_token – Choose SOURCE token ETH, USDC | Select one
    to_token – Choose DESTINATION token ETH, USDC | Select one

    Disclaimer - You can swap only ETH to any token or any token to ETH!
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    from_token = "ETH"
    to_token = "USDC"

    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 6
    slippage = 1

    all_amount = True

    min_percent = 10
    max_percent = 10

    vesync_inst = VeSync(wallet_info)
    await vesync_inst.swap(
        from_token, to_token, min_amount, max_amount, decimal, slippage, all_amount, min_percent, max_percent
    )


async def bungee_refuel(wallet_info):
    """
    Make refuel on Bungee
    ______________________________________________________
    to_chain – Choose DESTINATION chain: BSC, OPTIMISM, GNOSIS, POLYGON, BASE, ARBITRUM, AVALANCHE, AURORA, ZK_EVM

    Disclaimer - The chain will be randomly selected
    ______________________________________________________
    random_amount – True - amount random from min to max | False - use min amount
    """

    chain_list = ["GNOSIS"]

    random_amount = False

    bungee_inst = Bungee(wallet_info)
    await bungee_inst.refuel(chain_list, random_amount)


async def stargate_bridge(wallet_info):
    """
    Make stargate MAV token bridge to BSC
    ______________________________________________________
    all_amount - swap from min_percent to max_percent
    """

    min_amount = 0.001
    max_amount = 0.002
    decimal = 4
    slippage = 1

    sleep_from = 5
    sleep_to = 24

    all_amount = True

    min_percent = 10
    max_percent = 20

    stargate_inst = Stargate(wallet_info)
    await stargate_inst.bridge(
        min_amount, max_amount, decimal, slippage, sleep_from, sleep_to, all_amount, min_percent, max_percent
    )


async def deposit_eralend(wallet_info):
    """
    Make deposit on Eralend
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    eralend_inst = Eralend(wallet_info)
    await eralend_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_basilisk(wallet_info):
    """
    Make deposit on Basilisk
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = False

    min_percent = 60
    max_percent = 80

    basilisk_inst = Basilisk(wallet_info)
    await basilisk_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_reactorfusion(wallet_info):
    """
    Make deposit on ReactorFusion
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = False

    min_percent = 60
    max_percent = 80

    reactorfusion_inst = ReactorFusion(wallet_info)
    await reactorfusion_inst.router(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def deposit_zerolend(wallet_info):
    """
    Make deposit on ZeroLend
    ______________________________________________________
    make_withdraw - True, if need withdraw after deposit

    all_amount - deposit from min_percent to max_percent
    """
    min_amount = 0.0001
    max_amount = 0.0002
    decimal = 5

    sleep_from = 5
    sleep_to = 24

    make_withdraw = True

    all_amount = True

    min_percent = 5
    max_percent = 10

    zerolend_inst = ZeroLend(wallet_info)
    await zerolend_inst.deposit(
        min_amount, max_amount, decimal, sleep_from, sleep_to, make_withdraw, all_amount, min_percent, max_percent
    )


async def bridge_nft(wallet_info):
    """
    Make mint NFT and bridge NFT on L2Telegraph
    """

    sleep_from = 5
    sleep_to = 20

    l2telegraph_inst = L2Telegraph(wallet_info)
    await l2telegraph_inst.bridge(sleep_from, sleep_to)


async def mint_tavaera(wallet_info):
    """
    Mint Tavaera ID and Tavaera NFT
    """

    sleep_from = 5
    sleep_to = 20

    tavaera_nft = Tavaera(wallet_info)
    await tavaera_nft.mint(sleep_from, sleep_to)


async def mint_zkstars(wallet_info):
    """
    Mint ZkStars NFT
    """

    contracts = [
        "0xe7Ed1c47E1e2eA6e9126961df5d41798722A7656",
        "0x53424440d0ead57e599529b42807a0ba1965dd66",
        "0x406b1195f4916b13513fea102777df5bd4af06eb",
        "0xf19b7027d37c3321194d6c5f34ea2e6cbc73fa25",
        "0xd834c621dea708a21b05eaf181115793eaa2f9d9",
        "0xafec8df7b10303c3514826c9e2222a16f1486bee",
        "0x56bf83e598ce80299962be937fe0ba54f5d5e2b2",
        "0x8595d989a96cdbdc1651e3c87ea3d945e0460097",
        "0x945b1edcd03e1d1ad9255c2b28e1c22f2c819f0e",
        "0xc92fc3f19645014c392825e3cfa3597412b0d913",
        "0x808d59a747bfedd9bcb11a63b7e5748d460b614d",
        "0x8dd8706cbc931c87694e452caa0a83a564753241",
        "0x8dd3c29f039e932ebd8eac873b8b7a56d17e36c6",
        "0xca0848cadb25e6fcd9c8ce15bcb8f8da6c1fc519",
        "0x06d52c7e52e9f28e3ad889ab2083fe8dba735d52",
        "0x86f39d51c06cac130ca59eabedc9233a49fcc22a",
        "0xee0d4a8f649d83f6ba5e5c9e6c4d4f6ae846846a",
        "0xfda7967c56ce80f74b06e14ab9c71c80cb78b466",
        "0x0d99efcde08269e2941a5e8a0a02d8e5722403fc",
        "0xf72cf790ac8d93ee823014484fc74f2f1e337bf6"
    ]

    mint_min = 1
    mint_max = 1

    mint_all = False

    sleep_from = 5
    sleep_to = 10

    zkkstars = ZkStars(wallet_info)
    await zkkstars.mint(contracts, mint_min, mint_max, mint_all, sleep_from, sleep_to)


async def swap_tokens(wallet_info):
    """
    SwapTokens module: Automatically swap tokens to ETH
    ______________________________________________________
    use_dex - Choose any dex:
    syncswap, mute, spacefi, pancake, woofi, maverick, odos, zkswap, xyswap, openocean, inch, vesync
    """

    use_dex = [
        "maverick", "mute", "pancake", "syncswap",
        "woofi", "spacefi", "odos", "zkswap",
        "xyswap", "openocean", "inch", "vesync"
    ]

    use_tokens = ["USDC"]

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    min_percent = 100
    max_percent = 100

    swap_tokens_inst = SwapTokens(wallet_info)
    await swap_tokens_inst.swap(use_dex, use_tokens, sleep_from, sleep_to, slippage, min_percent, max_percent)


async def swap_multiswap(wallet_info):
    """
    Multi-Swap module: Automatically performs the specified number of swaps in one of the dexes.
    ______________________________________________________
    use_dex - Choose any dex:
    syncswap, mute, spacefi, pancake, woofi, maverick, odos, zkswap, xyswap, openocean, inch, vesync

    quantity_swap - Quantity swaps
    ______________________________________________________
    random_swap_token - If True the swap path will be [ETH -> USDC -> USDC -> ETH] (random!)
    If False the swap path will be [ETH -> USDC -> ETH -> USDC]
    """

    use_dex = [
        "maverick", "mute", "pancake", "syncswap",
        "woofi", "spacefi", "odos", "zkswap",
        "xyswap", "openocean", "inch", "vesync"
    ]

    min_swap = 1
    max_swap = 1

    sleep_from = 300
    sleep_to = 600

    slippage = 1

    random_swap_token = True

    min_percent = 10
    max_percent = 10

    multi = Multiswap(wallet_info)
    await multi.swap(
        use_dex, sleep_from, sleep_to, min_swap, max_swap, slippage, random_swap_token, min_percent, max_percent
    )


async def mint_nft(wallet_info):
    """
    Mint NFT on NFTS2ME
    ______________________________________________________
    contracts - list NFT contract addresses
    """

    contracts = ["0x4b363957913012789874ab6796bdb7b29d4588d3"]

    minter_inst = Minter(wallet_info)
    await minter_inst.mint_nft(contracts)


async def owlto_check_in(wallet_info):
    """
    Owlto daily check in. Send tx and press button on site
    ______________________________________________________

    ref - wallet address of referral
    """

    ref = "0xE022adf1735642DBf8684C05f53Fe0D8339F5663"

    owlto_inst = Owlto(wallet_info)
    await owlto_inst.check_in(ref)


async def mint_blockframe(wallet_info):
    """
    Mint nft on blockframe
    _______________________________________________________
    contracts - {contract address: value (price)}
    sleep_from, sleep_to - min and max sleep between mints
    """

    contracts = {
        "0x3C553974ab5A7f01ab7E16299B1b1a55b8D95e01": 0.0001
    }

    sleep_from = 10
    sleep_to = 10

    blockframe_inst = Blockframe(wallet_info)
    await blockframe_inst.mint(contracts, sleep_from, sleep_to)


async def custom_routes(wallet_info):
    """
    BRIDGE:
        – deposit_zksync
        – withdraw_zksync
        – bridge_orbiter
        – bungee_refuel
        – stargate_bridge
    WRAP:
        – wrap_eth
        – unwrap_eth
    DEX:
        – swap_syncswap
        – swap_maverick
        – swap_mute
        – swap_spacefi
        – swap_pancake
        – swap_woofi
        – swap_odos
        – swap_zkswap
        – swap_xyswap
        – swap_inch
        – swap_openocean
        – swap_vesync
    LIQUIDITY:
        – liquidity_syncswap
        – liquidity_spacefi
    LANDING:
        – deposit_eralend, withdraw_erlaned, enable_collateral_eralend, disable_collateral_eralend
        – deposit_basilisk, withdraw_basilisk, enable_collateral_basilisk, disable_collateral_basilisk
        – deposit_reactorfusion, withdraw_reactorfusion,
        enable_collateral_reactorfusion, disable_collateral_reactorfusion
        – deposit_zerolend
        – withdraw_zerolend
    NFT/DOMAIN:
        – mint_zkstars
        – create_omnisea
        – bridge_nft
        – mint_tavaera
        – mint_nft
        – mint_mailzero_nft
        – mint_zks_domain
        – mint_era_domain
    ANOTHER:
        – send_message (l2Telegraph)
        – send_mail (Dmail)
        – swap_multiswap
        – swap_tokens
        – deploy_contract_zksync
        – create_safe
    ______________________________________________________
    Disclaimer - You can add modules to [] to select random ones,
    example [module_1, module_2, [module_3, module_4], module 5]
    The script will start with module 1, 2, 5 and select a random one from module 3 and 4

    You can also specify None in [], and if None is selected by random, this module will be skipped

    You can also specify () to perform the desired action a certain number of times
    example (send_mail, 1, 10) run this module 1 to 10 times
    """

    use_modules = [automatic_routes]

    sleep_from = 30000
    sleep_to = 60000

    random_module = True

    routes_ = Routes(wallet_info)
    await routes_.start(use_modules, sleep_from, sleep_to, random_module)


async def automatic_routes(wallet_info):
    """
    The module automatically generates the paths a wallet will take,
    changing the probabilities of selecting one or another module for each wallet
    ______________________________________________________
    transaction_count - number of transactions (not necessarily all transactions are executed, modules can be skipped)
    cheap_ratio - from 0 to 1, the share of cheap transactions when building a route
    cheap_modules - list of modules to be used as cheap ones
    expensive_modules - list of modules to be used as expensive ones
    use_none - adds probability to skip module execution
    """

    transaction_count = 15
    cheap_ratio = 0.95

    sleep_from = 30000
    sleep_to = 70000

    use_none = True
    cheap_modules = [enable_collateral_eralend, enable_collateral_basilisk, enable_collateral_reactorfusion,
                     create_safe, mint_zkstars, send_mail, check_in_secondlive]
    expensive_modules = [deposit_reactorfusion, deposit_zerolend, deposit_basilisk, deposit_eralend,
                         create_omnisea, create_safe, swap_multiswap]

    routes_inst = Routes(wallet_info)
    await routes_inst.start_automatic(transaction_count, cheap_ratio,
                                      sleep_from, sleep_to,
                                      cheap_modules, expensive_modules,
                                      use_none)


async def multi_approve(wallet_info):
    """
    Make approve all tokens from config in SyncSwap, Mute, SpaceFi, Pancake, WooFi, Velocore

    Disclaimer - You can use 0 for cancel  approve
    """

    amount = 0

    sleep_from = 30
    sleep_to = 95

    multiapprove = MultiApprove(wallet_info)
    await multiapprove.start(amount, sleep_from, sleep_to)


# -------------------------------------------- NO NEED TO SET UP MODULES

async def vote_rubyscore(wallet_info):
    """
    Vote in Scroll at Rubyscore
    """

    rubyscore_inst = Rubyscore(wallet_info)
    await rubyscore_inst.vote()


async def send_mail(wallet_info):
    dmail_inst = Dmail(wallet_info)
    await dmail_inst.send_mail()


async def send_message(wallet_info):
    l2telegraph_inst = L2Telegraph(wallet_info)
    await l2telegraph_inst.send_message()


async def mint_mailzero_nft(wallet_info):
    mint_nft_inst = MailZero(wallet_info)
    await mint_nft_inst.mint()


async def mint_zks_domain(wallet_info):
    zks_domain_inst = ZKSDomain(wallet_info)
    await zks_domain_inst.mint()


async def mint_era_domain(wallet_info):
    era_domain_inst = EraDomain(wallet_info)
    await era_domain_inst.mint()


async def withdraw_erlaned(wallet_info):
    eralend_inst = Eralend(wallet_info)
    await eralend_inst.withdraw()


async def enable_collateral_eralend(wallet_info):
    eralend_inst = Eralend(wallet_info)
    await eralend_inst.enable_collateral()


async def disable_collateral_eralend(wallet_info):
    eralend_inst = Eralend(wallet_info)
    await eralend_inst.disable_collateral()


async def withdraw_basilisk(wallet_info):
    basilisk_inst = Basilisk(wallet_info)
    await basilisk_inst.withdraw()


async def enable_collateral_basilisk(wallet_info):
    basilisk_inst = Basilisk(wallet_info)
    await basilisk_inst.enable_collateral()


async def disable_collateral_basilisk(wallet_info):
    basilisk_inst = Basilisk(wallet_info)
    await basilisk_inst.disable_collateral()


async def withdraw_reactorfusion(wallet_info):
    reactorfusion_inst = ReactorFusion(wallet_info)
    await reactorfusion_inst.withdraw()


async def enable_collateral_reactorfusion(wallet_info):
    reactorfusion_inst = ReactorFusion(wallet_info)
    await reactorfusion_inst.enable_collateral()


async def disable_collateral_reactorfusion(wallet_info):
    reactorfusion_inst = ReactorFusion(wallet_info)
    await reactorfusion_inst.disable_collateral()


async def withdraw_zerolend(wallet_info):
    zerolend_inst = ZeroLend(wallet_info)
    await zerolend_inst.withdraw()


async def create_omnisea(wallet_info):
    omnisea_inst = Omnisea(wallet_info)
    await omnisea_inst.create()


async def create_safe(wallet_info):
    gnosis_safe = GnosisSafe(wallet_info)
    await gnosis_safe.create_safe()


async def check_in_secondlive(wallet_info):
    """
    Check-in on second live
    """
    second_live = SecondLive(wallet_info)
    await second_live.sign_in()


def get_tx_count():
    asyncio.run(check_tx())
