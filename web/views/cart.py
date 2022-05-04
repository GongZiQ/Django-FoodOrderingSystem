# 购物车管理视图界面
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product

def add(request, pid):
    """向购物车中添加商品"""
    # 从session中获取所有的菜品信息，并从中提取需要放入购物车的菜品信息
    product = request.session['productlist'][pid]
    product["num"] = 1
    cartlist = request.session.get('cartlist', {})
    if pid in cartlist:
        cartlist[pid]["num"] += product["num"]
    else:
        cartlist[pid] = product
    
    # 将cartlist存入session
    request.session['cartlist'] = cartlist
    print(cartlist)
    
    # 跳转到点餐首页
    return redirect(reverse('web_index'))
    

def delete(request, pid):
    """在购物车中删除商品"""
    cartlist = request.session.get('cartlist', {})
    del cartlist[pid]
    # 将cartlist存入session
    request.session['cartlist'] = cartlist
    # 跳转到点餐首页
    return redirect(reverse('web_index'))
    

def clear(request):
    """清空购物车"""
    request.session['cartlist'] = {}
    # 跳转到点餐首页
    return redirect(reverse('web_index'))

def change(request):
    """更改购物车信息"""
    cartlist = request.session.get('cartlist', {})
    pid = request.GET.get("pid", 0)  # 得到菜品序号
    m = int(request.GET.get("num", 1))
    if m < 1:
        m = 1
    cartlist[pid]["num"] = m
    request.session['cartlist'] = cartlist
    return redirect(reverse('web_index'))
