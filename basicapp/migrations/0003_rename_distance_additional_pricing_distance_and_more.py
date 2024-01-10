# Generated by Django 5.0.1 on 2024-01-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('basicapp', '0002_pricing_delete_task_delete_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pricing',
            old_name='distance_additional',
            new_name='distance',
        ),
        migrations.RenameField(
            model_name='pricing',
            old_name='distance_base',
            new_name='time',
        ),
        migrations.RenameField(
            model_name='pricing',
            old_name='tmf',
            new_name='wait',
        ),
        migrations.RemoveField(
            model_name='pricing',
            name='wc',
        ),
        migrations.AddField(
            model_name='pricing',
            name='day',
            field=models.CharField(default='', max_length=50),
        ),
    ]