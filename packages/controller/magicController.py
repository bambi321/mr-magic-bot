from packages.databaseManagers.magicPriceDatabaseManager import (
    MagicPriceDatabaseManager,
)
from packages.databaseManagers.magicAlgorithmDatabaseManager import (
    MagicAlgorithmDatabaseManager,
)
from packages.databaseManagers.magicResultsDatabaseManager import (
    MagicResultsDatabaseManager,
)
from packages.apiManagers.magicBinanceManager import MagicBinanceManager
from packages.apiManagers.magicConfigAPI import (
    magicGetUseBinanceMock,
    magicGetUseMovingAverage,
    magicGetUseRelativeStrengthIndex,
)
from packages.kits.datetime.magicDateTimeManager import MagicDateTimeManager
from packages.algorithmManagers.movingAverageAlgorithm import MovingAverageAlgorithm
from packages.algorithmManagers.relativeStrengthIndexAlgorithm import (
    RelativeStrengthIndexAlgorithm,
)
from packages.mocks.mockBinanceAPIManager import MockBinanceManager


class MagicController:
    def __init__(self, errorManager, logger):
        self._errorManager = errorManager
        self._logger = logger
        self._datetimeManager = MagicDateTimeManager(self._errorManager, self._logger)
        self._pricesDatabase = MagicPriceDatabaseManager(
            self._errorManager, self._logger
        )
        self._algorithmsDatabase = MagicAlgorithmDatabaseManager(
            self._errorManager, self._logger
        )
        self._resultsDatabase = MagicResultsDatabaseManager(
            self._errorManager, self._logger
        )

        self._addAlgorithms()

        if magicGetUseBinanceMock():
            self._binanceAPI = MockBinanceManager(self._errorManager)
        else:
            self._binanceAPI = MagicBinanceManager(self._errorManager)

    def _addAlgorithms(self):
        self._algorithms = []
        # add more algorithms here
        if magicGetUseMovingAverage():
            self._algorithms.append(
                MovingAverageAlgorithm(self._errorManager, self._logger)
            )
        if magicGetUseRelativeStrengthIndex():
            self._algorithms.append(
                RelativeStrengthIndexAlgorithm(self._errorManager, self._logger)
            )

    def updatePriceDatabase(self):
        self._logger.log("...updating price databases...")

        measureTime = self._datetimeManager.getMeasureDate(
            self._datetimeManager.getTimeNow()
        )
        assetNames = self._binanceAPI.getWalletAssets()

        if assetNames == self._errorManager.FAILURE:
            self._errorManager.raiseException("Could not retrieve assetNames")

        qualities = []
        for assetName in assetNames:
            [data, quality] = self._binanceAPI.getAssetHistory(assetName, measureTime)
            if quality:
                self._pricesDatabase.createTable(assetName)
                self._pricesDatabase.insertValues(assetName, data)
                self._logger.log(f"......updated {assetName} with new data!")
            else:
                self._logger.log(f"......failed to update {assetName} with new data!")

            qualities.append([assetName, quality])

        self._logger.log("...updating qualities!")
        self._pricesDatabase.createQualitiesTable(qualities)

    def analyse(self):
        qualities = self._pricesDatabase.collectQualityValues()
        for algorithm in self._algorithms:
            self._logger.log(f"...analysing data with {algorithm.name}...")

            entries = []

            for asset in qualities:
                [assetName, quality] = asset
                if quality:
                    assetData = self._pricesDatabase.collectValues(assetName)
                    entries.append(algorithm.analyse(assetName, assetData))

            self._algorithmsDatabase.createTable(algorithm.name, algorithm.tableSQLType)
            self._algorithmsDatabase.insertEntries(algorithm.name, entries)
