from django.urls import path
from django.views.generic import RedirectView

from . import controllers

app_name = "store"

urlpatterns = [
    path("", controllers.home, name="home"),
    path("stores/", controllers.store_list_page, name="stores_page"),
    path("map/", controllers.map_page, name="map_page"),
    path("info/<slug:slug>/", controllers.info_page, name="info_page"),
    path("news/<slug:slug>/", controllers.news_detail, name="news_detail"),

    path("admin/login/", controllers.AdminLoginView.as_view(), name="admin_login"),
    path("admin/logout/", controllers.admin_logout, name="admin_logout"),
    path("admin/", controllers.admin_dashboard, name="admin_dashboard"),
    path("admin/settings/", controllers.admin_settings, name="admin_settings"),
    path("admin/notifications/", controllers.admin_notifications, name="admin_notifications"),
    path("admin/<slug:model_slug>/", controllers.admin_list, name="admin_list"),
    path("admin/<slug:model_slug>/create/", controllers.admin_create, name="admin_create"),
    path("admin/<slug:model_slug>/<int:pk>/edit/", controllers.admin_update, name="admin_update"),
    path("admin/<slug:model_slug>/<int:pk>/delete/", controllers.admin_delete, name="admin_delete"),
    path("report/404/<str:action>/", controllers.report_404_action, name="report_404_action"),

    # Legacy URLs: /cms/... -> /admin/...
    path("cms/login/", RedirectView.as_view(url="/admin/login/", permanent=False)),
    path("cms/logout/", RedirectView.as_view(url="/admin/logout/", permanent=False)),
    path("cms/settings/", RedirectView.as_view(url="/admin/settings/", permanent=False)),
    path(
        "cms/<slug:model_slug>/<int:pk>/edit/",
        RedirectView.as_view(url="/admin/%(model_slug)s/%(pk)s/edit/", permanent=False),
    ),
    path(
        "cms/<slug:model_slug>/<int:pk>/delete/",
        RedirectView.as_view(url="/admin/%(model_slug)s/%(pk)s/delete/", permanent=False),
    ),
    path(
        "cms/<slug:model_slug>/create/",
        RedirectView.as_view(url="/admin/%(model_slug)s/create/", permanent=False),
    ),
    path("cms/<slug:model_slug>/", RedirectView.as_view(url="/admin/%(model_slug)s/", permanent=False)),
    path("cms/", RedirectView.as_view(url="/admin/", permanent=False)),
]

