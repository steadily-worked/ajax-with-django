from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    # ajax 통신요청 경로
    path('ajax/', views.ajax, name='ajax'),
]