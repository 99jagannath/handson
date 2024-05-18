rv = [1, 0, -1, 0]
cv = [0, 1, 0, -1]
ans = 1000000
def path_finder(cr,cc,r,c,mat,cnt):
    if cr <=0 or cr >= (r-1) or cc <= 0 or cc>=(c-1):
        ans = min (ans,cnt)
        return
    for k in range(4):
        cr = cr + rv[k]
        cc = cc + cv[k]
        if(mat[cr][cv]=='.'):
            mat[cr][cv] = '#'
            path_finder(cr,cc,r,c,mat,cnt+1)
r = int(input())
c = int(input())
cr = int(input())
cc = int(input())
mat = [r][c]
for i in range(r):
    for j in range(c):
        mat[i][j] = input()

path_finder(cr,cc,r,c,mat,0)

print(ans)
