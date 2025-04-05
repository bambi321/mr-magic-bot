from binance.client import Client

from packages.apiManagers.magicConfigAPI import (
    magicGetBinanceAPIKey,
    magicGetBinanceAPISecurity,
    magicGetBinancePointInterval,
    magicGetBinanceBaseCurrency,
    magicGetUseWatchList,
    magicGetWatchlist,
)


class MagicBinanceManager:
    def __init__(self, errorManager):
        self.__error = errorManager

        try:
            self.__client = Client(
                magicGetBinanceAPIKey(), magicGetBinanceAPISecurity()
            )
        except Exception as error:
            self.__error.processError(f"Could not connect to Binance API", error)
            return

        self.pointInterval = magicGetBinancePointInterval()

    # ----- PRIVATE METHODS -----

    def __getBalances(self):
        return self.__client.get_account()["balances"]

    # ----- PUBLIC METHODS -----

    def getWalletAssets(self):
        if magicGetUseWatchList():
            watchlist = magicGetWatchlist()
            return watchlist.split("|")

        try:
            balances = self.__getBalances()
        except Exception as error:
            self.__error.processError(f"Could not retrieve client balances", error)
            return self.__error.FAILURE

        walletAssets = []
        baseCurrency = magicGetBinanceBaseCurrency()
        for b in balances:
            if float(b["free"]):
                if b["asset"] == baseCurrency:
                    continue
                walletAssets.append(b["asset"] + baseCurrency)

        return walletAssets

    def getAssetHistory(self, asset, measureTime):
        quality = False

        try:
            klines = self.__client.get_historical_klines(
                asset, self.pointInterval, measureTime
            )
        except Exception as error:
            # bug fix - some wallet assets do not have ticker ratio to base currency, filter past these!
            if str(error) == "APIError(code=-1121): Invalid symbol.":
                self.__error.processError(
                    f"Could not retrieve history kline values for this asset: {asset}",
                    error,
                )
                return [[], quality]
            self.__error.processError("Connection timed out...retrying", error)
            self.__error.haltProgram(5)
            return self.getAssetHistory(
                asset, measureTime
            )  # recursive function to ensure good data return

        data = []
        for k in klines:
            data.append(k[4])

        if len(data):
            quality = True

        return [data, quality]
