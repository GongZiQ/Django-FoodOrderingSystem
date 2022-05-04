# 购物车管理视图界面
from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product

def add(request):
    """向购物车中添加商品"""
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get("pid", None)
    if pid:
        product = Product.objects.get(id=pid).toDict()
        product["num"] = 1
        # 菜的数量操作
        if pid in cartlist:
            cartlist[pid]["num"] += product["num"]
        else:
            cartlist[pid] = product
    
        # 将cartlist存入session
        request.session['cartlist'] = cartlist
    
    # 响应json格式的购物车信息
    return JsonResponse({'cartlist':cartlist})
    

def delete(request, pid):
    """在购物车中删除商品"""
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    # 将cartlist存入session
    request.session['cartlist'] = cartlist
    # 响应json格式的购物车信息
    return JsonResponse({'cartlist':cartlist})
    

def clear(request):
    """清空购物车"""
    request.session['cartlist'] = {}
    # 跳转到点餐首页
    return JsonResponse({'cartlist':{}})

def change(request):
    """更改购物车信息"""
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get("pid", 0)  # 得到菜品序号
    m = int(request.GET.get("num", 1))
    if m < 1:
        m = 1
    cartlist[pid]["num"] = m
    request.session['cartlist'] = cartlist
    return JsonResponse({'cartlist':cartlist})
