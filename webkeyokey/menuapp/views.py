from django.shortcuts import render, redirect, get_object_or_404
from main.models import CustomUser, Menu, Option, EtcOption, Basket, Pay
# from .forms import OptionForm, EtcOptionForm

# Create your views here.
#8.27 - AttributeError: type object 'Category' has no attribute 'obects' 에러 => 오타 조심하자

# 8.30 - 1. menu.m_image가 뜨지 않음. => main url.py에 적어줘야 했음.
# 2. 한 메뉴에 연결된 옵션과 기타옵션을 가져오는 건 어떻게 하는가? - 일단 object를 다 가져와보자..
# 3. 담기를 눌렀을 때 바구니에 저장해야 하는 것 - js가 필요하지 않나?
# 4. 체크박스에 체크되거나 수량을 +,-했을 때 모델에 저장하면 되는가? => forms.py로 바꿈
# 5. optionmenu 페이지에서 총 금액이 나오려면 옵션 선택하는대로 실시간으로 계산이 되어야 하지 않나?? => 새로고침 누를 때 계산하도록
# 6. 카테고리를 바꾸니 menu 페이지 이상하게 뜸 => 그냥 a태그로 카테고리 쓰기

def menu(request):
    menus = Menu.objects.all()
    return render(request, 'menuapp/menu.html', {'menus':menus})

def optionmenu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)
    if request.method == 'POST':
        basket = Basket()
        menu_op = menu

        menu_op.m_option.takeout = request.POST['takeout']
        menu_op.m_option.count = request.POST['count']

        check_values = request.POST.getlist('etcoption')
    # total_price = (menu.m_price + etcoptions.option_price)* options.count

    return render(request, 'menuapp/optionmenu.html', {'menu':menu})

def checkmenu(request):
    menus = Menu()
    baskets = Basket()
    # baskets.ototal_price = (menus.m_price + etcoptions.option_price)* options.count
    return render(request, 'menuapp/checkmenu.html')

def delete(request, pk):
    baskets = get_object_or_404(Basket, pk=pk)
    baskets.delete()
    return redirect('checkmenu')

def pay(request):
    return render(request, 'menuapp/pay.html')

def success(request):
    pay = Pay.objects.all()
    return render(request, 'menuapp/success.html', {'pay':pay})

def order(request):
    return render(request, 'menuapp/order.html')

def orderdetail(request):
    return render(request, 'menuapp/orderdetail.html')