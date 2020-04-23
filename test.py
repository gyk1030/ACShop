# def a(z=None):
#     print(z)
#
# a(z={1:2})


# a = {'q':1,'w':2}
#
# b = a.pop('z')
# print(b)


def test(data,args):
    a = {}
    a['data'] = data
    if args:
        a[args[0]] = args[1]
    print(a)
    # print(kwargs)

test([1,2,3],args=('a','123'))
