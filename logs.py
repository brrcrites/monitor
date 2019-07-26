import os
import requests

class LogInfo:

    def __init__(self, config):
        self.config = config

    def get_log_file(self):
        if 'send_logs' in self.config:
            logs_data = {}
            for log_path in self.config['send_logs']:
                with open(log_path) as log_file:
                    log_text = log_file.read()
                    logs_data[log_path] = log_text
            r = requests.post(url = 'http://127.0.0.1:5000/logs/send', data = logs_data )
            return logs_data
        return None
        