# Generated by Django 3.1 on 2020-08-14 03:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='contact name')),
                ('email', models.EmailField(max_length=254, verbose_name='contact email')),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='department name')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_link', models.ImageField(upload_to='', verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='project title')),
                ('desc', models.TextField(verbose_name='project description')),
                ('goals', models.TextField(verbose_name='project goals')),
                ('owner', models.CharField(max_length=100, verbose_name='project title')),
                ('qualifications', models.TextField(verbose_name='project qualifications')),
                ('pref_qualifications', models.TextField(verbose_name='project preferred qualifications')),
                ('contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmsSite.contacts')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='hmsSite.department')),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmsSite.images')),
            ],
        ),
    ]
