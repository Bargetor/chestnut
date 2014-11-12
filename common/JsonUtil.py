import json

class JsonObject(object):
    """docstring for ChestnutJson"""
    def __init__(self, dic = None):
        super(JsonObject, self).__init__()
        self.__init_chestnut_json()
        if dic is not None:
            self.data = dic.copy()



    def __init_chestnut_json(self):
        self.data = {}

    def get_json_str(self):
        return json.dumps(self.data)

    def append(self, name, value):
        self.data[name] = value

    def append_chestnut_json(self, name, chestnut_json):
        self.append(name, chestnut_json.data)

    def __str__(self):
        return self.get_json_str()



# chestnut_json = ChestnutJson()
# dic = {'a' : 'b'}
# chestnut_json.append('c', dic)
# print chestnut_json
