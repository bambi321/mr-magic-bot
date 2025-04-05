import random

from packages.apiManagers.magicConfigAPI import magicGetBinancePointInterval, magicGetDataHistoryScalar, magicGetDataHistoryUnit



class MockBinanceManager():

    def __init__(self, errorManager):
        self._errorManager = errorManager
        self._pointInterval = magicGetBinancePointInterval()

        self._dataHistoryUnit = self.__validateUnit(magicGetDataHistoryUnit())
        self._dataHistoryScalar = self.__validateScalar(magicGetDataHistoryScalar())

        print("You are using a mocked version of our Binance API.  Good Luck :)")


    def getWalletAssets(self):
        # mocked asset names
        return ["ADAUSDT", "BTCUSDT", "ENJUSDT", "TRUUSDT", "AIONUSDT", "DOGEUSDT", "ETHWUSDT", "SANDUSDT", "WAVEUSDT", 'AUDUSDT', 'DOTUSDT', 'MATICUSDT', 'SOLUSDT', 'XRPUSDT']
    
    def getAssetHistory(self, asset, measureTime):
        # generate random data for each asset

        pointsPerDay = 0
        if self._pointInterval == '15m':
            pointsPerDay = 4 * 24 # points per day
        elif self._pointInterval == '30m':
            pointsPerDay = 2 * 24
        elif self._pointInterval == '1h':
            pointsPerDay = 24
        else:
            self._errorManager(f"Currently do not support {self.__pointInterval} in Mocked BinanceAPI")
        
        daysPerRequestedPeriod = 0
        if self._dataHistoryUnit == 'day':
            daysPerRequestedPeriod = 1
        elif self._dataHistoryUnit == 'week':
            daysPerRequestedPeriod = 7
        elif self._dataHistoryUnit == 'month':
            daysPerRequestedPeriod = 30
        elif self._dataHistoryUnit == 'year':
            daysPerRequestedPeriod = 365

        totalPoints = pointsPerDay * daysPerRequestedPeriod * self._dataHistoryScalar

        data = []
        data.append(1000) # starting point
        for p in range(1, totalPoints):
            # calculate random value between -2 and 2
            randomVal = random.randint(0, 4) - 2
            data.append(data[p-1] + randomVal)

        return [data, True]
    
    def __validateUnit(self, unit):
        if unit == "day" or unit == "week" or unit == "month" or unit == "year":
            return unit
        else:
            self.__error.handleError("Unit to collect data history must be of type (day, week, month, year)")
            return None

    def __validateScalar(self, scalar):
        try:
            return int(scalar)
        except Exception as error:
            self.__error.processError("Scalar must be of type integer!", error)
            return None
