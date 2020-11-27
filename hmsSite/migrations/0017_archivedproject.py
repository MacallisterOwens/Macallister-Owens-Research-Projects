# Generated by Django 3.1 on 2020-10-09 06:04

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hmsSite', '0016_auto_20201005_2055'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArchivedProject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approved', models.BooleanField(blank=True, default=False, verbose_name='project approved')),
                ('title', models.CharField(max_length=300, verbose_name='project title')),
                ('desc', models.TextField(verbose_name='project description')),
                ('short_desc', models.CharField(max_length=300, null=True, verbose_name='project short description ~30 words')),
                ('readings', models.TextField(blank=True, null=True, verbose_name='suggested readings')),
                ('goals', models.TextField(blank=True, null=True, verbose_name='project goals')),
                ('collab', models.TextField(blank=True, null=True, verbose_name='collaborations')),
                ('funds', models.TextField(blank=True, null=True, verbose_name='project funding')),
                ('benefits', models.TextField(blank=True, null=True, verbose_name='applicant benefits')),
                ('scholarships', models.TextField(blank=True, null=True, verbose_name='scholarships fundings')),
                ('other', models.TextField(blank=True, null=True, verbose_name='other information')),
                ('qualifications', models.TextField(verbose_name='applicant mandatory qualifications')),
                ('pref_qualifications', models.TextField(blank=True, verbose_name='additional preferred qualifications')),
                ('start_date', models.DateField(default=datetime.date.today, verbose_name='project start date')),
                ('end_date', models.DateField(default=datetime.date.today, verbose_name='project end date')),
                ('contact1_name', models.CharField(max_length=150, null=True, verbose_name='primary contact name')),
                ('contact1_url', models.URLField(null=True, verbose_name='<a href="https://research-repository.uwa.edu.au/" target="_blank">Research Repositry URL<a/>')),
                ('contact1_email', models.EmailField(max_length=254, null=True, verbose_name='primary contact email')),
                ('contact1_phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='primary phone number')),
                ('contact2_name', models.CharField(blank=True, max_length=150, null=True, verbose_name='seconday contact name')),
                ('contact2_url', models.URLField(blank=True, null=True, verbose_name='<div class= "url2"> <a href="https://research-repository.uwa.edu.au/" target="_blank">Research Repositry URL<a/></div>')),
                ('contact2_email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='secondary contact email')),
                ('contact2_phone', models.CharField(blank=True, max_length=16, null=True, verbose_name='secondary phone number')),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/', verbose_name='image displayed on page')),
                ('image_thumbnail', models.ImageField(blank=True, null=True, upload_to='thumbnails/', verbose_name='thumbnail displayed on page')),
                ('faculty', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.faculty')),
                ('school', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.school')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Archived Project',
                'verbose_name_plural': 'Archived Projects',
            },
        ),
    ]
