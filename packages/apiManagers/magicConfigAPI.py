import configparser

rootConfigPath = "./config"

# Config File Paths
binanceConfigSetupPath = f"{rootConfigPath}/binance.cfg"
generalConfigSetupPath = f"{rootConfigPath}/general.cfg"
algorithmConfigSetupPath = f"{rootConfigPath}/algorithm.cfg"
watchlistConfigSetupPath = f"{rootConfigPath}/watchlist.cfg"

# --------------------------------
# Binance Config API
# --------------------------------

binanceConfig = configparser.ConfigParser()
binanceConfig.read(binanceConfigSetupPath)


def magicGetBinanceAPIKey():
    return binanceConfig["API-KEY"]["value"]


def magicGetBinanceAPISecurity():
    return binanceConfig["SECURITY-KEY"]["value"]


# --------------------------------
# Algorithm Config API
# --------------------------------

algorithmConfig = configparser.ConfigParser()
algorithmConfig.read(algorithmConfigSetupPath)


def magicGetUseMovingAverage():
    return algorithmConfig["USE-ALGORITHM"]["movingAverage"].lower() == "true"


def magicGetUseRelativeStrengthIndex():
    return algorithmConfig["USE-ALGORITHM"]["relativeStrengthIndex"].lower() == "true"


def magicGetMovingAverageCompareInterval():
    return algorithmConfig["MOVING-AVERAGE"]["comparePercentage"]


def magicGetRelativeStrengthIndexOverDays():
    return algorithmConfig["RELATIVE-STRENGTH-INDEX"]["overDays"]


def magicGetRelativeStrengthIndexBuyThreshold():
    return algorithmConfig["RELATIVE-STRENGTH-INDEX"]["buyThreshold"]


def magicGetRelativeStrengthIndexSellThreshold():
    return algorithmConfig["RELATIVE-STRENGTH-INDEX"]["sellThreshold"]


# --------------------------------
# General Config API
# --------------------------------

generalConfig = configparser.ConfigParser()
generalConfig.read(generalConfigSetupPath)


def magicGetShowErrorMessages():
    return generalConfig["RUNTIME-CONFIG"]["showErrorMessages"].lower() == "true"


def magicGetShowLogMessages():
    return generalConfig["RUNTIME-CONFIG"]["showLogMessages"].lower() == "true"


def magicGetSkipDataCollection():
    return generalConfig["RUNTIME-CONFIG"]["skipDataCollection"].lower() == "true"


def magicGetSkipAnalysis():
    return generalConfig["RUNTIME-CONFIG"]["skipAnalysis"].lower() == "true"


def magicGetUseWatchList():
    return generalConfig["RUNTIME-CONFIG"]["useWatchlist"].lower() == "true"


def magicGetUseBinanceMock():
    return generalConfig["MOCK"]["useBinanceMock"].lower() == "true"


def magicGetUseSelfwealthMock():
    return generalConfig["MOCK"]["useSelfwealthMock"].lower() == "true"


def magicGetPricesDb():
    return generalConfig["DATABASE"]["pricesFilepath"]


def magicGetAlgorithmsDb():
    return generalConfig["DATABASE"]["algorithmsFilepath"]


def magicGetResultsDb():
    return generalConfig["DATABASE"]["resultsFilepath"]


def magicGetDataHistoryUnit():
    return generalConfig["DATA-HISTORY"]["unit"]


def magicGetDataHistoryScalar():
    return generalConfig["DATA-HISTORY"]["scalar"]


def magicGetBinancePointInterval():
    return generalConfig["BINANCE"]["interval"]


def magicGetBinanceSleepTime():
    return generalConfig["BINANCE"]["sleepTime"]


def magicGetBinanceBaseCurrency():
    return generalConfig["BINANCE"]["baseCurrency"]


# --------------------------------
# Watchlist Config API
# --------------------------------

watchlistConfig = configparser.ConfigParser()
watchlistConfig.read(watchlistConfigSetupPath)


def magicGetWatchlist():
    return watchlistConfig["WATCHLIST"]["watchlist"]
