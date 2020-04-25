import os

import requests
import json


class DataBase:
    url = 'https://ospapp-53708.firebaseio.com/.json?auth='

    def __init__(self, tmp_file, heroes_file):
        with open("secret", 'r') as file:
            self.url = self.url + file.read().split("\n")[0]
        try:
            with open(heroes_file, 'r') as file:
                string = "{'heroes': " + str(file.read().__add__("\ninny, w sczegółach").split("\n")) + "}"
                to_database = json.loads(string.replace("'", '"'))
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print("brak pliku strażacy.txt lub błąd połączenia z bazą " + str(e))
        try:
            with open(tmp_file, 'w') as file:
                file.write(str(requests.get(self.url).json()).replace("'", '"').replace('/', "."))
        except Exception as e:
            print("błąd pobierania danych z bazy " + str(e))
        try:
            with open(tmp_file) as file:
                self.store = json.load(file)
        except Exception as e:
            print("Baza danych jest pusta, kończę ")
            os.remove("tmp.json")
            exit(0)

    def firebase_delete_all(self):  # ok
        try:
            for key in self.store:
                if 'heroes' not in key:
                    requests.delete(url=self.url[:-5] + key + ".json")
        except Exception as e:
            print("nie udało się usunąć raportów z bazy " + str(e))

    def get_report(self, uuid_num):  # ok
        return self.store[uuid_num]

    def get_all_friendly(self):  # ok
        result = []
        ready = []
        for item in self.store:
            if 'deleted' not in item and 'heroes' not in item:
                data = self.store[item]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
                if data["ready"] == "tak":
                    ready.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
        return result, ready

    def get_deleted(self):  # ok
        result = []
        for item in self.store:
            if 'deleted' in item:
                data = self.store[item[8:]]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":",""))
        return result

    def find_report(self, id_number):  # ok
        for item in self.store:
            if 'deleted' not in item and 'heroes' not in item:
                if self.store[item]["innerID"] == id_number:
                    return item
