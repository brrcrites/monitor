from flask import Flask, redirect, url_for, request, session
import requests
import json

from gcp_status import GCPStatus

app = Flask(__name__)
app.secret_key = 'terrible secret key' # Needed for using sessions

num_proc = 0
user_util = 0
system_util = 0
idle_util = 0
logs_array = {}

GCP_STATUS_URL = 'https://status.cloud.google.com/incidents.json'
AWS_STATUS_URL = ''

# TODO: we should build a basic page that has the data pushed into it rather than appending the button each time
def append_main_menu_button(page):
    return page + '<br><br><a href="%s">Main Menu</a>' % url_for('dashboard')

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
    return append_main_menu_button('<h1>GCP Incidents</h1>' + page)

@app.route('/processes/send', methods = ['POST'])
def processes_page():
    global num_proc
    num_proc = int(request.form['num_proc'])
    print('Number processes: %d' % num_proc)
    return ''

@app.route('/utilization/send', methods = ['POST'])
def utilization_page():
    global user_util, system_util, idle_util
    user_util = int(request.form['user_util'])
    system_util = int(request.form['system_util'])
    idle_util = int(request.form['idle_util'])
    print('%% user utilizations: %d\n%% system utilization: %d\n%% idle utilization: %d' % (user_util, system_util, idle_util))
    return ''

@app.route('/logs/send', methods = ['POST'])
def logs_page():
    global logs_array
    for log_path, log_text in request.form.items():
        logs_array[log_path] = log_text
    return ''

@app.route('/dashboard')
def processes_dashboard():
    global num_proc, user_util, system_util, idle_util
    return append_main_menu_button('Client currently has %d processes running<br>%% user utilizations: %d<br>%% system utilization: %d<br>%% idle utilization: %d' % (num_proc, user_util, system_util, idle_util))

@app.route('/logs')
def logs_dashboard():
    global logs_array
    logs_page = ''
    if len(logs_array) > 0:
        for log_path, log_text in logs_array.items():
            logs_page += '>>> %s<br><br>' % log_path
            logs_page += '%s<br><br>' % log_text
    else:
        logs_page = 'No Logs have been received'
    return append_main_menu_button(logs_page)

@app.route('/')
def dashboard():
    page = '<a href="%s">GCP Incidents</a><br>' % url_for('gcp_incidents_page')
    page += '<a href="%s">Dashboard</a><br>' % url_for('processes_dashboard')
    page += '<a href="%s">Logs</a><br>' % url_for('logs_dashboard')
    return page

