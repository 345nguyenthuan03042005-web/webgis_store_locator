from django.conf import settings
from django.contrib import admin
from django.utils.html import format_html
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
                field.widget.attrs["title"] = "Toa do chi duoc lay tu ban do."

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
            message = "Can chot toa do bang click tren ban do truoc khi luu."
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
    filter_horizontal = ("san_pham",)

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
        js = ("store/js/admin_coord_from_main_map.js",)


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
