# Generated by Django 3.0 on 2021-10-01 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapp', '0033_orderpending_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='comment',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]