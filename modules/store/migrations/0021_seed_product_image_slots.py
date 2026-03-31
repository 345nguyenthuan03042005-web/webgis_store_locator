from django.db import migrations


def create_image_slots(apps, schema_editor):
    SanPham = apps.get_model("gis_store", "SanPham")
    HinhAnhSanPham = apps.get_model("gis_store", "HinhAnhSanPham")

    for product in SanPham.objects.all():
        existing_count = HinhAnhSanPham.objects.filter(san_pham=product).count()
        missing = max(0, 3 - existing_count)
        for index in range(missing):
            HinhAnhSanPham.objects.create(
                san_pham=product,
                chu_thich=f"Ảnh phụ {existing_count + index + 1}",
                thu_tu=existing_count + index + 1,
            )


def remove_empty_image_slots(apps, schema_editor):
    HinhAnhSanPham = apps.get_model("gis_store", "HinhAnhSanPham")
    HinhAnhSanPham.objects.filter(hinh_anh="").delete()


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0020_sanpham_tonkho_hinhanhsanpham"),
    ]

    operations = [
        migrations.RunPython(create_image_slots, remove_empty_image_slots),
    ]
