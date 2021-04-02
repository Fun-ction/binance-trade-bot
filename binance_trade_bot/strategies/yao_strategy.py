from binance_trade_bot.auto_trader import AutoTrader
from binance_trade_bot.utils import get_market_ticker_price_from_list
from typing import Dict


class Strategy(AutoTrader):
    def scout(self):
        """
        Scout for potential jumps from the current coin to another coin
        """
        all_tickers = self.manager.get_all_market_tickers()
        coins = set()
        owned_coins = set()
        coin_prices : Dict[Coin, float] = {}
        # scouted_coins = {}

        for coin in self.db.get_coins():
            current_coin_balance = self.manager.get_currency_balance(coin.symbol)
            coin_price = get_market_ticker_price_from_list(all_tickers, coin + self.config.BRIDGE)

            if coin_price is None:
                self.logger.info("Skipping scouting... current coin {} not found".format(coin + self.config.BRIDGE))
                continue

            if coin_price * current_coin_balance < self.manager.get_min_notional(
                coin.symbol, self.config.BRIDGE.symbol
            ):
                continue
            owned_coins.add(coin.symbol)
            coins.add(coin)
            coin_prices[coin] = coin_price

        for coin in coins :

            # Display on the console, the current coin+Bridge, so users can see *some* activity and not think the bot
            # has stopped. Not logging though to reduce log size.
            self.logger.info(f"Scouting for best trades. Current ticker: {coin + self.config.BRIDGE} ", False)
            # scouted_coins.add(coin)

            self._jump_to_best_nonnotational_coin(coin, coin_prices[coin], all_tickers, owned_coins)

        # self.logger.info(f"Scouted for best trades. Current tickers: {scouted_coins} with bridge {self.config.BRIDGE}", False)
        self.bridge_scout()
