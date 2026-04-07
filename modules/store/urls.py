from django.urls import path
from django.views.generic import RedirectView

from . import controllers

app_name = "store"

urlpatterns = [
    path("", controllers.home, name="home"),
    path("products/", controllers.product_catalog, name="product_catalog"),
    path("products/<int:pk>/", controllers.product_detail, name="product_detail"),
    path("cart/", controllers.cart_view, name="cart"),
    path("cart/add/<int:pk>/", controllers.cart_add, name="cart_add"),
    path("cart/update/", controllers.cart_update, name="cart_update"),
    path("cart/remove/<int:pk>/", controllers.cart_remove, name="cart_remove"),
    path("cart/clear/", controllers.cart_clear, name="cart_clear"),
    path("checkout/", controllers.checkout_view, name="checkout"),
    path("orders/", controllers.my_orders, name="my_orders"),
    path("orders/<int:pk>/", controllers.order_detail, name="order_detail"),
    path("payments/momo/<int:pk>/", controllers.momo_demo_payment, name="momo_demo_payment"),
    path("notifications/", controllers.user_notifications, name="user_notifications"),
    path("feedback/", controllers.feedback_view, name="feedback"),
    path("stores/", controllers.store_list_page, name="stores_page"),
    path("map/", controllers.map_page, name="map_page"),
    path("info/<slug:slug>/", controllers.info_page, name="info_page"),
    path("news/<slug:slug>/", controllers.news_detail, name="news_detail"),

    path("admin/login/", controllers.AdminLoginView.as_view(), name="admin_login"),
    path("admin/logout/", controllers.admin_logout, name="admin_logout"),
    path("admin/", controllers.admin_dashboard, name="admin_dashboard"),
    path("admin/inventory/", controllers.admin_inventory_hub, name="admin_inventory_hub"),
    path("admin/inventory/restock/", controllers.admin_inventory_restock, name="admin_inventory_restock"),
    path("admin/settings/", controllers.admin_settings, name="admin_settings"),
    path("admin/notifications/", controllers.admin_notifications, name="admin_notifications"),
    path("admin/trash/", controllers.admin_trash_list, name="admin_trash"),
    path("admin/trash/<int:pk>/restore/", controllers.admin_trash_restore, name="admin_trash_restore"),
    path("admin/trash/<int:pk>/delete/", controllers.admin_trash_delete, name="admin_trash_delete"),
    path("admin/users/", controllers.admin_user_management, name="admin_user_management"),
    path("admin/users/<int:pk>/password/", controllers.admin_user_password, name="admin_user_password"),
    path("admin/orders/<int:pk>/<str:status>/", controllers.admin_order_status_action, name="admin_order_status_action"),
    path("admin/orders/<int:pk>/payment/<str:status>/", controllers.admin_order_payment_status_action, name="admin_order_payment_status_action"),
    path("admin/orders/<int:pk>/receipt/<str:action>/", controllers.admin_order_receipt_review_action, name="admin_order_receipt_review_action"),
    path("admin/inventory/<int:pk>/print/", controllers.admin_inventory_print, name="admin_inventory_print"),
    path("admin/inventory/<int:pk>/pdf/", controllers.admin_inventory_pdf, name="admin_inventory_pdf"),
    path("admin/<slug:model_slug>/", controllers.admin_list, name="admin_list"),
    path("admin/<slug:model_slug>/create/", controllers.admin_create, name="admin_create"),
    path("admin/<slug:model_slug>/<int:pk>/edit/", controllers.admin_update, name="admin_update"),
    path("admin/<slug:model_slug>/<int:pk>/delete/", controllers.admin_delete, name="admin_delete"),
    path("report/404/<str:action>/", controllers.report_404_action, name="report_404_action"),

    path("user/login/", controllers.UserLoginView.as_view(), name="user_login"),
    path("user/register/", controllers.user_register, name="user_register"),
    path("user/logout/", controllers.user_logout, name="user_logout"),
    path("user/", controllers.user_dashboard, name="user_dashboard"),
    path("user/profile/", controllers.user_profile, name="user_profile"),
    path("user/address/", controllers.user_address, name="user_address"),
    path("user/password/", controllers.user_password_change, name="user_password_change"),

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
