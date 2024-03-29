import subprocess
import re
import requests
import logging

from probe import Probe

class ProcInfo(Probe):

    def __init__(self, config):
        super().__init__(config)

    def get_num_proc(self):
        # For Mac/FreeBSD only probably, one sample and no columns to only get global info
        proc = subprocess.Popen(['top','-l','1','-n','0'], stdout=subprocess.PIPE)
        top_output = proc.stdout.read().decode('utf-8')
        # Looking for 0-9 any number of times followed by a space and the word 'total'
        pattern = re.compile('[0-9]+\stotal')
        num_processes_string = pattern.search(top_output)
        # Take the result (we should check we have one) and then split it at the space
        num_processes, total_string = num_processes_string.group().split(' ')
        r = requests.post(url = self.target + '/processes/send', data = { 'num_proc': num_processes } )
        logging.info(f'Sent number of processes {num_processes} to the server endpoing located at {self.target}')

    def get_utilization(self):
        proc = subprocess.Popen(['top','-l','1','-n','0'], stdout=subprocess.PIPE)
        top_output = proc.stdout.read().decode('utf-8')

        pattern = re.compile('[0-9]+\%\suser')
        user_utilization_string = pattern.search(top_output)
        user_utilization, total_string = user_utilization_string.group().split('%')

        pattern = re.compile('[0-9]+\%\ssys')
        system_utilization_string = pattern.search(top_output)
        system_utilization, total_string = system_utilization_string.group().split('%')

        pattern = re.compile('[0-9]+\%\sidle')
        idle_utilization_string = pattern.search(top_output)
        idle_utilization, total_string = idle_utilization_string.group().split('%')

        util_info = { 'user_util': user_utilization, 'system_util': system_utilization, 'idle_util': idle_utilization }
        r = requests.post(url = self.target + '/utilization/send', data = util_info )
        logging.info(f'Sent the utilization values {user_utilization} (user), {system_utilization} (system), {idle_utilization} (idle) to the server endpoing located at {self.target}')
