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

    phone = models.IntegerField(default="010")
    u_id = models.IntegerField(null=True)   #null=True id가 null 허용이 되면 안 될 것 같은데..?
    answer = models.TextField(max_length=200, blank=True)
    question_id = models.IntegerField(default=1, choices=Q)

class EtcOption(models.Model):
    def __str__(self):
        return self.option_name

    option_name = models.CharField(max_length=200)
    option_price = models.IntegerField()

class Option(models.Model):
    etcoption_id = models.ForeignKey(EtcOption, on_delete=models.CASCADE, related_name='etcoption_id')
    takeout = models.BooleanField()
    count = models.IntegerField()

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

    m_option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='m_option')
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_id')
    m_name = models.CharField(max_length=200)
    m_info = models.TextField()
    m_price = models.IntegerField()
    m_img = models.ImageField(blank=True, upload_to="images/", null=True)

class Basket(models.Model):
    ototal_price = models.IntegerField()
    menu_id = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name='menu_id')

class Pay(models.Model):
    date = models.DateTimeField()
    total = models.IntegerField()
    order_num = models.IntegerField()



