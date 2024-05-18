import subprocess

data = None
pattern ='\'*.py\''
js_dir = '../'
cmd = " find . > %s;" % ( data)
p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)

print(p.communicate())
print(data)