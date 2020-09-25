from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.main, name='main'),
    # ajax 통신요청 경로
    # path('ajax/', views.ajax, name='ajax'),
    path('list/', views.list, name='list'),
    path('left/', views.left, name='left'),
]