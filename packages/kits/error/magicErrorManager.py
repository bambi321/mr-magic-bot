from time import sleep

from packages.apiManagers.magicConfigAPI import magicGetBinanceSleepTime, magicGetShowErrorMessages
from packages.kits.error.magicErrorException import MagicErrorException

class MagicErrorManager:

    def __init__(self):
        self.SUCCESS = 0
        self.FAILURE = 1
        self.__showErrorMessages = magicGetShowErrorMessages()

        if not self.__showErrorMessages:
            print("You have turned off error messages.  Please don't break me :)")

    def processError(self, message, error=None):
        if self.__showErrorMessages:
            print(f"Error: {message} -> {error}")

    def raiseException(self, exceptionMessage):
        print(f"Error: {exceptionMessage}")
        raise MagicErrorException()

    def handleError(self, message):
        if self.__showErrorMessages:
            print(f"{message}")  

    def haltProgram(self, t = magicGetBinanceSleepTime()):
        t = int(t)
        while t >= 0:
            # If there is more than 5 seconds, count in 10 sec intervals
            if t > 5 and t % 10 == 0: print(f"...{t} seconds")
            # else, print all numbers
            elif t <= 5: print(f"...{t} seconds")
            t -= 1
            # sleep for 1 second inbetween timers
            sleep(1)

         