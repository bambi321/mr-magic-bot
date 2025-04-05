from packages.databaseManagers.magicDatabaseManager import MagicDatabaseManager
from packages.apiManagers.magicConfigAPI import magicGetResultsDb

class MagicResultsDatabaseManager(MagicDatabaseManager):

    def __init__(self, errorManager, logger):
        super().__init__(errorManager, logger, magicGetResultsDb())
