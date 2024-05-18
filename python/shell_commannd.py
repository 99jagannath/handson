import subprocess
exe = "ps -eaf | grep python"
exe1 = "python"
def process_list():
    ps = subprocess.Popen(exe1, shell=True)
    # ps_pid = ps.pid
    # output = ps.stdout.read().decode()
    # print(output)
    # ps.stdout.close()
    # ps.wait()

    # for line in output.split("\n"):
    #     if line != "" and line != None:
    #         fields = line.split()
    #         pid = fields[0]
    #         print(pid)

process_list()
