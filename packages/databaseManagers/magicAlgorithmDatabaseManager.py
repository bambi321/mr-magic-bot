from packages.databaseManagers.magicDatabaseManager import MagicDatabaseManager
from packages.apiManagers.magicConfigAPI import magicGetAlgorithmsDb

class MagicAlgorithmDatabaseManager(MagicDatabaseManager):

    def __init__(self, errorManager, logger):
        super().__init__(errorManager, logger, magicGetAlgorithmsDb())

    def createTable(self, tableName, tableSQLType):
        return self._createTable(tableName, tableSQLType)

    def insertEntries(self, tableName, entries):
        for entry in entries:
            if entry != None: self.insertEntry(tableName, entry)
            else: self._error.handleError(f"Attemped entry insertion into {tableName} is None")

    def insertEntry(self, tableName, entry):
        self._insertValue(tableName, entry)
