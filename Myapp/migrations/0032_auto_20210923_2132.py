# Generated by Django 3.0 on 2021-09-23 21:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0031_auto_20210923_2112'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='orderid',
            field=models.IntegerField(),
        ),
    ]