from django.contrib import admin
from .models import CustomUser, Menu, Option, EtcOption, Basket, Pay

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Menu)
admin.site.register(Option)
admin.site.register(EtcOption)
admin.site.register(Basket)
admin.site.register(Pay)

