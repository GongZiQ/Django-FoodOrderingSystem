#订单信息视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
import time
from myadmin.models import Member, Order


# 浏览订单
def index(request, pIndex):
    omod = Order.objects
    order_list = omod.filter(status__lt=9)
    kw = request.GET.get("keyword", None)
    mywhere =[]
    if kw:
        order_list = order_list.filter(order_id=kw)
        mywhere.append("keyword="+kw)
    
    pIndex = int(pIndex)
    page = Paginator(order_list,10)
    maxpages = page.num_pages
    list2 = page.page(pIndex)
    plist = page.page_range
    
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
        
    context = {"orderlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages, 'mywhere':mywhere}
    return render(request, "myadmin/order/index.html", context)