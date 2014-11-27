import re

def match(r, string):
    pattern = re.compile(r)
    return pattern.match(string)

def findall(r, string):
    return re.findall(r, string)
