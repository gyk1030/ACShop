# def a(z=None):
#     print(z)
#
# a(z={1:2})


# a = {'q':1,'w':2}
#
# b = a.pop('z')
# print(b)


# def test(data,args):
#     a = {}
#     a['data'] = data
#     if args:
#         a[args[0]] = args[1]
#     print(a)
#     print(kwargs)
#
# test([1,2,3],args=('a','123'))



import redis

# 普通连接
conn = redis.Redis(host="127.0.0.1", port=6379)
conn.set("x1","hello",ex=5) # ex代表seconds，px代表ms
val = conn.get("x1")
print(val)