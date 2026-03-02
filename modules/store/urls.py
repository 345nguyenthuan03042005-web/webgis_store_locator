from django.urls import path
from . import controllers

app_name = 'store'

urlpatterns = [
    path('', controllers.home, name='home'),
    path('stores/', controllers.store_list_page, name='stores_page'),
    path('map/', controllers.map_page, name='map_page'),
    path('info/<slug:slug>/', controllers.info_page, name='info_page'),
    path('news/<slug:slug>/', controllers.news_detail, name='news_detail'),
]
