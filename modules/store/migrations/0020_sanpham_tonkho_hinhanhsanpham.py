from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0019_gopykhachhang"),
    ]

    operations = [
        migrations.AddField(
            model_name="sanpham",
            name="ton_kho",
            field=models.PositiveIntegerField(default=0, verbose_name="Tồn kho"),
        ),
        migrations.CreateModel(
            name="HinhAnhSanPham",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("hinh_anh", models.ImageField(blank=True, null=True, upload_to="images/", verbose_name="Ảnh sản phẩm")),
                ("chu_thich", models.CharField(blank=True, max_length=150, verbose_name="Chú thích")),
                ("thu_tu", models.PositiveIntegerField(default=0, verbose_name="Thứ tự")),
                (
                    "san_pham",
                    models.ForeignKey(
                        on_delete=models.deletion.CASCADE,
                        related_name="hinh_anh_phu",
                        to="gis_store.sanpham",
                        verbose_name="Sản phẩm",
                    ),
                ),
            ],
            options={
                "verbose_name": "Hình ảnh sản phẩm",
                "verbose_name_plural": "Hình ảnh sản phẩm",
                "ordering": ["thu_tu", "id"],
            },
        ),
    ]
