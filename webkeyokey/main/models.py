from django.db import models
from django.contrib.auth.models import AbstractUser

#8.25 - CustomUser 모델 추가시 null? 오류

# Create your models here.


class CustomUser(AbstractUser):
    Q = [
        (1, '나의 보물 1호는?'),
        (2, '나의 고향은?'),
        (3, '붕어빵 먹을 때 가장 먼저 먹는 부위는?'),
        (4, '나의 MBTI는?'),
        (5, '돌잡이 때 잡은 것은?')
    ]

    def __str__(self):
        return self.username

    u_id = models.IntegerField(unique=True, null=True)
    username = models.TextField(null=True)
    phone = models.TextField(default="010")
    answer = models.TextField(max_length=200, blank=True)
    question_id = models.IntegerField(default=1, choices=Q)
    USERNAME_FIELD = 'u_id'
    REQUIRED_FIELDS = ['username']

class Menu(models.Model):
    def __str__(self):
        return self.m_name

    C = [
        (1, '커피'),
        (2, '주스'),
        (3, '티'),
        (4, '스무디/프라푸치노'),
        (5, '논커피'),
        (6, '디저트')
    ]
    
    c_id = models.IntegerField(default=1, choices=C)

    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')
    m_name = models.CharField(max_length=200)
    m_info = models.TextField()
    m_price = models.IntegerField()
    m_img = models.ImageField(blank=True, upload_to="images/", null=True)
    m_takeout = models.BooleanField(default=False) # 사장님이 포장가능여부 표시
    options = models.ManyToManyField('Option', blank=True)

class Option(models.Model):
    def __str__(self):
        return self.option_name

    option_name = models.CharField(max_length=200)
    option_price = models.IntegerField()
    checked = models.BooleanField(default=False)    #옵션 체크했을 때 필요한 필드

class Basket(models.Model):
    ototal_price = models.IntegerField()
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='selected_menu')
    b_options = models.ManyToManyField('Option', blank=True)  #다대다 관계로 바꿈
    takeout = models.BooleanField(default=False)    # 소비자가 포장할지 안할지 선택
    count = models.IntegerField()

class Pay(models.Model):
    date = models.DateTimeField()
    total = models.IntegerField()
    order_num = models.IntegerField()
    #baskets 필드 삭제
    orders = models.ManyToManyField('Order', blank=True) #order 모델 다대다연결

class Order(models.Model):
    def __str__(self):
        return str(self.or_num)
    or_name = models.CharField(max_length=200)
    or_num = models.IntegerField()
    or_options = models.ManyToManyField('Option', blank=True)
    or_count = models.IntegerField()
    or_takeout = models.BooleanField(default=False)
