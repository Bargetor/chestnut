def str_array_splice(array):
    if array is None:
        return None
    if len(array) == 0:
        return None
    resultStr = ''
    for str in array:
        resultStr += str
    return resultStr

def merged_dict(d1, d2):
    if not d1 : return d2
    if not d2 : return d1
    return dict(d1, **d2)
