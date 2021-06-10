# check https://drive.google.com/file/d/1DgJpJ1I9FXb7Ux3_eD-xekhu7_ZnX0eg/view
# official API documentation

import requests
import urllib3

urllib3.disable_warnings()
import json
from datetime import date


class GreensensApi:
    def __init__(self, username: str, password: str):
        self._user = username
        self._pass = password
        self._host = "https://api.greensens.de/api"
        self.s = requests.Session()
        self._at = None
        self._atd = None
        self._error = "OK"
        self.authenticate()

        self._bearer = f"Bearer {self._at}"
        self._headers = {"Content-Type": "application/json"}
        self._data = None
        # self._hubs = None
        self._sensors = None
        self._num_of_hubs = 0
        self._num_of_sensors = 0

        self.update()
        self.update_sensors()

    def return_is_authenticated(self):
        return (self._at != None)

    def return_last_error(self):
        return self._error

    def return_data(self):
        """Return sensor data"""
        self.update()
        return self._data

    def return_sensors(self):
        """Return sensor data"""
        # self.update()
        self.update_sensors()
        return self._sensors

    def update_sensors(self):
        """Return sensor list"""
        list = []
        if self._data != None:
            for key, value in self._data.items():
                list.append(key)
        self._sensors = list

    def update(self):
        """Update sensor data"""
        self._data = self.get_sensordata()

    ## HTTP REQUEST ##
    def get_sensordata(self):
        if self._at != None:
            """Make a request."""
            url = f"{self._host}/plants"
            self.update_access_token()
            headers = self._headers
            headers["authorization"] = self._bearer
            data = self.s.get(
                url, headers=headers, verify=False, timeout=10
            )
            if data.status_code == 200:
                hubs = data.json()["data"]["registeredHubs"]
                new_data = {}
                self._num_of_hubs = len(hubs)
                self._num_of_sensors = 0
                for hub in hubs:
                    self._num_of_sensors += len(hub["plants"])
                    for sensor in hub["plants"]:
                        new_data[sensor["sensorID"]] = sensor
                self._error = "OK"
                return new_data
            else:
                self._error = f"HTTP error: " + str(data.status_code) + " for " + data.request.url
                return self._data

    ## AUTH ##
    def authenticate(self):
        url = f"{self._host}/users/authenticate"
        payload = json.dumps({"login": self._user, "password": self._pass})
        response = self.s.post(
            url, headers={"Content-Type": "application/json"}, data=payload, timeout=10
        )
        if response.json()["data"] != None:
            token = response.json()["data"]["token"]
            auth_date = date.today()
            self._at = token
            self._atd = auth_date
        else:
            self._error = response.json()["errors"]

    def update_access_token(self):
        if self._at == None:
            self.authenticate()
        tokenage = date.today() - self._atd
        if tokenage.days > 4:
            self.authenticate()

    def return_num_of_hubs(self):
        return self._num_of_hubs

    def return_num_of_sensors(self):
        return self._num_of_sensors

##===============================##
