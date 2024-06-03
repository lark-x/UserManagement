from django.shortcuts import HttpResponse, redirect
from django.utils.deprecation import MiddlewareMixin


class AuthMiddleware(MiddlewareMixin):
    """ 中间件1 """

    def process_request(self, request):
        # 0.排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL
        if request.path_info in ['/login/', '/image/code/']:
            return
        # 1.读取当前访问的用户的session信息,如果能读到,说明已登录,可以向后执行
        info_dict = request.session.get('info')
        if info_dict:
            return
        # 2.如果没有登录过
        return redirect('/login/')
