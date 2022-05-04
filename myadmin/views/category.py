# 菜品分类的视图文件
from logging import exception
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.core.paginator import Paginator
from datetime import datetime
import time
import random
from myadmin.models import Shop, Category

# 分页浏览
def index(request, pIndex):
    cmod = Category.objects
    mywhere = []
    clist = cmod.filter(status__lt=9)
    
    # 获取、判断并封装keyword键搜索
    kw = request.GET.get("keyword", None)
    if kw:
        clist = clist.filter(name__contain=kw)
        mywhere.append("keyword="+kw)
        
    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status', '')
    if status != '':
        clist = clist.filter(status=status)
        mywhere.append("status="+status)
        
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(clist, 10)  # 以10条每页创建分页
    maxpages = page.num_pages
    
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    
    #遍历信息，并获取对应的商铺名称，以shopname名封装
    for vo in list2:
        sob = Shop.objects.get(id=vo.shop_id)
        vo.shopname = sob.name  # 这里的信息对象可以追加信息/属性
    # 封装信息加载模板
    context = {"categorylist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}
    return render(request, 'myadmin/category/index.html', context)

def loadCategory(request,sid):
    clist = Category.objects.filter(status__lt=9,shop_id=sid).values("id","name")
    #返回QuerySet对象，使用list强转成对应的菜品分类列表信息
    return JsonResponse({'data':list(clist)})
    

# 加载添加表单
def add(request):
    slist = Shop.objects.values("id", "name")
    context={"shoplist":slist}
    return render(request, 'myadmin/category/add.html', context)

# 执行添加
def insert(request):
    try:
        ob = Category()
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败"}
    return render(request,"myadmin/info.html",context)

# 菜品删除
def delete(request, cid=0):
    try:
        ob = Category.objects.get(id=cid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"删除成功！"}
    except Exception as err:
        print(err)
        context={"info":"删除失败"}

    return JsonResponse(context)

# 加载菜品编辑表单
def edit(request, cid=0):
    try:
        ob = Category.objects.get(id=cid)
        slist = Shop.objects.values("id","name")
        context={"category":ob,"shoplist":slist}
        return render(request,"myadmin/category/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)

# 执行菜品编辑
def update(request, cid=0):
    try:
        ob = Category.objects.get(id=cid)
        ob.shop_id = request.POST['shop_id']
        ob.name = request.POST['name']
        #ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)