from django.http import JsonResponse

def wrapper_200(data=None, msg="", args=()):
    resp_data = dict()
    resp_data["code"] = 0
    resp_data["msg"] = msg
    if args:
        resp_data[args[0]] = args[1]
    if not data:
        data = {}
    resp_data["data"] = data
    return JsonResponse(resp_data)


def wrapper_400(msg=""):
    resp_data = dict()
    resp_data["code"] = 400
    resp_data["msg"] = msg
    return JsonResponse(resp_data)


def wrapper_500(msg=""):
    resp_data = dict()
    resp_data["code"] = 500
    resp_data["msg"] = msg
    return JsonResponse(resp_data)



