# Generated by Django 3.0 on 2021-07-28 20:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0004_auto_20210729_0120'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproduct',
            name='instock',
            field=models.BooleanField(default=True),
        ),
    ]
