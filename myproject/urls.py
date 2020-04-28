"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from discussions import views

from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls, name= 'url_admin'),
    path('', views.home, name='url_home'),
    re_path(r'^discussions/(?P<discussion_id>\d+)/$', views.discussion_topics,
            name='url_discussion_topics'),
    re_path(r'^discussions/(?P<discussion_id>\d+)/new/$', views.new_topic,
            name='url_new_topic'),
    path('signup/', accounts_views.signup, name='url_signup'),
    path('logout/', auth_views.LogoutView.as_view(), name='url_logout'),
]
