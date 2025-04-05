from packages.controller.magicController import MagicController
from packages.kits.error.magicErrorManager import MagicErrorManager
from packages.kits.logger.magicLoggerManager import MagicLoggerManager
from packages.apiManagers.magicConfigAPI import magicGetSkipDataCollection, magicGetSkipAnalysis

def main():
    errorManager = MagicErrorManager()
    logger = MagicLoggerManager()
    controller = MagicController(errorManager, logger)

    if (not magicGetSkipDataCollection()): controller.updatePriceDatabase()
    else: logger.log("You have skipped data collection.  Hope you have data already!")

    if (not magicGetSkipAnalysis()): controller.analyse()
    else: logger.log('You have skipped data analysis.  Hope you have results already!')


print('...starting script...welcome to mr magic')
main()
print('...finishing script...')
