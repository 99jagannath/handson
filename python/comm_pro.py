import subprocess

args = ["export TNS_ADMIN=/var/odo/oce/japandit/master/tools/data_plane/python/../../data_plane/atp/DEFAULT202109","sqlplus ADMIN/@DEFAULT202109_tpurgent "]
proc = subprocess.Popen(args, 
                        stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE,
                        shell=True)

proc.stdin.write(b'"Welcome1#123"\n')


stdout, stderr = proc.communicate()
print(stdout)
print(stderr)

with subprocess.Popen(["python"], stdout=subprocess.PIPE,stdin=subprocess.PIPE,shell=True) as proc:
    print("connected")
    stdout, stderr = proc.communicate()
    print(stdout)
    print(stderr)
    print(proc.stdout.read())