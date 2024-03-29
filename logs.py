import os
import requests
import logging

from probe import Probe

class LogInfo(Probe):

    def __init__(self, config):
        super().__init__(config)

    def get_log_file(self):
        if 'send_logs' in self.config:
            logs_data = {}
            for log_path in self.config['send_logs']:
                try:
                    with open(log_path) as log_file:
                        log_text = log_file.read()
                        logs_data[log_path] = log_text
                except:
                    logs_data[log_path] = '<font color="red">ERROR: The client failed to open the file "%s"</font>' % log_path
                r = requests.post(url = self.target + '/logs/send', data = logs_data)
                logging.info(f'Sent conents of the log at {log_path} to the server endpoing located at {self.target}')
        
    def get_file_tree(self):
        # TODO: I don't like the way this is packaged and sent
        tree = ''
        initial_depth = os.getcwd().count(os.path.sep)
        for path, dirs, files in os.walk(os.getcwd()):
            current_depth = path.count(os.path.sep) - initial_depth
            tree += ('<span style="margin-left:%dem">' % current_depth) + path + '<br>'
            for f in files:
                tree += ('<span style="margin-left:%dem">' % (current_depth + 1)) + f + '<br>'
        r = requests.post(url = self.target + '/tree/send', data = { 'tree' : tree })
        logging.info(f'Sent directory and file tree from the clients directory to the server endpoint located at {self.target}')
                
