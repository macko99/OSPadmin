import requests
import json


class DataBase:
    base_url = 'https://osptest-3ddc5.firebaseio.com/'
    url = ''
    secret = ''

    def __init__(self, tmp_file):
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
            raise Exception("Błędny login: " + user)
        elif user_passwd == "UPDATE":
            raise Exception("Musisz zaktualizować aplikację!")
        if password != user_passwd:
            raise Exception("blędne hasło dla: " + user)
        self.base_url = self.base_url + user
        self.url = self.base_url + self.secret

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

    def firebase_delete_all(self):
        try:
            for key in self.store:
                if 'heroes' not in key and 'passwd' not in key and 'types' not in key:
                    requests.delete(url=self.base_url + "/" + key + self.secret)
        except Exception as e:
            print("nie udało się usunąć raportów z bazy " + str(e))