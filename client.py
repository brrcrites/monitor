import subprocess
import re
import requests
import json
import argparse

from proc_info import ProcInfo
from logs import LogInfo

parser = argparse.ArgumentParser(description = 'Client for sending monitoring data to central server')
parser.add_argument('--config', type=str, help='Path to the JSON configuration file [required]')
args = parser.parse_args()

if not args.config:
    print('Please provide a config file using the --config flag')
    exit(-1) # TODO: raise an exception here instead

# TODO: clean this up
filehandle = open(args.config,'r')
filestring = filehandle.read()
print(filestring)
config = json.loads(filestring)

info = ProcInfo(config)
print(info.get_num_proc())
print(info.get_utilization())

logs = LogInfo(config)
print(logs.get_log_file())
