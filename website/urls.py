from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    path('', views.index, name='index'),#membuat url untuk view index
    path('datatransaksi/', views.datatransaksi, name='datatransaksi'),#membuat url untuk view data transaksi
    path('result/', views.result, name='result'),#membuat url untuk view result
]
