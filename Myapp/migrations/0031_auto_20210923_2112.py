# Generated by Django 3.0 on 2021-09-23 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0030_auto_20210923_1828'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='orderid',
            field=models.CharField(max_length=20),
        ),
    ]
