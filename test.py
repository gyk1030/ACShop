
# def a(z=None):
#     print(z)
#
# a(z={1:2})


# a = {'q':1,'w':2}
#
# b = a.pop('z')
# print(b)


def test(a=()):
    res = dict()
    res[a[0]] = a[1]
    print(res)

test(a=(1,2))