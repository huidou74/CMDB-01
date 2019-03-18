from django.contrib import admin

# Register your models here.
from hc.models import UserInfo
from hc.models import Position
from hc.models import Auth
from hc.models import AuthGroup
from hc.models import Menu

admin.site.register(UserInfo)
admin.site.register(Position)
admin.site.register(Auth)
admin.site.register(AuthGroup)
admin.site.register(Menu)

