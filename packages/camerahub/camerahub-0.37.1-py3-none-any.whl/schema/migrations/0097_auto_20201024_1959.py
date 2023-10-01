# Generated by Django 2.2.16 on 2020-10-24 19:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schema', '0096_auto_20201024_1941'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='camera',
            options={'ordering': ['-own', 'cameramodel__manufacturer', 'cameramodel__model', 'serial'], 'verbose_name_plural': 'cameras'},
        ),
        migrations.AlterModelOptions(
            name='lens',
            options={'ordering': ['-own', 'lensmodel__manufacturer', 'lensmodel__model', 'serial'], 'verbose_name_plural': 'lenses'},
        ),
    ]
