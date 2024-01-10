# Generated by Django 5.0.1 on 2024-01-08 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0010_ride_totalhours_ride_totalprice_ride_username_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='endtime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='ride',
            name='starttime',
            field=models.TimeField(),
        ),
        migrations.AlterField(
            model_name='ride',
            name='totalhours',
            field=models.DecimalField(decimal_places=2, max_digits=5),
        ),
        migrations.AlterField(
            model_name='ride',
            name='waittime',
            field=models.TimeField(),
        ),
    ]
