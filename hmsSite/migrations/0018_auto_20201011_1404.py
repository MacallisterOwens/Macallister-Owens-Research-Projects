# Generated by Django 3.1 on 2020-10-11 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmsSite', '0017_auto_20201011_1339'),
    ]

    operations = [
        migrations.AddField(
            model_name='image_stock',
            name='image',
            field=models.ImageField(null=True, upload_to=None, verbose_name='stock_image_no_upload'),
        ),
        migrations.AlterField(
            model_name='image_stock',
            name='name',
            field=models.CharField(max_length=150, null=True, verbose_name='image_stock_name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image_stock',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.image_stock'),
        ),
    ]
