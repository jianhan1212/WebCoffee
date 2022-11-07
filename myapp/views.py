from django.shortcuts import render
from urllib import request
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import authenticate
from django.contrib import auth
from myapp import models


cartlist = []  #購買商品串列

# Create your views here.
def index(request):
    return render(request,'index.html',locals())


def contact(request):
    return render(request,'contact.html',locals())

def menu(request):
    return render(request,'menu.html',locals())

def news(request):
    return render(request,'news.html',locals())

def order(request):
    global cartlist
    total = 0
    if 'cartlist' in request.session:
        cartlist = request.session['cartlist']
    else:
        cartlist=[]

    cartnum = len(cartlist)
    productall = models.ProductModel.objects.all()

    for unit in cartlist:
        total += int(unit[3])
    grandtotal = int(total +(total*0.10))
    return render(request,'order.html',locals())

def cart(request):  #顯示購物車
    global cartlist
    cartlist1 = cartlist  #以區域變數傳給模版
    total = 0
    for unit in cartlist:  #計算商品總金額
        total += int(unit[3])
    servicecharge = int(total*0.10) #服務費
    grandtotal = int(total+servicecharge)  #總金額
    print(cartlist)
    return render(request,"cart.html",locals())

def addtocart(request, ctype=None, productid=None):
	global cartlist
	if ctype == 'add':  #加入購物車
		product = models.ProductModel.objects.get(id=productid)
		flag = True  #設檢查旗標為True
		for unit in cartlist:  #逐筆檢查商品是否已存在
			if product.pname == unit[0]:  #商品已存在
				unit[2] = str(int(unit[2])+ 1)  #數量加1
				unit[3] = str(int(unit[3]) + product.pprice)  #計算價錢
				flag = False  #設檢查旗標為False
				break
		if flag:  #商品不存在
			temlist = []  #暫時串列
			temlist.append(product.pname)  #將商品資料加入暫時串列
			temlist.append(str(product.pprice))  #商品價格
			temlist.append('1')  #先暫訂數量為1
			temlist.append(str(product.pprice))  #總價
			cartlist.append(temlist)  #將暫時串列加入購物車           
		request.session['cartlist'] = cartlist  #購物車寫入session 
		return redirect('/order/')
                    
	elif ctype == 'update':  #更新購物車
		n = 0
		for unit in cartlist:
			unit[2] = request.POST.get('qty' + str(n), '1')  #取得數量
			unit[3] = str(int(unit[1]) * int(unit[2]))  #取得總價
			n += 1
		request.session['cartlist'] = cartlist
		return redirect('/cart/')
	elif ctype == 'empty':  #清空購物車
		cartlist = []  #設購物車為空串列
		request.session['cartlist'] = cartlist
		return redirect('/order/')
	elif ctype == 'remove':  #刪除購物車中商品
		del cartlist[int(productid)]  #從購物車串列中移除商品
		request.session['cartlist'] = cartlist
		return redirect('/cart/')

def cartok(request):
    global cartlist
    total = 0
    for unit in cartlist:
        total += int(unit[3])	
    grandtotal = total + total*0.10
    for unit in cartlist:  #將購買商品寫入資料庫
        total = int(unit[1]) * int(unit[2])
        unitorder = models.DetailModel.objects.create(pname=unit[0], unitprice=unit[1], quantity=unit[2], dtotal=total)
    cartlist = []
    request.session['cartlist'] = cartlist
    return render(request, "cartok.html", locals())

def useradd(request):
    if request.method == "POST":
        username = request.POST['username']
        userPassword = request.POST['userPassword']
        userRePassword = request.POST['userRePassword']
        userPhone = request.POST['userPhone']
        userBirthday = request.POST['userBirthday']
        userEmail = request.POST['userEmail']

        #判斷是否登入
        try:
            user=User.objects.get(username=username)  
        except:
            user=None
        
        if user!=None:
            print("帳號已建立")
            password_check=True #密碼檢查
            return render(request, "useradd.html",locals())  
        else:
            if userPassword != userRePassword:
                password_check=False
                return render(request, "useradd.html",locals())  
            else:
                print("可註冊")
                #儲存至資料庫
                user = User.objects.create_user(username, userEmail, userPassword)
                user.is_staff = False	# 工作人員狀態，設定True則可以登入admin後台
                user.is_active = True
                user.tel = userPhone
                user.cBirthday = userBirthday
                user.save()
                useradd_success_status=True #註冊成功
                return render(request, "login.html",locals())
    else:
        user=None #註冊帳號檢查
        password_check=True #密碼檢查
        return render(request, "useradd.html",locals())

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        userPassword = request.POST['userPassword']
        # print(username)
        # print(userPassword)
        user = authenticate(username=username, password=userPassword)  #驗證
        print(user)
        if user is not None:  #驗證通過
            auth.login(request,user) #登入註冊
            global cartlist
            total = 0
            if 'carlist' in request.session:
                cartlist = request.session['carlist']
            else:
                cartlist=[]
            cartnum = len(cartlist)
            productall = models.ProductModel.objects.all()
            for unit in cartlist:
                total += int(unit[3])
            grandtotal = int(total +(total*0.10))    
            return render(request, "order.html",locals())  
        else:  #驗證未通過
            messages = '登入失敗！'
            useradd_login_status=True
            print(useradd_login_status)
        return render(request, "login.html",locals())  
    else:
        useradd_success_status=False #只有登入
        useradd_login_status=False
        return render(request, "login.html",locals())

def logout(request):
	auth.logout(request)
	return redirect('/index/')	

