"""pygreensens.py"""
import json
import urllib3
from datetime import date
from .const import *

urllib3.disable_warnings()

class GreenSens():
    
    def __init__(self, username, password, monitored_conditions):
        self._user = username
        self._pass = password
        self._mcond = monitored_conditions
        self._sess = urllib3.PoolManager(cert_reqs = 'CERT_NONE')
        self._token, self._tokendate = self.authenticate()
        self._auth = "Bearer " + self._token
        self._headers = {"Content-Type": "application/json", "Authorization": self._auth}
        self._userdata = None
        self._plantdata = None
        self._notifications = None
        self.fetch_initial_data()
        
        self.hubs = self.get_hubs()
        self.sensors = self.get_sensors()
        self.plants = self.clean_plantdata()

    def fetch_single_plant(self, sensor_id):
        data = self.plants[str(sensor_id)]
        return data

    def get_hubs(self):
        data = self._plantdata
        hubs_list = []
        for item in data:
            hubs_list.append(item["gatewayId"])
        return hubs_list
    def get_sensors(self):
        data = self._plantdata
        sensor_list = []
        for item in data:
            for i in range(len(item['plants'])):
                sensor_list.append(str(item['plants'][i]["sensorID"]))
        return sensor_list
 
    def clean_plantdata(self):
        data = self._plantdata
        plant_dict = {}
        for item in data:
            for i in range(len(item['plants'])):
                plant_dict[str(item['plants'][i]["sensorID"])] = {}
                for p in range(len(self._mcond)):
                    plant_dict[str(item['plants'][i]["sensorID"])][self._mcond[p]] = item['plants'][i][self._mcond[p]]
        return plant_dict




    # CONNECTION TO CLOUD #
    def update(self):
        self.check_tokenage()
        self.update_plantdata()

    def fetch_initial_data(self):
        self.update_plantdata()
        self.update_userdata()
        
    def update_userdata(self):
        self._userdata = self._get(USER_URL)

    def update_plantdata(self):
        self._plantdata = self._get(PLANT_URL)['data']['registeredHubs']

    def check_tokenage(self):
        tokenage = date.today() - self._tokendate
        tokendays = tokenage.days
        if tokendays > 5:
            self._token, self._tokendate = self.authenticate()
        else:
            days = 5 - tokendays
            print(f"Token is still valid for {days} days")
            
    def authenticate(self):
        payload = {"login": self._user, "password": self._pass}
        req_url = USER_URL + "/authenticate"
        j_payload = json.dumps(payload)
        r = self._sess.request('POST', req_url, headers={"Content-Type": "application/json"}, body=j_payload)
        token = json.loads(r.data.decode('utf-8'))['data']['token']
        auth_date = date.today()
        return token, auth_date

    def _post(self, url, payload={}):
        r_url = url
        if item:
            r_url = url + item
        j_payload = json.dumps(payload)
        r = self._sess.request('POST', r_url, headers=self._headers, body=j_payload)
        data = json.loads(r.data.decode('utf-8'))
        return(data)    

    def _get(self, url, item=None):
        r_url = url
        if item:
            r_url = url + item
        r = self._sess.request('GET', r_url, headers=self._headers)
        data = json.loads(r.data.decode('utf-8'))
        return(data)
