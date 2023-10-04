##
##  Copyright (c) 2021 unSkript, Inc
##  All rights reserved.
##

import json

class NBParams():
    """
    This takes params as json string.
    """
    def __init__(self, params_json:str):
        self.paramsDict = json.loads(params_json)
    """
    Returns the value corresponding to a key.
    """
    def get(self, key:str):
        if key not in self.paramsDict.keys():
            print(f'key {key} not found')
            return None
        return self.paramsDict.get(key)
    """
    Returns the paramsDict dictionary.
    """
    def getParamsDict(self):
        return self.paramsDict





