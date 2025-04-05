class MagicAlgorithm():
    def __init__(self, errorManager, logger, name):
        self.name = name
        self._errorManager = errorManager
        self._logger = logger

    def analyse(self, name=None, dataset=None):
        self._logger.log(f'This algorithm does not have an implemented analyse method: ${self.name}')