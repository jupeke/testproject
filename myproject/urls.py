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
from django.contrib.auth import views as auth_views
from accounts import views as accounts_views

urlpatterns = [
    path('admin/', admin.site.urls, name= 'url_admin'),
    path('', views.home, name='url_home'),
    re_path(r'^discussions/(?P<discussion_id>\d+)/$', views.discussion_topics,
        name='url_discussion_topics'
    ),
    re_path(r'^discussions/(?P<discussion_id>\d+)/new/$', views.new_topic,
        name='url_new_topic'
    ),
    re_path(r'^discussions/(?P<discussion_id>\d+)/topics/(?P<topic_id>\d+)/$',
        views.topic_posts,
        name='url_topic_posts'
    ),

    re_path(r'^discussions/(?P<discussion_id>\d+)/topics/(?P<topic_id>\d+)/edit/$',
        views.edit_topic,
        name='url_edit_topic'
    ),

    re_path(r'^discussions/(?P<discussion_id>\d+)/topics/(?P<topic_id>\d+)/posts/(?P<post_id>\d+)/edit/$',
        views.edit_post,
        name='url_edit_post'
    ),

    path('signup/', accounts_views.signup, name='url_signup'),


    path('account/', accounts_views.my_account, name='url_account'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'),
        name='url_login'
    ),
    path('logout/', auth_views.LogoutView.as_view(),
        name='url_logout'
    ),


    # Below views are built-in in Django -> name change to "url_.." produced
    # mistakes.. Maybe must be the written as they are (or then change something
    # somewhere)
    path('reset/',
        auth_views.PasswordResetView.as_view(
            template_name='password_reset.html',
            email_template_name='password_reset_email.html',
            subject_template_name='password_reset_subject.txt'
        ),
        name='password_reset'),

    path('reset/done/',
        auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),
        name='password_reset_done'),

    re_path(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='password_reset_confirm.html'
        ),
        name='password_reset_confirm'),

    path('reset/complete/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='password_reset_complete.html'
        ),
        name='password_reset_complete'),

    path('settings/password/', auth_views.PasswordChangeView.as_view(
            template_name='password_change.html'
        ),
        name='password_change'),

    path('settings/password/done/', auth_views.PasswordChangeDoneView.as_view(
            template_name='password_change_done.html'
        ),
        name='password_change_done'),
    ]
