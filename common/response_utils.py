from django.http import JsonResponse

def wrapper_200(data=None, msg=""):
    resp_data = dict()
    resp_data["status"] = 200
    resp_data["msg"] = msg
    if not data:
        data = {}
    resp_data["data"] = data
    return JsonResponse(resp_data)


def wrapper_400(msg=""):
    resp_data = dict()
    resp_data["status"] = 400
    resp_data["msg"] = msg
    return JsonResponse(resp_data)


def wrapper_500(msg=""):
    resp_data = dict()
    resp_data["errCode"] = 500
    resp_data["errMsg"] = msg
    return JsonResponse(resp_data)



