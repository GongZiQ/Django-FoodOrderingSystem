from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.urls import reverse
from myadmin.models import User, Shop, Category, Product

def index(request):
    # return HttpResponse('欢迎进入大堂点餐前台首页！')
    return redirect(reverse('web_index'))

def webindex(request):
    cartlist = request.session.get('cartlist', {})
    total_money = 0
    # request.session["total_money"] = total_money
    for vo in cartlist.values():
        total_money += vo["num"] * vo["price"]
    request.session["total_money"] = total_money
    context = {"categorylist":request.session.get("categorylist", {}).items()}
    return render(request, "web/index.html", context)

# 加载登录表单
def login(request):
    shoplist = Shop.objects.filter(status=1)
    context = {"shoplist":shoplist}
    return render(request, "web/login.html", context)

# 提交登录表单
def dologin(request):
    try:
        if request.POST["shop_id"] == "0":
            return redirect(reverse('web_login')+"?typeinfo=1")  # 直接重定向
        if request.POST["code"] != request.session['verifycode']:
            # context = {"info":"验证码不正确！"}
            return redirect(reverse('web_login')+"?typeinfo=2")  # 直接重定向
        user = User.objects.get(username=request.POST['username'])
        if user.status == 6 or user.status == 1:
            import hashlib
            md5 = hashlib.md5()
            n = user.password_salt
            s = request.POST['pass'] + str(n)
            md5.update(s.encode('utf-8'))
            if user.password_hash == md5.hexdigest():
                request.session['webuser'] = user.toDict()
                
                # 获取当前店铺信息
                shopob = Shop.objects.get(id=request.POST["shop_id"])
                request.session["shopinfo"] = shopob.toDict()
                
                # 获取菜品类别和菜品信息
                clist = Category.objects.filter(shop_id=shopob.id, status=1)
                categorylist = dict()
                productlist = dict()
                for vo in clist:
                    c = {"id":vo.id, "name":vo.name, "pids":[]}
                    plist = Product.objects.filter(category_id=vo.id, status=1)
                    for p in plist:
                        c['pids'].append(p.toDict())
                        productlist[p.id] = p.toDict()
                    categorylist[vo.id] = c
                    
                # 将上面的结果放入session
                request.session['categorylist'] = categorylist
                request.session['productlist'] = productlist
                
                return redirect(reverse('web_index'))
            else:
                return redirect(reverse('web_login')+"?typeinfo=5")  # 直接重定向
        else:
            return redirect(reverse('web_login')+"?typeinfo=4")  # 直接重定向
    except Exception as err:
        print(err)
        return redirect(reverse('web_login')+"?typeinfo=3")  # 直接重定向

# 退出管理员登录
def logout(request):
    del request.session['webuser']
    return redirect(reverse('web_login'))

# 验证码
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')

# Create your views here.
