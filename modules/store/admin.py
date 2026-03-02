from django.conf import settings
from django.apps import apps
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import format_html
from django.utils.text import capfirst
from django import forms

from .models import (
    ThuongHieu,
    NhaCungCap,
    NhomSanPham,
    SanPham,
    ChuoiCuaHang,
    CuaHang,
    NhanVien,
    KhuyenMai,
)


def _img(field_file, size: int = 42, media_fallback: str | None = None):
    url = ""

    try:
        if field_file and getattr(field_file, "name", ""):
            url = field_file.url
    except Exception:
        url = ""

    if not url and media_fallback:
        url = settings.MEDIA_URL + media_fallback.lstrip("/")

    if not url:
        return "-"

    return format_html(
        '<img src="{}" loading="lazy" '
        'style="width:{}px;height:{}px;object-fit:cover;'
        'border-radius:10px;border:1px solid rgba(255,255,255,.18);" />',
        url,
        size,
        size,
    )



def _vi_permission_action(name: str) -> str:
    mapping = (
        ("Can add ", "Có thể thêm "),
        ("Can change ", "Có thể sửa "),
        ("Can delete ", "Có thể xóa "),
        ("Can view ", "Có thể xem "),
    )
    for src, dst in mapping:
        if name.startswith(src):
            return dst + name[len(src):]
    return name


def _app_verbose_name(app_label: str) -> str:
    try:
        return apps.get_app_config(app_label).verbose_name
    except LookupError:
        return app_label


class UserAdminViChangeForm(UserChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        rename = {
            "first_name": "Tên",
            "last_name": "Họ",
            "email": "Địa chỉ email",
        }
        for field_name, label in rename.items():
            field = self.fields.get(field_name)
            if field is not None:
                field.label = label

        password_field = self.fields.get("password")
        if password_field is not None and self.instance and self.instance.pk:
            reset_url = reverse("admin:auth_user_password_change", args=(self.instance.pk,))
            password_field.help_text = format_html(
                "Mật khẩu gốc không được lưu nên không thể xem lại mật khẩu hiện tại. "
                "Bạn có thể đổi mật khẩu bằng <a href=\"{}\">biểu mẫu này</a>.",
                reset_url,
            )

        groups_field = self.fields.get("groups")
        if groups_field is not None:
            groups_field.help_text = (
                "Người dùng sẽ nhận toàn bộ quyền của các nhóm được chọn. "
                "Giữ phím Ctrl/Command để chọn nhiều mục."
            )

        perms_field = self.fields.get("user_permissions")
        if perms_field is not None:
            perms_field.help_text = (
                "Quyền riêng được cấp trực tiếp cho người dùng. "
                "Giữ phím Ctrl/Command để chọn nhiều mục."
            )

            def _permission_label(obj):
                app_name = _app_verbose_name(obj.content_type.app_label)
                model_cls = obj.content_type.model_class()
                model_name = model_cls._meta.verbose_name if model_cls else obj.content_type.model
                action_name = _vi_permission_action(obj.name)
                return f"{capfirst(app_name)} | {capfirst(model_name)} | {action_name}"

            perms_field.label_from_instance = _permission_label


class UserAdminVi(DjangoUserAdmin):
    form = UserAdminViChangeForm

class CuaHangAdminForm(forms.ModelForm):
    class Meta:
        model = CuaHang
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ("vi_do", "kinh_do"):
            field = self.fields.get(field_name)
            if field is not None:
                field.widget.attrs["readonly"] = "readonly"
                field.widget.attrs["title"] = "T\u1ecda \u0111\u1ed9 ch\u1ec9 \u0111\u01b0\u1ee3c l\u1ea5y t\u1eeb b\u1ea3n \u0111\u1ed3."
        san_pham_field = self.fields.get("san_pham")
        if san_pham_field is not None:
            san_pham_field.help_text = (
                "T\u00ecm nhanh v\u00e0 ch\u1ecdn theo ch\u1ebf \u0111\u1ed9 Ch\u1ecdn 1/Ch\u1ecdn nhi\u1ec1u b\u00ean d\u01b0\u1edbi danh s\u00e1ch."
            )

    def clean(self):
        cleaned = super().clean()
        lat = cleaned.get("vi_do")
        lon = cleaned.get("kinh_do")
        source = (self.data.get("_coord_from_map") or "").strip()

        changed = not bool(self.instance and self.instance.pk)

        if self.instance and self.instance.pk and lat is not None and lon is not None:
            old_lat = float(self.instance.vi_do)
            old_lon = float(self.instance.kinh_do)
            changed = abs(float(lat) - old_lat) > 1e-12 or abs(float(lon) - old_lon) > 1e-12

        if changed and source != "map":
            message = "C\u1ea7n ch\u1ed1t t\u1ecda \u0111\u1ed9 b\u1eb1ng c\u00e1ch click tr\u00ean b\u1ea3n \u0111\u1ed3 tr\u01b0\u1edbc khi l\u01b0u."
            self.add_error("vi_do", message)
            self.add_error("kinh_do", message)

        return cleaned


@admin.register(ThuongHieu)
class ThuongHieuAdmin(admin.ModelAdmin):
    list_display = ("id", "ten")
    list_display_links = ("id", "ten")
    search_fields = ("ten",)
    ordering = ("ten",)
    list_per_page = 25


@admin.register(NhaCungCap)
class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = ("id", "ten", "ghi_chu_short")
    list_display_links = ("id", "ten")
    search_fields = ("ten", "ghi_chu")
    ordering = ("ten",)
    list_per_page = 25

    @admin.display(description="Ghi chú")
    def ghi_chu_short(self, obj):
        return (obj.ghi_chu[:60] + "...") if obj.ghi_chu and len(obj.ghi_chu) > 60 else (obj.ghi_chu or "-")


@admin.register(NhomSanPham)
class NhomSanPhamAdmin(admin.ModelAdmin):
    list_display = ("id", "ten")
    list_display_links = ("id", "ten")
    search_fields = ("ten",)
    ordering = ("ten",)
    list_per_page = 25


@admin.register(SanPham)
class SanPhamAdmin(admin.ModelAdmin):
    list_display = ("id", "thumb", "ten", "nhom_san_pham", "thuong_hieu", "nha_cung_cap")
    list_display_links = ("id", "ten")
    list_filter = ("nhom_san_pham", "thuong_hieu", "nha_cung_cap")
    search_fields = ("ten", "nhom_san_pham__ten", "thuong_hieu__ten", "nha_cung_cap__ten")
    list_select_related = ("nhom_san_pham", "thuong_hieu", "nha_cung_cap")
    ordering = ("ten",)
    list_per_page = 25
    autocomplete_fields = ("nhom_san_pham", "thuong_hieu", "nha_cung_cap")

    @admin.display(description="Ảnh")
    def thumb(self, obj):
        return _img(obj.hinh_anh, size=44)

    class Media:
        js = ("assets/js/image_preview.js",)


@admin.register(ChuoiCuaHang)
class ChuoiCuaHangAdmin(admin.ModelAdmin):
    list_display = ("id", "logo_thumb", "ten", "mo_ta_short")
    list_display_links = ("id", "ten")
    search_fields = ("ten", "mo_ta")
    ordering = ("ten",)
    list_per_page = 25

    @admin.display(description="Logo")
    def logo_thumb(self, obj):
        return _img(obj.logo, size=44)

    @admin.display(description="Mô tả")
    def mo_ta_short(self, obj):
        return (obj.mo_ta[:60] + "...") if obj.mo_ta and len(obj.mo_ta) > 60 else (obj.mo_ta or "-")

    class Media:
        js = ("assets/js/image_preview.js",)


@admin.register(CuaHang)
class CuaHangAdmin(admin.ModelAdmin):
    form = CuaHangAdminForm
    list_display = (
        "id",
        "ten",
        "chuoi",
        "quan_huyen",
        "gio_hoat_dong",
        "hoat_dong_24h",
        "dia_chi_short",
        "vi_do",
        "kinh_do",
    )
    list_display_links = ("id", "ten")
    list_filter = ("chuoi", "quan_huyen", "hoat_dong_24h")
    search_fields = ("ten", "dia_chi", "quan_huyen", "chuoi__ten")
    list_select_related = ("chuoi",)
    ordering = ("chuoi__ten", "quan_huyen", "ten")
    list_per_page = 25

    @admin.display(description="Địa chỉ")
    def dia_chi_short(self, obj):
        return (obj.dia_chi[:60] + "...") if obj.dia_chi and len(obj.dia_chi) > 60 else (obj.dia_chi or "-")

    @admin.display(description="Giờ hoạt động")
    def gio_hoat_dong(self, obj):
        if obj.hoat_dong_24h:
            return "24/7"
        if obj.mo_cua and obj.dong_cua:
            return f"{obj.mo_cua.strftime('%H:%M')} - {obj.dong_cua.strftime('%H:%M')}"
        if obj.mo_cua:
            return f"Mở: {obj.mo_cua.strftime('%H:%M')}"
        if obj.dong_cua:
            return f"Đóng: {obj.dong_cua.strftime('%H:%M')}"
        return "-"

    class Media:
        css = {
            "all": ("store/css/admin_multiselect.css",),
        }
        js = (
            "store/js/admin_multiselect_autocomplete_vn.js",
            "store/js/admin_coord_from_main_map.js",
        )


@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ("id", "avatar_thumb", "ho_ten", "chuc_vu", "cua_hang", "so_dien_thoai", "email")
    list_display_links = ("id", "ho_ten")
    list_filter = ("cua_hang__chuoi", "cua_hang", "chuc_vu")
    search_fields = ("ho_ten", "chuc_vu", "so_dien_thoai", "email", "cua_hang__ten", "cua_hang__chuoi__ten")
    list_select_related = ("cua_hang", "cua_hang__chuoi")
    ordering = ("ho_ten",)
    list_per_page = 25
    autocomplete_fields = ("cua_hang",)

    @admin.display(description="Avatar")
    def avatar_thumb(self, obj):
        return _img(obj.avatar, size=40, media_fallback="avatar/default.jpg")

    class Media:
        js = ("assets/js/image_preview.js",)


@admin.register(KhuyenMai)
class KhuyenMaiAdmin(admin.ModelAdmin):
    list_display = ("id", "ten", "mo_ta_short")
    list_display_links = ("id", "ten")
    search_fields = ("ten", "mo_ta")
    ordering = ("-id",)
    list_per_page = 25
    filter_horizontal = ("thuong_hieu", "cua_hang")

    @admin.display(description="Mô tả")
    def mo_ta_short(self, obj):
        return (obj.mo_ta[:70] + "...") if obj.mo_ta and len(obj.mo_ta) > 70 else (obj.mo_ta or "-")

try:
    admin.site.unregister(User)
except NotRegistered:
    pass

admin.site.register(User, UserAdminVi)