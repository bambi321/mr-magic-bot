def validateInteger(testVar, errorStream=None):
    try:
        return int(testVar)
    except Exception as error:
        errorStream.processError(f"Number not validated as an integer: {testVar}", error)
