from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin


class AuthLogin(MiddlewareMixin):
    white_list= ['/api/user/vcode/fetch/','/api/user/vcode/submit/' ]

    def process_request(self, request):
        if request.path in self.white_list:
            return
        if not request.session.get('uid'):
            return JsonResponse({'code': 1002, 'data': '用户未登录'})
