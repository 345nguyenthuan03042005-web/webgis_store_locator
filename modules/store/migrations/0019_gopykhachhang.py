from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0018_order_shipping_delivered_statuses"),
    ]

    operations = [
        migrations.CreateModel(
            name="GopYKhachHang",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("ho_ten", models.CharField(max_length=120, verbose_name="Họ tên")),
                ("email", models.EmailField(max_length=254, verbose_name="Email")),
                ("so_dien_thoai", models.CharField(blank=True, max_length=20, verbose_name="Số điện thoại")),
                ("chu_de", models.CharField(max_length=150, verbose_name="Chủ đề")),
                ("noi_dung", models.TextField(verbose_name="Nội dung góp ý")),
                ("da_phan_hoi", models.BooleanField(default=False, verbose_name="Đã phản hồi")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="Thời gian tạo")),
            ],
            options={
                "verbose_name": "Góp ý khách hàng",
                "verbose_name_plural": "Góp ý khách hàng",
                "ordering": ["-created_at"],
            },
        ),
    ]
