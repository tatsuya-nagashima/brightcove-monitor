import os
import base64
import requests
import datetime
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)
USER_ID = os.environ.pop('USER_ID')
PASSWORD = os.environ.pop('PASSWORD')
API_KEY = os.environ.pop('API_KEY')
CLIENT = os.environ.pop('CLIENT')
CLIENT_SECRET = os.environ.pop('CLIENT_SECRET')
ACCOUNT_ID = os.environ.pop('ACCOUNT_ID')
VIDEO_ID = os.environ.pop('VIDEO_ID')
JOB_ID = os.environ.pop('JOB_ID')


class BrightcoveAPI():

    def __init__(self, api_key, client, client_secret, account_id, video_id, job_id):
        self.api_key = api_key
        self.client = client
        self.client_secret = client_secret
        self.account_id = account_id
        self.video_id = video_id
        self.job_id = job_id

    def get_access_token(self):
        url = "https://oauth.brightcove.com/v4/access_token"
        params = "grant_type=client_credentials"
        authString = str(base64.b64encode(self.client+":"+self.client_secret))
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Authorization': 'Basic ' + authString}

        res = requests.post(url, headers=headers, params=params)
        access_token = res.json()['access_token']

        return access_token

    def get_city(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "city",
            "fields": "video_view",
            "limit": 500,
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_device_type(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "device_type",
            "fields": "video_view",
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_view_time(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "player",
            "fields": "video_seconds_viewed,video_impression",
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_unique_user(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "date",
            "fields": "daily_unique_viewers",
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_referrer(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "referrer_domain",
            "fields": "referrer_domain",
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_search_term(self, access_token, date):
        url = 'https://analytics.api.brightcove.com/v1/data'
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "accounts": self.account_id,
            "dimensions": "search_terms",
            "fields": "search_terms",
            "from": date,
            "to": date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_timeseries(self, access_token, date):
        year = date.split("-")[0]
        month = date.split("-")[1]
        day = str(int(date.split("-")[2]) + 1)
        to_date = year + "-" + month + "-" + day

        url = "https://analytics.api.brightcove.com/v1/timeseries/accounts/" + self.account_id
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "dimensions": "video",
            "where": "video=="+self.video_id,
            "metrics": "ccu",
            "bucket_duration": "1m",
            "from": date,
            "to": to_date
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_analytics(self, access_token):

        url = "https://analytics.api.brightcove.com/v1/timeseries/accounts/" + self.account_id
        headers = {
            'Content-Type': "application/json",
            'Authorization': "Bearer " + access_token,
            'Accept-Encoding': "gzip"
        }
        params = {
            "dimensions": "video",
            "where": "video==" + self.video_id,
            "metrics": "ccu",
            "bucket_duration": "1m"
        }

        res = requests.get(url, headers=headers, params=params)
        return res.json()

    def get_live_job_details(self):
        url = "https://api.bcovlive.io/v1/jobs/"
        headers = {'Content-Type': "application/json", 'x-api-key': self.api_key}
        params = {"job_id": self.job_id}
        res = requests.get(url, headers=headers, params=params)

        return res.json()


if __name__ == "__main__":

    bc_api = BrightcoveAPI(api_key=API_KEY, client=CLIENT, client_secret=CLIENT_SECRET, account_id=ACCOUNT_ID, video_id=VIDEO_ID, job_id=JOB_ID)

    access_token = bc_api.get_access_token()
    print bc_api.get_timeseries(access_token, "2020-04-10")
