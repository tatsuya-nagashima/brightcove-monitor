import os
import requests
import json
import datetime
import base64
import uuid
from dotenv import load_dotenv
from flask import Flask, send_file, jsonify
from flask_httpauth import HTTPDigestAuth
from brightcove_api import BrightcoveAPI

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

publicDir = os.path.join(os.path.dirname(__file__), "./public")
indexPath = os.path.join(publicDir, 'index.html')
app = Flask(__name__, static_folder=str(publicDir), static_url_path='')
app.config['SECRET_KEY'] = str(uuid.uuid4())

auth = HTTPDigestAuth()
login_list = {USER_ID: PASSWORD}

bc_api = BrightcoveAPI(api_key=API_KEY, client=CLIENT, client_secret=CLIENT_SECRET, account_id=ACCOUNT_ID, video_id=VIDEO_ID, job_id=JOB_ID)

@auth.get_password
def get_pw(id):
    if id in login_list:
        return login_list.get(id)
    return None


@app.route("/")
@auth.login_required
def main():
    return send_file(indexPath)


@app.route('/state', methods=['GET'])
def update_state():
    details = bc_api.get_live_job_details()
    state = details['jobs'][0]['state']

    return jsonify(state=state)


@app.route('/viewers', methods=['GET'])
def update_viewres():
    access_token = bc_api.get_access_token()
    analytics = bc_api.get_analytics(access_token)
    logs = analytics['ccu']['data'][0]["points"][-5:]  # the number of logs = 5

    timestamp = []
    viewers = []
    for log in logs:
        epoc = log["timestamp"]/1000
        jst = datetime.datetime.fromtimestamp(epoc)

        timestamp.insert(0, str(jst))
        viewers.insert(0, log["value"])

    return jsonify(timestamp=timestamp, viewers=viewers)


@app.route('/log/<date>', methods=['GET'])
def download_log(date):
    access_token = bc_api.get_access_token()
    city = bc_api.get_city(access_token, date)
    device_type = bc_api.get_device_type(access_token, date)
    view_time = bc_api.get_view_time(access_token, date)
    unique_user = bc_api.get_unique_user(access_token, date)
    referrer = bc_api.get_referrer(access_token, date)
    search_term = bc_api.get_search_term(access_token, date)
    timeseries = bc_api.get_timeseries(access_token, date)
    timeseries = timeseries['ccu']['data'][0]["points"]

    log = ''
    log += "Total Views" + "," + str(view_time['summary']['video_view']) + "\n"
    log += "Unique Viewers" + "," + str(unique_user['items'][0]['daily_unique_viewers']) + "\n"
    log += "Avg. View Time" + "," + str(view_time['summary']['video_seconds_viewed']/unique_user['items'][0]['daily_unique_viewers']/60) + "\n"
    log += "Total Viewed Minutes" + "," + str(view_time['summary']['video_seconds_viewed']/60) + "\n"
    log += '\n'

    log += "Device_type\n"
    for device in device_type['items']:
        log += device['device_type'] + ',' + str(device['video_view']) + '\n'
    log += '\n'

    log += "City\n"
    for ci in city['items']:
        log += ci['city'] + ',' + str(ci['video_view']) + '\n'
    log += '\n'

    header = "referrer_domain\n"
    log += header
    for ref in referrer['items']:
        log += str(ref['referrer_domain']) + ',' + str(ref['video_view']) + '\n'
    log += '\n'

    log += "search_terms\n"
    for term in search_term['items']:
        searchTerm=str(term['search_terms'])
        videoView=str(term['video_view'])

        log += searchTerm + ',' + videoView + '\n'

    log += '\n'

    log += "Concurrent users\n"
    for ti in timeseries:
        epoc=ti["timestamp"]/1000  # msec => sec
        jst_ymdhms=str(datetime.datetime.fromtimestamp(epoc))
        jst_ymd = jst_ymdhms[:10]
        viewers=str(ti.get("value"))
        if date == jst_ymd:
            log += jst_ymdhms + "," + viewers + "\n"

    return jsonify(log = log)


if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 5000)
