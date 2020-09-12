from django.urls import path
from menuapp import views


urlpatterns = [
    path('', views.menu, name='menu'),
    path('optionmenu/<int:pk>', views.optionmenu, name='optionmenu'),
    path('checkmenu/', views.checkmenu, name='checkmenu'),
    path('pay/', views.pay, name='pay'),
    path('success/', views.success, name='success'),
    path('order/', views.order, name='order'),
    path('orderdetail/', views.orderdetail, name='orderdetail'),
    path('delete/<int:pk>', views.delete, name='delete'),
]
