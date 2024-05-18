from collections import namedtuple

t = namedtuple( "Test", ['x','y', 'u'] )


print(type(t))
print(t(1,2,3).x)