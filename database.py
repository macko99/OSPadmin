import requests
import json


class DataBase:
    url = 'https://ospapp-53708.firebaseio.com/.json?auth='

    def __init__(self, tmp_file):
        with open("secret", 'r') as file:
            self.url = self.url + file.read().split("\n")[0]
        try:
            with open(tmp_file, 'w') as file:
                file.write(str(requests.get(self.url).json()).replace("'", '"'))
            with open(tmp_file) as file:
                self.store = json.load(file)
        except Exception as e:
            print(str(e))

    def firebase_delete_all(self): #ok
        try:
            for key in self.store:
                requests.delete(url=self.url[:-5] + key + ".json")
        except Exception as e:
            print(str(e))

    def get_report(self, uuid_num): #ok
        return self.store[uuid_num]

    def get_all_friendly(self): #ok
        result = []
        for item in self.store:
            if 'deleted' not in item:
                data = self.store[item]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
        return result

    def get_deleted(self): #ok
        result = []
        for item in self.store:
            if 'deleted' in item:
                data = self.store[item[8:]]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
        return result

    def find_report(self, id_number): #ok
        for item in self.store:
            if 'deleted' not in item:
                if self.store[item]["innerID"] == id_number:
                    return item