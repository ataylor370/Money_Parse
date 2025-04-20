from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='accounts.signup'),
    path('login/', views.login_view, name='accounts.login'),
    path('logout/', views.logout_view, name='accounts.logout'),
    path("delete/", views.delete_account_view, name="delete_account"),
]
