import math
def egyptian(nu, den, unitDenos):
    if nu == 0:
        return
    newDeno = math.ceil(den/nu)

    unitDenos.append(newDeno)

    egyptian(nu *newDeno - den, den * newDeno, unitDenos)

ans = []
egyptian(6,14, ans)

print(ans)