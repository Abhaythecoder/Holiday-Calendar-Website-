from django.urls import path
from . import views


urlpatterns = [
    path('holidays/', views.get_holidays, name='get_holidays'),
    path('', views.loginView, name='log'),
    path('login/', views.loginbutton, name='login'),
    path('holidays/wiki/', views.holi_wiki, name='holi_wiki'),

]
