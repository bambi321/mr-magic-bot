from packages.algorithmManagers.magicAgorithm import MagicAlgorithm
from packages.apiManagers.magicConfigAPI import magicGetRelativeStrengthIndexOverDays
from packages.apiManagers.magicConfigAPI import magicGetBinancePointInterval
from packages.apiManagers.magicConfigAPI import magicGetRelativeStrengthIndexBuyThreshold
from packages.apiManagers.magicConfigAPI import magicGetRelativeStrengthIndexSellThreshold
from packages.kits.common.validateInteger import validateInteger
from packages.kits.common.calculateDatapoints import calculateDatapointsFromDaysAndInterval

class RelativeStrengthIndexAlgorithm(MagicAlgorithm):

    tableSQLType = """(assetName string NOT NULL, 
                       quality string NOT NULL,
                       verdict string NOT NULL,
                       RS float NOT NULL,
                       RSI float NOT NULL
                 ) """

    def __init__(self, errorManager, logger):
        super().__init__(errorManager, logger, "RelativeStrengthIndex")

        self.buyThreshold = validateInteger(magicGetRelativeStrengthIndexBuyThreshold())
        self.sellThreshold = validateInteger(magicGetRelativeStrengthIndexSellThreshold())


    def _createAlgorithmEntry(self, assetName, quality, verdict=None, RS=None, RSI=None):
        entry = "("
        entry += f'"{assetName}", '
        entry += f'"{quality}", '
        entry += f'"{verdict}", '
        entry += f'{RS}, '
        entry += f'{RSI}'
        entry += ')'

        return entry
    
    def _getVerdict(self, RSI):
        if RSI >= self.sellThreshold:
            return 'SELL'
        elif RSI <=self.buyThreshold:
            return 'BUY'
        return 'INCONCLUSIVE'

    def analyse(self, assetName, dataset):
        self._logger.log(f"......analysing {assetName} with {self.name}")
        overDays = validateInteger(magicGetRelativeStrengthIndexOverDays(), self._errorManager)
        if overDays <= 0 or overDays > 100:
            self._errorManager.handleError("Your 'OverDays' time period must be greater than zero...but not that big?")
            return self._createAlgorithmEntry(assetName, False)
        
        noOfDatapoints = calculateDatapointsFromDaysAndInterval(overDays, magicGetBinancePointInterval())
        noOfDatapoints = validateInteger(noOfDatapoints)
        if noOfDatapoints <= 0 or noOfDatapoints > len(dataset):
            self._errorManager.processError(f"Asset: ${assetName} dataset could not be parsed with {noOfDatapoints} number of datapoints")
            return self._createAlgorithmEntry(assetName, False)
        
        listOfGains = []
        listOfLosses = []
        for point in range(len(dataset) - noOfDatapoints + 1, len(dataset)):
            diff = dataset[point] - dataset[point - 1]
            if diff > 0:
                listOfGains.append(diff)
            elif diff < 0:
                listOfLosses.append(abs(diff))

        avgGain = sum(listOfGains)/len(listOfGains)
        avgLoss = sum(listOfLosses)/len(listOfLosses)

        RS = avgGain / avgLoss # calculate relative strength
        RSI = 100 - (100/(1 + RS)) # calculate relative strength index

        verdict = self._getVerdict(RSI)

        return self._createAlgorithmEntry(assetName, True, verdict, RS, RSI)
        
        


