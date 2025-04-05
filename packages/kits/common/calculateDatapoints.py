import re

from packages.kits.common.validateInteger import validateInteger

def calculateDatapointsFromDaysAndInterval(noOfDays, pointInterval):
    match = re.match(r'^(\d+)([a-zA-Z])', pointInterval)

    if match:
        val = validateInteger(match.group(1))
        span = match.group(2)

        # noOfPointsPerDay = 24 * pointPerHour -> pointsPerHour = minutesPerHour/minutesPerPoint
        # noOfPointsPerDay = 1 * pointsPerDay
        noOfPointsPerDay = 0
        if span == 'm':
            noOfPointsPerDay = 24 * 60/val
        elif span == 's':
            # secondsPerPoint = val
            noOfPointsPerDay = 24 * 60 * 60/val
        elif span == 'h':
            noOfPointsPerDay = 24/val
        
    return noOfPointsPerDay * noOfDays