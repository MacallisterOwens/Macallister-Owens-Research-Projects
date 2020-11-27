# Generated by Django 3.1 on 2020-10-11 05:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmsSite', '0016_auto_20201005_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image_Stock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='image_stock')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='image_stock',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.image_stock'),
        ),
    ]
