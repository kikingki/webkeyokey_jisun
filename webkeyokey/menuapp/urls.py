from django.urls import path
from menuapp import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('optionmenu/<int:pk>', views.optionmenu, name='optionmenu'),
    path('checkmenu/', views.checkmenu, name='checkmenu'),
    path('pay/', views.pay, name='pay'),
    path('pay/success/', views.success, name='success'),
    path('order/', views.order, name='order'),
    path('orderdetail/<int:pk>', views.orderdetail, name='orderdetail'), #경로수정
    path('checkmenu/delete_basket/<int:pk>', views.delete_basket, name='delete_basket'),
    path('delete_order/<int:pk>', views.delete_order, name='delete_order'), #order 삭제 추가
]
