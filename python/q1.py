from asyncio.windows_events import NULL


def solution(S):
    lines = S.split('\n')
    ans = ''
    l = 10000
    for line in lines:
        words = []
        words.append(line[:6])
        words.append(line[7:10])
        words.append(line[11:])
        if 'root' in words[0] and words[1][0] == 'r' and words[1][1] == '-' and words[1][2] == '-':
            extn = words[2].split('.')[1]
            if extn in ['doc', 'xls', 'pdf']:
                if ans == '' or len(words[2]) < l:
                    ans = words[2]
                    l = len(words[2])
    return l

s = '''
  root r-- jaga.doc
 aroot r-- kj.xls
pcroot rw- k.pdf
'''            
print(solution(s))




