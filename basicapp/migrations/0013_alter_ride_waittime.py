# Generated by Django 5.0.1 on 2024-01-08 17:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0012_alter_ride_totalhours'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='waittime',
            field=models.CharField(max_length=50),
        ),
    ]
