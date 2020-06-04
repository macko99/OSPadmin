import requests
import json


class DataBase:
    base_url = 'https://osptest-3ddc5.firebaseio.com/'
    url = ''
    secret = ''

    def __init__(self, tmp_file, heroes_file, passwd_path, action_type_file):
        try:
            with open("OSPadmin_dane/logowanie.txt", 'r') as file:
                arr = file.read().split("\n")
                user = arr[0]
                password = arr[1]
        except Exception as e:
            raise Exception("brak pliku logowanie.txt " + str(e))

        global user_passwd
        with open("OSPadmin_dane/secret", 'r') as file:
            self.secret = file.read().split("\n")[0]
        try:
            user_passwd = str(requests.get(self.base_url + "passwd/" + user + self.secret).json())
        except Exception as e:
            raise Exception("brak połączenia z bazą " + str(e))
        if user_passwd == "None":
            raise Exception("błędny login: " + user)
        elif user_passwd == "UPDATE":
            raise Exception("Musisz zaktualizować aplikację!")
        if password != user_passwd:
            raise Exception("blędne hasło dla: " + user)
        self.base_url = self.base_url + user
        self.url = self.base_url + self.secret

        try:
            with open(heroes_file, 'r') as file:
                driver = []
                action = []
                section = []
                all = []
                heroes = file.read().__add__("\ninny, w sczegółach@K,A,S#").split("\n")
                for hero in heroes:
                    if '@' in hero:
                        types = hero.split("@")[1]
                        if 'A' in types:
                            action.append(hero.split("@")[0])
                        if 'K' in types:
                            driver.append(hero.split("@")[0])
                        if 'S' in types:
                            section.append(hero.split("@")[0])
                        if '#' not in types:
                            all.append(hero.split("@")[0])
                    else:
                        all.append(hero)
                string = "{'heroes': {'action': " + str(action) + ", 'driver': " + str(driver) + ", 'section':" + str(section) + ", 'all':" + str(all) + "}}"
                to_database = json.loads(string.replace("'", '"'))
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print("brak pliku strażacy.txt lub błąd połączenia z bazą " + str(e))
        try:
            with open(passwd_path, 'r') as file:
                string = "{'passwd' : '" + file.readline() + "'}"
                to_database = json.loads(string.replace("'", '"'))
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print("brak pliku hasło_mobile.txt lub błąd połączenia z bazą " + str(e))
        try:
            with open(action_type_file, 'r') as file:
                string = "{'types': " + str(file.read().__add__("\ninny, w sczegółach").split("\n")) + "}"
                to_database = json.loads(string.replace("'", '"'))
                requests.patch(url=self.url, json=to_database)
        except Exception as e:
            print("brak pliku zdarzenia.txt lub błąd połączenia z bazą " + str(e))
        try:
            with open(tmp_file, 'w') as file:
                file.write(str(requests.get(self.url).json()).replace("'", '"').replace('/', "."))
        except Exception as e:
            raise Exception("błąd pobierania danych z bazy " + str(e))
        try:
            with open(tmp_file) as file:
                self.store = json.load(file)
        except Exception as e:
            raise Exception("Baza danych jest pusta " + str(e))

    def get_report(self, uuid_num):
        return self.store[uuid_num]

    def get_all_friendly(self):
        result = []
        ready = []
        for item in self.store:
            if 'deleted' not in item and 'heroes' not in item and 'passwd' not in item and 'types' not in item:
                data = self.store[item]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
                if data["ready"] == "Tak":
                    ready.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":", ""))
        return result, ready

    def get_deleted(self):
        result = []
        for item in self.store:
            if 'deleted' in item and 'heroes' not in item and 'passwd' not in item and 'types' not in item:
                data = self.store[item[8:]]
                result.append(data["innerID"] + "_" + data["location"] + "_" + data["depDate"] + "_" + data['modDate'][11:].replace(":",""))
        return result

    def find_report(self, id_number):
        for item in self.store:
            if 'deleted' not in item and 'heroes' not in item and 'passwd' not in item and 'types' not in item:
                if self.store[item]["innerID"] == id_number:
                    return item
