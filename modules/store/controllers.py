from django.shortcuts import render


def home(request):
    return render(request, 'store/home.html')


def store_list_page(request):
    return render(request, 'store/store_list.html')


def map_page(request):
    return render(request, 'store/map.html')
