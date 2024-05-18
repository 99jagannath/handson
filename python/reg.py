import re

data = '''
5611:
Could not find recording "japandit_jfr_recordings".

Use JFR.check without options to see list of all available recordings.
'''
data2 = '''
<1- 5611:
Recording: recording=65 name="japandit_jfr_recordings" duration=3m filename="/u01/data/domains/logs/jfr_recordings/serverX.jfr" compress=false (running)
''' 
#result = re.findall('(5611)(.+)((?:\n.+)+)(Use JFR.check without options to see list of all available recordings.)',data)
result = re.search(r'5611.*Use JFR.check without options to see list of all available recordings.', data, re.MULTILINE)
print(result)
rx_sequence=re.compile(r"^(.+?)\n\n((?:[A-Z]+\n)+)",re.MULTILINE)
for match in rx_sequence.finditer(data):
    title, sequence = match.groups()
    title = title.strip()
    sequence = rx_blanks.sub("",sequence)
    print("Title:",title)
    print("Sequence:",sequence)
print(data == data2)
print(data.splitlines()[2])
print(data2.splitlines()[2])