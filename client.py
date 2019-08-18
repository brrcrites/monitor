import subprocess
import re
import requests
import json
import argparse
import logging

from proc import ProcInfo
from logs import LogInfo

def parse_config_json(config_location):
    # TODO: validate the input config against a schema
    try:
        fd = open(config_location,'r')
        file_str = fd.read()
    except:
        print('The config file located at "%s" failed to open or read' % config_location)
        exit(-1) # TODO: raise an exception here instead
    try:
        file_json = json.loads(file_str)
    except:
        print('The config file located at "%s" failed to parse as valid JSON' % config_location)
        exit(-1) # TODO: raise an exception here instead
    if 'log' in file_json:
        logging.basicConfig(filename=file_json['log'], level=logging.INFO)
    else:
        logging.basciConfig(filename='probe.log', level=logging.INFO)
    return file_json

parser = argparse.ArgumentParser(description = 'Client for sending monitoring data to central server')
parser.add_argument('--config', type=str, help='Path to the JSON configuration file [required]', required=True)
args = parser.parse_args()

config = parse_config_json(args.config)

# TODO: Need to figure out a systematic way to generate the correct probes based on the config
info = ProcInfo(config)
info.get_num_proc()
info.get_utilization()

logs = LogInfo(config)
logs.get_log_file()
logs.get_file_tree()
