from django.http import JsonResponse, HttpResponse
from django.core.cache import cache

# Create your views here.
from UserApp.logics import send_vcode
from UserApp.models import Users, Profile
from tanTan.forms import UsersForm
from tanTan.forms import ProfileForm


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


# 查看个人资料
def showProfile(request):
    uid = request.session.get('uid')
    profile, create = Profile.objects.get_or_create(id=uid)
    return JsonResponse(data={'code': 0, 'data': profile.to_dict()})


def updateProfile(request):
    user_form = UsersForm(request.POST)
    profile_form = ProfileForm(request.POST)
    if user_form.is_valid() and profile_form.is_valid():
        uid = request.session['uid']
        Users.objects.update_or_create(id=uid,defaults=user_form.cleaned_data)
        Profile.objects.update_or_create(id=uid,defaults=profile_form.cleaned_data)
        return JsonResponse(data={'code': 0, 'data': None})
    else:
        err = {}
        err.update(user_form.errors)
        err.update(profile_form.errors)
        return JsonResponse(data={'code': 1003, 'data': err})
