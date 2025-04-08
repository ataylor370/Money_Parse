from django.urls import path, include
from . import views
from django.contrib import admin

urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('accounts/', include('accounts.urls')),
]