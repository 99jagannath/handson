import subprocess
import tempfile
import os
file = 'file_list'
data = os.path.join(tempfile.gettempdir(), file)
cmd = "cd ./js_tut; find . >> %s; find ./js_tut >> %s" % (data,data)
p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=True)
print(p.communicate())