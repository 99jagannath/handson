
# import tempfile
# import os

# tmp = tempfile.NamedTemporaryFile(mode='w+t', prefix='jagannath_',suffix='.sh',dir='./')
# print(tmp.name)
# try:
#   # tmp.write("ls -al\n")
#   # tmp.write('python')
#   # cmd="sh %s" % tmp.name
#   # print(tmp.read())
#   # print(cmd)
#   os.system("python")

# finally:
#   tmp.close()
#   if(os.path.exists(tmp.name) == False):
#     print('File is removed')
import subprocess

cmd = "python"
subprocess.call("export a=1;echo a", shell=True)
returned_value = subprocess.call("echo $a")  # returns the exit code in unix
print('returned value:', returned_value)