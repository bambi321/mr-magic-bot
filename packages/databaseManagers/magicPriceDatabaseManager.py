from packages.databaseManagers.magicDatabaseManager import MagicDatabaseManager
from packages.apiManagers.magicConfigAPI import magicGetPricesDb

class MagicPriceDatabaseManager(MagicDatabaseManager):

    tableSQLType = "(price float NOT NULL)"

    def __init__(self, errorManager, logger):
        super().__init__(errorManager, logger, magicGetPricesDb())

    def createTable(self, tableName):
        return self._createTable(tableName, self.tableSQLType)
    
    def droptable(self, tableName):
        return self._dropTable(tableName)

    def insertValue(self, tableName, priceValue):
        return self._insertValue(tableName, f'({priceValue})')

    def insertValues(self, tableName, priceValues):
        for priceValue in priceValues:
            self._insertValue(tableName, f'({priceValue})')

    def collectValues(self, tableName):
        results = self._collectValues(tableName)

        trimmedData = []
        for r in results:
            trimmedData.append(r[0])
        return trimmedData
    
    # ----- QUALITY MANAGEMENT -----

    def createQualitiesTable(self, assets):
        tableName = 'QUALITIES'
        self._dropTable(tableName)

        qualitiesSQLType = '(assetName string NOT NULL, quality string NOT NULL)'
        self._createTable(tableName, qualitiesSQLType)
        for asset in assets:
            [assetName, quality] = asset
            self._insertValue(tableName, f'("{assetName}", "{quality}")')

    def collectQualityValues(self):
        qualities = self._collectValues('QUALITIES')

        modifiedData = []
        for quality in qualities:
            [assetName, foundQuality] = quality
            q = False
            if (foundQuality == 'True'): q = True

            modifiedData.append((assetName, q))

        return modifiedData
