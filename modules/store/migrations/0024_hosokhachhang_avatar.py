from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("gis_store", "0023_trashrecord"),
    ]

    operations = [
        migrations.AddField(
            model_name="hosokhachhang",
            name="avatar",
            field=models.ImageField(blank=True, null=True, upload_to="avatar/customers/", verbose_name="Ảnh đại diện"),
        ),
    ]
