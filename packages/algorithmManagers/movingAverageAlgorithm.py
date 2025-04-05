from time import sleep

from packages.algorithmManagers.magicAgorithm import MagicAlgorithm

from packages.apiManagers.magicConfigAPI import magicGetMovingAverageCompareInterval
from packages.kits.common.validateInteger import validateInteger
from packages.kits.common.validateFloat import validateFloat

class MovingAverageAlgorithm(MagicAlgorithm):

    tableSQLType = """(assetName string NOT NULL, 
                       quality string NOT NULL,
                       verdict string NOT NULL,
                       strength float NOT NULL,
                       pointAverage float NOT NULL,
                       compareAverage float NOT NULL,
                       compareInterval float NOT NULL
                 ) """

    def __init__(self, errorManager, logger):
        super().__init__(errorManager, logger, "MovingAverage")

    def _createAlgorithmEntry(self, assetName, quality, verdict=None, strength=None, pointAverage=None, compareAverage=None, compareInterval=None):

        entry = '('
        entry += f'"{assetName}", '
        entry += f'"{quality}", '
        entry +=  f'"{verdict}", '
        entry += f'{strength}, '
        entry += f'{pointAverage}, '
        entry += f'{compareAverage}, '
        entry += f'{compareInterval}'
        entry += ')'

        return entry

    def _getVerdict(self, pointAverage, compareAverage):
        diff = abs(pointAverage - compareAverage)
        strength = diff / pointAverage * 100

        if pointAverage > compareAverage: verdict = 'BUY'
        elif pointAverage < compareAverage: verdict = 'SELL'
        else: verdict = 'INCONCLUSIVE'

        return [verdict, strength]

    def analyse(self, assetName, dataset):
        self._logger.log(f"......analysing {assetName} with {self.name}")
        compareInterval = validateFloat(magicGetMovingAverageCompareInterval(), self._errorManager)
        noOfPoints = len(dataset)
        noOfPointsForCompare = validateInteger(compareInterval/100 * noOfPoints, self._errorManager)

        pointSum = 0
        compareSum = 0
        if compareInterval == None or compareInterval <= 0 or compareInterval >= 100:
            self._errorManager.processError(f"Passed Interval to compare Moving Average is invalid!  Value must be between 0 and 100 -> {compareInterval}")
            return self._createAlgorithmEntry(assetName, False)

        for data in dataset:
            pointSum += data

        if (noOfPoints - noOfPointsForCompare < 0):
            self._logger.log(f'.........failed to analyse {assetName} with {self.name}.  You have tried to analyse a greater dataset than what we have recorded!')
            return self._createAlgorithmEntry(assetName, False)

        for index in range(noOfPoints - noOfPointsForCompare, noOfPoints):
            compareSum += dataset[index]

        pointAverage = pointSum/noOfPoints
        compareAverage = compareSum/noOfPointsForCompare

        [verdict, strength] = self._getVerdict(pointAverage, compareAverage)

        return self._createAlgorithmEntry(assetName, True, verdict, strength, pointAverage, compareAverage, compareInterval)



        


