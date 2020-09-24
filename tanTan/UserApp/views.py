from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

# Create your views here.
from UserApp.logics import send_vcode
from UserApp.models import Users


# 发送手机短信验证码
def fetchVcode(request):
    phonenum = request.GET.get('phonenum')
    data = {'data': None, }
    if send_vcode(phonenum=phonenum):
        data['code'] = 0
    else:
        data['code'] = 1000
    return JsonResponse(data=data)


# 接收并验证用户提交的手机短信验证码
def submitVcode(request):
    data = {}
    vcode = request.POST.get('vcode')
    phonenum = request.POST.get('phonenum')
    cache_code = cache.get('sendvcode_%s' % phonenum)
    if vcode and vcode == cache_code:
        data['code'] = 0
        try:
            user = Users.objects.get(phonenum=phonenum)
            data['data'] = user.user()
        except:
            user = Users.objects.create(nickname=phonenum, phonenum=phonenum)
            data['data'] = user.userInfo()
        request.session['uid'] = user.id
    else:
        data['code'] = 1001
        data['data'] = '验证码错误'
    return JsonResponse(data=data)


def showProfile(request):

    return HttpResponse('登录成功')


def updateProfile(request):
    return None
