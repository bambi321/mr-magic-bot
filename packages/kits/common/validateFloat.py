def validateFloat(testVar, errorStream):
    try:
        return float(testVar)
    except Exception as error:
        errorStream.processError(f"Number not validated as an float: {testVar}", error)
