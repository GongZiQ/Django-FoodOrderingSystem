# 店铺信息管理的视图文件
from logging import exception
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import time
import random
from myadmin.models import Shop

# 分页浏览
def index(request, pIndex):
    smod = Shop.objects
    mywhere = []
    shoplist = smod.filter(status__lt=9)
    
    # 获取、判断并封装keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        shoplist = shoplist.filter(name__contain=kw)
        mywhere.append("keyword="+kw)
    
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
        
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(shoplist, 3)  # 以3条每页创建分页
    maxpages = page.num_pages
    
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    
    # 封装信息加载模板
    context = {"shoplist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}
    return render(request, 'myadmin/shop/index.html', context) 

# 加载添加店铺表单
def add(request):
    return render(request, 'myadmin/shop/add.html')

# 执行添加
def insert(request):
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return render(request, "myadmin/info.html", {"info":"没有店铺封面上传文件信息"})
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        with open("./static/uploads/shop/"+cover_pic,"wb+") as destination:
            for chunk in myfile.chunks():      # 分块写入文件  
                destination.write(chunk)  

        # 店铺logo图片的上传处理
        myfile = request.FILES.get("banner_pic",None)
        if not myfile:
            return render(request, "myadmin/info.html", {"info":"没有店铺logo上传文件信息"})
        banner_pic = str(time.time())+"."+myfile.name.split('.').pop()
        with open("./static/uploads/shop/"+banner_pic,"wb+") as destination: 
            for chunk in myfile.chunks():      # 分块写入文件  
                destination.write(chunk)  
        ob = Shop()
        ob.name = request.POST['shopname']
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.address = request.POST['shopaddress']
        ob.phone = request.POST['shopphone']
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"添加成功！"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败！"}
    return render(request, "myadmin/info.html", context)
        

# 店铺删除操作
def delete(request, sid=0):
    try:
        ob = Shop.objects.get(id=sid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败！"}
    return render(request, "myadmin/info.html", context)
        
        
        

# 加载编辑表单
def edit(request, sid=0):
    try:
        ob = Shop.objects.get(id=sid)
        context = {"shop":ob}
        return render(request, "myadmin/shop/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info":"没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)
        

# 执行编辑表单
def update(request, sid=0):
    try:
        # 店铺封面图片的上传处理
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return render(request, "myadmin/info.html", {"info":"没有店铺封面上传文件信息"})
        cover_pic = str(time.time())+"."+myfile.name.split('.').pop()
        with open("./static/uploads/shop/"+cover_pic,"wb+") as destination:
            for chunk in myfile.chunks():      # 分块写入文件  
                destination.write(chunk)  
        
        # 店铺Logo 上传
        myfile = request.FILES.get("banner_pic", None)
        if not myfile:
            return render(request, "myadmin/info.html", {"info":"没有店铺Logo上传文件信息"})
        banner_pic = str(time.time()) + "." + myfile.name.split('.').pop()
        with open("./static/uploads/shop/"+banner_pic, "wb+") as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
                
        ob = Shop.objects.get(id=sid)
        ob.name = request.POST['name']
        ob.phone = request.POST['phone']
        ob.address = request.POST['address']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.cover_pic = cover_pic
        ob.banner_pic = banner_pic
        ob.save()
        context = {"info":"修改成功！"}
    except Exception as err:
        print(err)
        context = {"info":"修改失败！"}
    return render(request, "myadmin/info.html", context)
        