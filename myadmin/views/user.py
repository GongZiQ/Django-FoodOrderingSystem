# 员工信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.db.models import Q  # 用于封装或条件
from django.core.paginator import Paginator  # 分页用
from datetime import datetime
import random
from myadmin.models import User


def index(request,pIndex):
    """浏览信息"""
    umod = User.objects
    mywhere=[]
    ulist = umod.filter(status__lt=9)

    # 获取、判断并封装关keyword键搜索
    kw = request.GET.get("keyword",None)
    if kw:
        # 查询员工账号或昵称中只要含有关键字的都可以
        ulist = ulist.filter(Q(username__contains=kw) | Q(nickname__contains=kw))
        mywhere.append("keyword="+kw)

    # 获取、判断并封装状态status搜索条件
    status = request.GET.get('status','')
    if status != '':
        ulist = ulist.filter(status=status)
        mywhere.append("status="+status)
        
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(ulist, 5)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    
    # p判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    
    # 封装信息加载模板
    context= {"userlist":list2, 'plist':plist, 'pIndex':pIndex, 'maxpages':maxpages, 'mywhere':mywhere}

    return render(request, 'myadmin/user/index.html', context)

def add(request):
    """加载信息添加表单"""
    return render(request, "myadmin/user/add.html")

def insert(request):
    """执行信息添加"""
    try:
        ob = User()
        ob.username = request.POST["username"]
        ob.nickname = request.POST["nickname"]
        
        # 获取密码并MD5
        import hashlib
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password']+str(n)
        
        md5.update(s.encode('utf-8'))
        ob.password_hash = md5.hexdigest()
        ob.password_salt = n
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"添加成功！"}
    except Exception as err:
        print(err)
        context={"info":"添加失败！"}
    return render(request, "myadmin/info.html", context)

def delete(request, uid=0):
    """执行信息删除"""
    try:
        ob = User.objects.get(id=uid)
        ob.status = 9
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    # return JsonResponse(context)
    return render(request, "myadmin/info.html", context)

def edit(request, uid=0):
    """加载信息编辑表单"""
    try:
        ob = User.objects.get(id=uid)
        context={"user":ob}
        return render(request,"myadmin/user/edit.html",context)
    except Exception as err:
        context={"info":"没有找到要修改的信息！"}
        return render(request,"myadmin/info.html",context)
    

def update(request, uid):
    """执行信息编辑"""
    try:
        ob = User.objects.get(id=uid)
        ob.nickname = request.POST['nickname']
        ob.status = request.POST['status']
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.save()
        context={"info":"修改成功！"}
    except Exception as err:
        print(err)
        context={"info":"修改失败"}
    return render(request,"myadmin/info.html",context)