# Author:gyk
from django.shortcuts import redirect
from ac_user.models import UserInfo


#
# # 获取用户名名及用户对象
# def get_user(request):
#     print(':::',request)
#     user_id = request.session.get('_auth_user_id',None)
#     user = UserInfo.objects.filter(pk=user_id,isDelete=False).first()
#     return user
#
# def Authenticate(request):
#     user = request.user
#     print('///////',user)
#     if not user.is_authenticated:
#         # print('6666')
#         return redirect('/login/')
#
#     return get_user(request)