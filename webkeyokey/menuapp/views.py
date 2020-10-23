from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from main.models import CustomUser, Menu, Option, Basket, Pay, Order
from datetime import datetime
from django.utils.dateformat import DateFormat
import random


# from .forms import OptionForm, EtcOptionForm

# Create your views here.
#8.27 - AttributeError: type object 'Category' has no attribute 'obects' 에러 => 오타 조심하자

# 8.30 - 1. menu.m_image가 뜨지 않음. => main url.py에 적어줘야 했음.
# 2. 한 메뉴에 연결된 옵션과 기타옵션을 가져오는 건 어떻게 하는가? - 일단 object를 다 가져와보자..
# 3. 담기를 눌렀을 때 바구니에 저장해야 하는 것 - js가 필요하지 않나?
# 4. 체크박스에 체크되거나 수량을 +,-했을 때 모델에 저장하면 되는가? => forms.py로 바꿈
# 5. optionmenu 페이지에서 총 금액이 나오려면 옵션 선택하는대로 실시간으로 계산이 되어야 하지 않나?? => 새로고침 누를 때 계산하도록
# 6. 카테고리를 바꾸니 menu 페이지 이상하게 뜸 => 그냥 a태그로 카테고리 쓰기

# 9.21 - 1. 바구니도 옵션과 다대다 관계로 해야할 듯? 한 바구니에 1메뉴+여러개의 옵션 가격이 들어가야함.
# 2. takeout 체크박스를 선택하지 않았을 경우엔 아예 POST로 전달이 안되는데 이런 경우엔 어떡하징 => 해결
# 3. 바구니의 총 금액 보여주기 -> jsp로 


def menu(request):
    menus = Menu.objects.all()
    user = request.user     #현재 로그인한 유저
    return render(request, 'menuapp/menu.html', {'menus':menus})

def optionmenu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    basket = Basket()
    if request.method == 'POST':
        basket.menu_id = menu
        basket.takeout = False
        if request.POST.getlist('takeout') != []:
            basket.takeout = True
        basket.count = request.POST['count']
        if int(basket.count) <= 0:  #수량을 음수로 선택했을 경우 다시 선택하도록 함
            return HttpResponse("수량을 다시 선택해주세요.")    
        basket.ototal_price = menu.m_price
        check_values = request.POST.getlist('option[]')
        op_list = list()
        for c in check_values:
            if Option.objects.filter(option_name=c).exists():
                op = Option.objects.get(option_name=c)
                basket.ototal_price += op.option_price
                op_list.append(op)

        basket.ototal_price *= int(basket.count)
        basket.save()
        basket.b_options.add(*op_list)

    return render(request, 'menuapp/optionmenu.html', {'menu':menu})

def checkmenu(request):
    # 총 금액 계산하는 money 변수 추가
    baskets = Basket.objects.all()
    money = 0
    for b in baskets:
        money +=  int(b.ototal_price)
    return render(request, 'menuapp/checkmenu.html', {'baskets': baskets, 'money':money})

def delete_basket(request, pk):
    basket = get_object_or_404(Basket, pk=pk)
    basket.delete()
    return redirect('checkmenu')

def pay(request):
    money = 0
    for b in Basket.objects.all():
        money += int(b.ototal_price)
    if money == 0:
        return HttpResponse("주문금액이 0원입니다. 메뉴를 추가해주세요.")
    return render(request, 'menuapp/pay.html', {'money':money})

def success(request):
    pay = Pay()
    pay.date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    pay.total = 0
    pay.order_num = random.randrange(0,500) # random 범위가 좁은 것 같아서 100->500으로 수정
    bt_list = list()
    or_list = list()    #order를 저장할  리스트 or_list 생성
    for b in Basket.objects.all():
        pay.total += int(b.ototal_price)
        order = Order()
        order.or_name = b.menu_id.m_name
        order.or_num = pay.order_num
        order.or_count = b.count
        order.or_takeout = b.takeout
        for bt in b.b_options.all():
            bt_list.append(bt)
            
        order.save()
        order.or_options.add(*bt_list)
        bt_list.clear() #리스트 비우기
        or_list.append(order) #리스트에 order 추가

    pay.save()
    pay.orders.add(*or_list) #pay에 order 저장

    for b in Basket.objects.all():
        b.delete()
    return render(request, 'menuapp/success.html', {'pay':pay})


def order(request):
    por_list = Pay.objects.all()    #order 대신 pay 모델을 불러오는 것으로 변경
    return render(request, 'menuapp/order.html', {'por_list':por_list})

def delete_order(request, pk):  # 한 고객의 모든 주문을 한번에 삭제
    pay = get_object_or_404(Pay, pk=pk)
    for o in pay.orders.all():
        o.delete()
    return redirect('order')

def orderdetail(request, pk):
    p_or = get_object_or_404(Pay, pk=pk)
    return render(request, 'menuapp/orderdetail.html', {'p_or':p_or})
