from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.core.paginator import Paginator
from myadmin.models import Shop, User, Member, Category, Product, Orders, OrderDetail, Payment

# 移动端个人中心

def index(request):
    '''个人中心首页'''
    return render(request,"mobile/member.html")

def orders(request):
    '''浏览会员订单'''
    md = Orders.objects
    mid = request.session['mobileuser']['id']
    orderlist = md.filter(member_id=mid)
    
    status = request.GET.get('status','')
    if status != '':
        orderlist = orderlist.filter(status=status)
        
    orderlist.order_by("-id")
    order_status = ["无", "排队中","已撤销","已完成"]
    for vo in orderlist:
        plist = OrderDetail.objects.filter(order_id=vo.id)[:4]  # 获取前4条
        vo.plist = plist
        vo.statusinfo = order_status[vo.status] #转换订单状态
        
    context = {"orderslist":orderlist}
    return render(request,"mobile/member_orders.html", context)

def detail(request):
    '''浏览会员订单详情'''
    pid = request.GET.get("pid",0)
    order = Orders.objects.get(id=pid)
    plist = OrderDetail.objects.filter(order_id=order.id)
    order.plist = plist
    shop = Shop.objects.only('name').get(id=order.shop_id)
    order.shopname = shop.name
    order_status = ["无", "排队中","已撤销","已完成"]
    order.statusinfo = order_status[order.status]
    return render(request,"mobile/member_detail.html", {"order":order})

def logout(request):
    '''执行会员退出'''
    return render(request,"mobile/register.html")