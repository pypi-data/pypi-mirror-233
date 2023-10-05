"""
 DEX SWAP Main
"""

from typing import Optional

from loguru import logger
from web3 import Web3

from dxsp import __version__
from dxsp.config import settings
from dxsp.protocols import DexKwenta, DexUniswap, DexZeroX


class DexSwap:
    """
    class to build a DexSwap Object
     use to interact with the dex protocol

     Args:
         w3 (Optional[Web3]): Web3

     Returns:
         DexSwap

     Methods:
        _create_client()
        get_quote()
        execute_order()
        get_help()
        get_info()
        get_name()
        get_account_balance()
        get_account_position()



    """

    def __init__(self, w3: Optional[Web3] = None):
        """
        Initialize the DexTrader object
        to interact with exchanges

        """
        exchanges = settings.dex
        self.dex_info = []
        try:
            for dx in exchanges:
                logger.debug(f"Loading {dx}")
                name = dx
                wallet_address = exchanges[dx]["wallet_address"]
                private_key = exchanges[dx]["private_key"]
                w3 = Web3(Web3.HTTPProvider(exchanges[dx]["rpc"]))
                protocol_type = exchanges[dx]["protocol_type"]
                protocol_version = exchanges[dx]["protocol_version"]
                api_endpoint = exchanges[dx]["api_endpoint"]
                api_key = exchanges[dx]["api_key"]
                router_contract_addr = exchanges[dx]["router_contract_addr"]
                factory_contract_addr = exchanges[dx]["factory_contract_addr"]
                trading_risk_percentage = (
                    True or exchanges[dx]["trading_risk_percentage"]
                )
                trading_risk_amount = 1 or exchanges[dx]["trading_risk_amount"]
                trading_slippage = 2 or exchanges[dx]["trading_slippage"]
                trading_asset_address = "" or exchanges[dx]["trading_asset_address"]
                trading_asset_separator = "" or exchanges[dx]["trading_asset_separator"]
                block_explorer_url = exchanges[dx]["block_explorer_url"]
                block_explorer_api = exchanges[dx]["block_explorer_api"]
                mapping = exchanges[dx]["mapping"]
                client = self._create_client(
                    name=name,
                    wallet_address=wallet_address,
                    private_key=private_key,
                    w3=w3,
                    protocol_type=protocol_type,
                    protocol_version=protocol_version,
                    api_endpoint=api_endpoint,
                    api_key=api_key,
                    router_contract_addr=router_contract_addr,
                    factory_contract_addr=factory_contract_addr,
                    trading_asset_address=trading_asset_address,
                    trading_risk_percentage=trading_risk_percentage,
                    trading_risk_amount=trading_risk_amount,
                    trading_slippage=trading_slippage,
                    trading_asset_separator=trading_asset_separator,
                    block_explorer_url=block_explorer_url,
                    block_explorer_api=block_explorer_api,
                    mapping=mapping,
                )
                self.dex_info.append(client)
            logger.debug("init complete")

        except Exception as e:
            logger.error(e)

    def _create_client(self, **kwargs):
        protocol_type = kwargs["protocol_type"]
        if protocol_type == "uniswap":
            return DexUniswap(**kwargs)
        elif protocol_type == "0x":
            return DexZeroX(**kwargs)
        elif protocol_type == "kwenta":
            return DexKwenta(**kwargs)
        else:
            logger.error(f"protocol type {protocol_type} not supported")

    async def get_quotes(self, sell_token):
        """
        gets a quote for a token

        Args:
            sell_token (str): The sell token.

        Returns:
            str: The quote with the trading symbol

        """
        logger.debug("get quote", sell_token)
        info = "🦄\n"
        for dx in self.dex_info:
            logger.debug("get quote {}", dx)
            buy_address = dx.trading_asset_address
            sell_token = await dx.replace_instrument(sell_token)
            sell_address = await dx.contract_utils.search_contract_address(sell_token)
            quote = await dx.get_quote(buy_address, sell_address) or "Quote failed"
            symbol = await dx.contract_utils.get_token_symbol(dx.trading_asset_address)
            info += f"{dx.name}: {quote} {symbol}\n"

        return info.strip()

    async def submit_order(self, order_params):
        """
        Execute an order function.

        Args:
            order_params (dict): The order parameters.

        Returns:
            str: The trade confirmation

        """
        try:
            for dx in self.dex_info:
                logger.debug("submit order {}", dx)
                action = order_params.get("action")
                instrument = await dx.replace_instrument(order_params.get("instrument"))
                quantity = order_params.get("quantity", 1)
                sell_token, buy_token = (
                    (dx.trading_asset_address, instrument)
                    if action == "BUY"
                    else (instrument, dx.trading_asset_address)
                )
                order = await dx.get_swap(sell_token, buy_token, quantity)
                if order:
                    trade_confirmation = (
                        f"⬇️ {instrument}"
                        if (action == "SELL")
                        else f"⬆️ {instrument}\n"
                    )
                    trade_confirmation += order
            return trade_confirmation

        except Exception as error:
            return f"⚠️ order execution: {error}"

    async def get_info(self):
        """
        Get information from the account.

        :return: The information retrieved from the account.
        """
        info = f"ℹ️  v{__version__}\n"
        for dx in self.dex_info:
            info += f"\n{await dx.get_info()}" or "Info failed\n"
        return info.strip()

    # 🔒 USER RELATED
    async def get_balances(self):
        """
        Retrieves the account balance.

        :return: The account balance.
        :rtype: float
        """
        info = "💵\n"
        for dx in self.dex_info:
            info += f"\n{dx.name}:"
            info += f"{await dx.get_account_balance()}"
        return info.strip()

    async def get_positions(self):
        """
        Retrieves the account position.

        :return: The account position.
        :rtype: AccountPosition
        """
        info = "📊\n"
        for dx in self.dex_info:
            info += f"\n{dx.name}:"
            info += f"{await dx.get_account_position()}"
        return info.strip()
