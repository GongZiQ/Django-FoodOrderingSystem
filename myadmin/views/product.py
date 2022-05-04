from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator
from datetime import datetime
import time,os

from myadmin.models import Product, Shop, Category

# 浏览菜品信息
def index(request, pIndex):
    pmod = Product.objects
    mywhere = []
    productlist = pmod.filter(status__lt=9)
    
    # 获取、判断并封装keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        productlist = productlist.filter(name__contain=kw)
        mywhere.append("keyword="+kw)
        
    # 获取、判断并封装状态status搜索
    status = request.GET.get('status', '')
    if status != '':
        productlist = productlist.filter(status=status)
        mywhere.append("status=" + status)
    
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(productlist, 10)
    maxpages = page.num_pages
    
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
        
    list2 = page.page(pIndex)
    plist = page.page_range
    
    for vo in list2:
        vo.shopname = Shop.objects.get(id=vo.shop_id).name
        vo.categoryname = Category.objects.get(id=vo.category_id).name
    
    # 封装信息加载模板
    context = {"productlist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}
    return render(request, "myadmin/product/index.html", context)

# 加载菜品添加表单
def add(request):
    slist = Shop.objects.values("id", "name")
    context = {"shoplist":slist}
    return render(request, "myadmin/product/add.html", context)

# 执行菜品添加
def insert(request):
    try:
        myfile = request.FILES.get("cover_pic", None)
        if not myfile:
            return render(request,"myadmin/info.html", {"info":"没有封面上传文件！"})
        cover_pic = str(time.time()) + "."+myfile.name.split(".").pop()
        with open("./static/uploads/product/" + cover_pic, "wb+") as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
        ob = Product()
        ob.shop_id = request.POST['shop_id']
        ob.category_id = request.POST['category_id']
        ob.name = request.POST['name']
        ob.price = request.POST['price']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.cover_pic = cover_pic
        ob.save()
        context = {"info":"添加成功！"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败！"}
    return render(request, "myadmin/info.html", context)

# 删除菜品
def delete(request, pid=0):
    try:
        ob = Product.objects.get(id=pid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    return render(request, "myadmin/info.html", context)

# 加载编辑表单
def edit(request, pid=0):
    try:
        ob = Product.objects.get(id=pid)
        slist = Shop.objects.values("id", "name")
        context = {"product":ob, "shoplist":slist}
        return render(request, "myadmin/product/edit.html",context)
    except Exception as err:
        print(err)
        context = {"info":"没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)

# 执行编辑表单
def update(request, pid=0):
    try:
        # 封面图片的上传
        myfile = request.FILES.get("cover_pic",None)
        if not myfile:
            return render(request, "myadmin/info.html", context)
        cover_pic = str(time.time()) + "." +myfile.name.split('.').pop()
        with open("./static/uploads/product/"+cover_pic, "wb+") as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
        ob = Product.objects.get(id=pid)
        ob.shop_id = request.POST["shop_id"]
        ob.category_id = request.POST["category_id"]
        ob.cover_pic = cover_pic
        ob.name = request.POST["name"]
        ob.price = request.POST["price"]
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.status = request.POST["status"]
    except Exception as err:
        print(err)
        context = {"info":"没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)
        

