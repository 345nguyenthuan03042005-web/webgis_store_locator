from django.db import migrations, models


def migrate_done_to_delivered(apps, schema_editor):
    DonHang = apps.get_model("gis_store", "DonHang")
    DonHang.objects.filter(trang_thai="done").update(trang_thai="delivered")


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0017_chitietdonhang_don_gia_donhang_tong_tien_and_more"),
    ]

    operations = [
        migrations.RunPython(migrate_done_to_delivered, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="donhang",
            name="trang_thai",
            field=models.CharField(
                choices=[
                    ("pending", "Chờ xử lý"),
                    ("confirmed", "Đã xác nhận"),
                    ("shipping", "Đang giao"),
                    ("delivered", "Đã giao"),
                    ("done", "Hoàn tất"),
                    ("cancelled", "Đã hủy"),
                ],
                default="pending",
                max_length=20,
                verbose_name="Trạng thái",
            ),
        ),
    ]
