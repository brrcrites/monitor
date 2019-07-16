import subprocess
import re
import requests

from proc_info import ProcInfo

info = ProcInfo()
print(info.get_num_proc())
print(info.get_utilization())

