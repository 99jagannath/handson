def lcs(str1 , str2):
    m, n = len(str1), len(str2)
    p, c = [0]*(n+1), [0]*(n+1)
    for i in range(1, m+1):
        for j in range(1, n+1):
            if str1[i-1] == str2[j-1]:
                c[j] = 1 + p[j-1]
            else:
                if c[j-1] > p[j]:
                    c[j] = c[j-1]
                else:
                    c[j] = p[j]
        c, p = p, c
    return p[n]

str1 = input()
str2 = input()
str1 = ''.join(sorted(str1))
str2 = ''.join(sorted(str2))
print(lcs(str1, str2))

