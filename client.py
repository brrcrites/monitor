import subprocess
import re

def get_current_top():
    # For Mac/FreeBSD only probably, one sample and no columns to only get global info
    proc = subprocess.Popen(['top','-l','1','-n','0'], stdout=subprocess.PIPE)
    top_output = proc.stdout.read().decode('utf-8')
    print(top_output)
    # Looking for 0-9 any number of times followed by a space and the word 'total'
    pattern = re.compile('[0-9]+\stotal')
    num_processes_string = pattern.search(top_output)
    # Take the result (we should check we have one) and then split it at the space
    num_processes, total_string = num_processes_string.group().split(' ')
    print(num_processes)

get_current_top()
