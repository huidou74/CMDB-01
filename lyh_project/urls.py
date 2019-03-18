"""zuoye_1222 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from hc import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url('^$',views.login),

    url('^index/',views.index),
    url(r'^reload_hosts/' ,views.add_all_hosts),
    url(r'^login/', views.login),
    url(r'^code.html', views.Code),
    url(r'^register/', views.register),
    url(r'^reload/', views.reload_pwd),
    url(r'^update/', views.update),
    url(r'^delete/', views.delete),
    url(r'^delete_session/',views.delete_session),
    url(r'^date/' , views.date),
    url(r'^host/list/', views.List.as_view()),
    url(r'^host/add/$', views.Add.as_view()),
    url(r'^host/update/(\d+)/', views.Update_Form.as_view()),    #(\d+) 匹配任意数字
    url(r'^host/delete/(\d+)/', views.Delete.as_view()),
    url(r'^host/messages/(\d+)/', views.Mes_Host.as_view()),   # 主机详细页
    url(r'^host/messages/update_db/attr/', views.update_attr),
    url(r'^host/messages/create_db/', views.create_db),
    url(r'^host/messages/update_db/', views.update_db),
    url(r'^host/messages/delete_db/', views.delete_db),
    url(r'^host/messages/$', views.messages),
    url(r'^host/$',views.host),
    url(r'^user/list/', views.user_list),
    # url(r'^test/',views.test_q),   # 测试专用
    url(r'^menu/list/',views.menu_list),
    url(r'^position/list/',views.pos_list),
    url(r'^position/add/',views.pos_add),
    url(r'^position/update/(\d+)/',views.Pos_Update.as_view()),
    url(r'^position/delete/(\d+)/',views.pos_del),
    url(r'^authgroup/list/',views.auth_group_list),
    url(r'^auth/list/',views.auth_list),
    url(r'^authority/' , include('hc_auth.urls')),
    url(r'^publish/',include('publishing_system.urls')),
]


handler404 = "hc.views.page_not_found"
handler500 = "hc.views.page_error"