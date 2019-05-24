#_*_coding__*_
# 自定义中间件
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect, HttpResponse, render

class MyAuthMD(MiddlewareMixin):
    # 白名单 一定要有，因为还没有登录，不需要验证是否登录
    white_list = ['/login/', '/register/', '/exist_user/']
    # 黑名单
    black_list = ['/black/']

    def process_request(self, request):
        # 拿到当前访问网址
        next_url = request.path
        if next_url in self.white_list or request.session.get('user'):
            return
        elif next_url in self.black_list:
            return HttpResponse("This is an illegal  URL")
        else:
            return redirect('/login/?next={}'.format(next_url))


