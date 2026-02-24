from django.urls import path
from . import controllers

app_name = 'store'

urlpatterns = [
    path('', controllers.home, name='home'),
    path('stores/', controllers.store_list_page, name='stores_page'),
    path('map/', controllers.map_page, name='map_page'),
]
