from datetime import datetime

from packages.apiManagers.magicConfigAPI import magicGetBinanceAPIKey, magicGetBinanceAPISecurity, magicGetDataHistoryScalar, magicGetDataHistoryUnit
from packages.kits.error.magicErrorManager import MagicErrorManager

class MagicDateTimeManager():

    def __init__(self, errorManager, logger):
        self.__error = errorManager
        self.__logger = logger
        self.__dataHistoryUnit = self.__validateUnit(magicGetDataHistoryUnit())
        self.__dataHistoryScalar = self.__validateScalar(magicGetDataHistoryScalar())

    # ----- PRIVATE METHODS -----

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

    def __deconstructDateVariables(self, time):
        return [time.year, time.month, time.day]

    def __constructDateString(self, year, month, day):
        output = f"{day} "

        if month == 1: output += "Jan "
        elif month == 2: output += "Feb "
        elif month == 3: output += "Mar "
        elif month == 4: output += "Apr "
        elif month == 5: output += "May "
        elif month == 6: output += "Jun "
        elif month == 7: output += "Jul "
        elif month == 8: output += "Aug "
        elif month == 9: output += "Sep"
        elif month == 10: output += "Oct "
        elif month == 11: output += "Nov "
        elif month == 12: output += "Dec "

        output += f",{year}"

        return output

    def __getMeasureDateDAY(self, datetime):
        self.__logger.log('to be implemented')

    def __getMeasureDateWEEK(self, datetime):
        self.__logger.log('to be implemented')

    def __getMeasureDateMONTH(self, datetime):
        [year, month, day] = self.__deconstructDateVariables(datetime)

        for _ in range(self.__dataHistoryScalar):
            month -= 1
            if month == 0:
                year -= 1
                month = 12

        # bug fix: if day = 31 and month lands on a non-31 day month, approximate to the 30th
        if month in [4, 6, 9, 11] and day == 31:
            day = 30

        return self.__constructDateString(year, month, day)

    # ----- PUBLIC METHODS -----

    def getTimeNow(self):
        return datetime.now()

    def getMeasureDate(self, datetime):
        unit = self.__dataHistoryUnit.lower()
        if unit == "day": return self.__getMeasureDateDAY(datetime)
        elif unit == "week": return self.__getMeasureDateWEEK(datetime)
        elif unit == "month": return self.__getMeasureDateMONTH(datetime)
        elif unit == "year": return self.__getMeasureDateYear(datetime)