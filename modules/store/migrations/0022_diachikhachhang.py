from django.conf import settings
from django.db import migrations, models


def _display_name(user):
    full_name = " ".join(part for part in [getattr(user, "last_name", ""), getattr(user, "first_name", "")] if part).strip()
    return full_name or getattr(user, "username", "")


def forwards(apps, schema_editor):
    app_label, model_name = settings.AUTH_USER_MODEL.split(".")
    UserModel = apps.get_model(app_label, model_name)
    HoSoKhachHang = apps.get_model("gis_store", "HoSoKhachHang")
    DiaChiKhachHang = apps.get_model("gis_store", "DiaChiKhachHang")

    existing_user_ids = set(DiaChiKhachHang.objects.values_list("user_id", flat=True))
    profiles = HoSoKhachHang.objects.exclude(dia_chi="").select_related("user")
    for profile in profiles:
        if profile.user_id in existing_user_ids:
            continue
        user = UserModel.objects.filter(pk=profile.user_id).first()
        if user is None:
            continue
        DiaChiKhachHang.objects.create(
            user_id=profile.user_id,
            ho_ten_nguoi_nhan=_display_name(user),
            so_dien_thoai=profile.so_dien_thoai or "",
            dia_chi_cu_the=profile.dia_chi,
            loai_dia_chi="home",
            mac_dinh=True,
        )


def backwards(apps, schema_editor):
    DiaChiKhachHang = apps.get_model("gis_store", "DiaChiKhachHang")
    DiaChiKhachHang.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("gis_store", "0021_seed_product_image_slots"),
    ]

    operations = [
        migrations.CreateModel(
            name="DiaChiKhachHang",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ho_ten_nguoi_nhan", models.CharField(max_length=120, verbose_name="Họ tên người nhận")),
                ("so_dien_thoai", models.CharField(max_length=20, verbose_name="Số điện thoại")),
                ("tinh_thanh", models.CharField(blank=True, max_length=120, verbose_name="Tỉnh/Thành phố")),
                ("quan_huyen", models.CharField(blank=True, max_length=120, verbose_name="Quận/Huyện")),
                ("phuong_xa", models.CharField(blank=True, max_length=120, verbose_name="Phường/Xã")),
                ("dia_chi_cu_the", models.CharField(max_length=255, verbose_name="Địa chỉ cụ thể")),
                (
                    "loai_dia_chi",
                    models.CharField(
                        choices=[("home", "Nhà riêng"), ("office", "Văn phòng"), ("other", "Khác")],
                        default="home",
                        max_length=20,
                        verbose_name="Loại địa chỉ",
                    ),
                ),
                ("mac_dinh", models.BooleanField(default=False, verbose_name="Địa chỉ mặc định")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="dia_chi_khach_hang",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Tài khoản",
                    ),
                ),
            ],
            options={
                "verbose_name": "Địa chỉ khách hàng",
                "verbose_name_plural": "Địa chỉ khách hàng",
                "ordering": ["-mac_dinh", "-created_at", "-id"],
            },
        ),
        migrations.RunPython(forwards, backwards),
    ]
