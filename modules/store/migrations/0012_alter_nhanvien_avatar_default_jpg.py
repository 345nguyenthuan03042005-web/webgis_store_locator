from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0011_cuahang_dong_cua_cuahang_hoat_dong_24h_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="nhanvien",
            name="avatar",
            field=models.ImageField(
                blank=True,
                default="avatar/default.jpg",
                null=True,
                upload_to="avatar/",
                verbose_name="Ảnh nhân viên",
            ),
        ),
    ]

