from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import render
from django.http import HttpResponseNotFound

urlpatterns = [
    path('', include('modules.store.urls')),
    path('tools/', include('modules.spatial.urls')),
    # test 404 page when DEBUG=True
    path('404-test/', lambda request: HttpResponseNotFound(render(request, '404.html'))),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
