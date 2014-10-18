def StrArraySplice(array):
    if array is None:
        return None
    if len(array) == 0:
        return None
    resultStr = ''
    for str in array:
        resultStr += str
    return resultStr
