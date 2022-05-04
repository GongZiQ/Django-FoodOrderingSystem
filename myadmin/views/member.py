#会员信息视图文件
from django.shortcuts import render
from django.http import HttpResponse
from django.core.paginator import Paginator
from datetime import datetime
import time
from myadmin.models import Member

# 会员信息浏览
def index(request, pIndex):
    mmod = Member.objects
    mywhere = []
    memberlist = mmod.filter(status__lt = 9)
    
    kw = request.GET.get("keyword", None)
    if kw:
        memberlist = memberlist.filter(nickname__contains = kw)
        mywhere.append("keyword="+kw)
        
    pIndex = int(pIndex)
    page = Paginator(memberlist, 10)
    maxpages = page.num_pages
    
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    plist = page.page_range
    
    #封装信息加载模板输出
    context = {"memberlist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages, 'mywhere':mywhere}
    return render(request,"myadmin/member/index.html",context)
    

# 加载会员信息添加表单
def add(request):
    return render(request, "myadmin/member/add.html")

# 执行信息添加
def insert(request):
    try:
        myfile = request.FILES.get("avatar", None)
        if not myfile:
            context = {"info":"没有上传头像文件！"}
        avatar = str(time.time()) + "." + myfile.name.split(".").pop()
        with open("./static/uploads/member/" + avatar, "wb+") as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
        ob = Member()
        ob.nickname = request.POST["nickname"]
        ob.mobile = request.POST["mobile"]
        ob.status = 1
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.avatar = avatar
        ob.save()
        context = {"info":"添加成功！"}
    except Exception as err:
        print(err)
        context = {"info":"添加失败！"}
    return render(request, "myadmin/info.html", context)

# 删除会员信息
def delete(request, mid=0):
    try:
        ob = Member.objects.get(id=mid)
        ob.status = 9
        ob.save()
        context = {"info":"删除成功！"}
    except Exception as err:
        print(err)
        context = {"info":"删除失败！"}
    return render(request, "myadmin/info.html", context)

# 加载会员信息编辑表单
def edit(request, mid=0):
    try:
        ob = Member.objects.get(id=mid)
        context={"member":ob}
        return render(request, "myadmin/member/edit.html", context)
    except Exception as err:
        print(err)
        context = {"info": "编辑表单加载失败！"}
        return render(request, "myadmin/info.html", context)

# 完成会员编辑
def update(request, mid=0):
    try:
        myfile = request.FILES.get("avatar", None)
        if not myfile:
            context = {"info":"没有上传头像图片！"}
        avatar = str(time.time()) + "." + myfile.name.split(".").pop()
        with open("./static/uploads/member/"+avatar, "wb+") as destination:
            for chunk in myfile.chunks():
                destination.write(chunk)
        ob = Member.objects.get(id=mid)
        ob.nickname = request.POST["nickname"]
        ob.mobile = request.POST["mobile"]
        ob.status = request.POST["status"]
        ob.avatar = avatar
        ob.save()
        context = {"info":"编辑成功！"}
    except Exception as err:
        print(err)
        context = {"info":"编辑失败！"}
    return render(request, "myadmin/info.html", context)