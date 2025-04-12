from django.urls import path,include

import accounts
from . import views
urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('home/',views.home,name='home'),
    path('',views.about,name='about'),
    path('account/', include('accounts.urls')),
]