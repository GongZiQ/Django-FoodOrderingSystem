# 自定义中间件类
from django.shortcuts import redirect
from django.urls import reverse

import re

class ShopMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.
        print("ShopMiddleware")

    def __call__(self, request):

        # 获取当前请求路径
        path = request.path
        #print("mycall..."+path)

        # 后台请求路由判断
        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin/login','/myadmin/dologin','/myadmin/logout','/myadmin/verify']
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match(r"^/myadmin",path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))
            
        
        # web前端的登录验证
        if re.match(r"^/web",path):
            # 判断当前用户是否没有登录
            if "webuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('web_login'))
            
        
        
        # 移动端的登录验证
        # 定义网站后台不用登录也可访问的路由url
        mobile_urllist = ['/mobile/register','/mobile/doregister']
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match(r"^/mobile",path) and (path not in mobile_urllist):
            # 判断当前用户是否没有登录
            if "mobileuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('mobile_register'))
        


        # 请求继续执行下去
        response = self.get_response(request)
        # Code to be executed for each request/response after
        # the view is called.
        return response