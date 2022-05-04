# 购物车管理视图界面
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from myadmin.models import User, Member, Category, Product, Orders, OrderDetail, Payment
from datetime import datetime
from django.core.paginator import Paginator

# 订单的浏览界面
def index(request, pIndex=1):
    omd = Orders.objects
    shop_id = request.session['shopinfo']['id']
    mywhere = []
    orderlist = omd.filter(shop_id=shop_id)
    
    status = request.GET.get('status','')
    if status != '':
        orderlist = orderlist.filter(status=status)
        mywhere.append("status="+status)
        
    orderlist = orderlist.order_by("-id")
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(orderlist, 10)
    maxpages = page.num_pages
    plist = page.page_range
    if pIndex > maxpages:
        pIndex = maxpages
    elif pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)
    
    for vo in list2:
        if vo.user_id == 0:
            vo.nickname = "无"
        else:
            user = User.objects.only('nickname').get(id=vo.user_id)
            vo.nickname = user.nickname
            
        if vo.member_id == 0:
            vo.nickname = "大堂顾客"
        else:
            mem = Member.objects.only('mobile').get(id=vo.member_id)
            vo.membername = mem.mobile
    #封装信息加载模板输出
    context = {"orderslist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere,'url':request.build_absolute_uri()}
    return render(request,"web/list.html",context)

# 大堂点餐执行添加订单操作
def insert(request):
    try:
        # 执行订单信息添加
        od = Orders()
        od.shop_id = request.session['shopinfo']['id'] # 店铺ID号
        od.member_id = 0 # 会员ID
        od.user_id = request.session['webuser']['id'] # 操作员
        od.money = request.session['total_money']
        od.status = 1  # 订单状态：1过行中/2无效/3已完成
        od.payment_status = 2 # 支付状态：1未支付/2已支付/已退款
        od.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        od.save()
        
        # 执行支付信息添加
        op = Payment()
        op.order_id = od.id  # 订单id号
        op.member_id = 0  # 会员id号
        op.money = request.session['total_money'] #支付款
        op.type = 2 #付款方式：1会员付款/2收银收款
        op.bank = request.GET.get("bank",3) #收款银行渠道:1微信/2余额/3现金/4支付宝
        op.status = 2 #支付状态:1未支付/2已支付/3已退款
        op.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.update_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        op.save()
        
        # 执行订单详情添加
        cartlist = request.session.get('cartlist',{})
        for shop in cartlist.values():
            ov = OrderDetail()
            ov.order_id = od.id
            ov.product_id = shop['id']
            ov.product_name = shop['name']
            ov.price = shop['price']
            ov.quantity = shop['num']
            ov.status = 1
            ov.save()
        del request.session['cartlist']  
        del request.session['total_money']
        return HttpResponse("Y")
        
    except Exception as err:
        print(err)
        context = {"info":"订单添加失败，请稍后再试！"}
        return HttpResponse("N")

# 加载订单详情页
def detail(request):
    oid = request.GET.get("oid",0)
    # 加载订单详情
    dlist = OrderDetail.objects.filter(order_id=oid)
    # 遍历每个商品详情，从Goods中获取对应的图片
    #for og in dlist:
    #    og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

    # 放置模板变量，加载模板并输出
    context = {'detaillist':dlist}
    return render(request,"web/detail.html",context)

# 修改订单状态
def status(request):
    try:
        oid = request.GET.get("oid",'0')
        ob = Orders.objects.get(id=oid)
        ob.status = request.GET['status']
        ob.save()
        return HttpResponse("Y")
    except Exception as err:
        print(err)
        return HttpResponse("N")

