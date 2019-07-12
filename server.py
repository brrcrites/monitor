from flask import Flask, redirect, url_for
import requests
import json

from gcp_status import GCPStatus

app = Flask(__name__)

GCP_STATUS_URL = 'https://status.cloud.google.com/incidents.json'
AWS_STATUS_URL = ''

def request_gcp_status_json():
    r = requests.get(url = GCP_STATUS_URL)
    return json.loads(r.text)

def process_all_gcp_status(gcp_json):
    for incident in gcp_json:
        print(json.dumps(incident, indent=4))

def process_gcp_status(gcp_status_obj):
    if 'begin' in gcp_status_obj and 'end' in gcp_status_obj and 'service_name' in gcp_status_obj and 'severity' in gcp_status_obj:
        return GCPStatus(gcp_status_obj['service_name'], gcp_status_obj['begin'], gcp_status_obj['end'], gcp_status_obj['severity'])
    return None

@app.route('/gcp')
def gcp_incidents_page():
    gcp_statuses = request_gcp_status_json()
    status_objects = []
    for gcp_status in gcp_statuses:
        status = process_gcp_status(gcp_status)
        if status != None:
            status_objects.append(status)
    page = ''
    for index,obj in enumerate(status_objects):
        page += str(obj) + '<br>'
    return '<h1>GCP Incidents</h1>' + page

@app.route('/')
def dashboard():
    return '<a href="%s">GCP Incidents</a>' % url_for('gcp_incidents_page')

