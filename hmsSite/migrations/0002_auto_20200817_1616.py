# Generated by Django 3.1 on 2020-08-17 08:16

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hmsSite', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='faculty')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, null=True, verbose_name='school/centre')),
            ],
        ),
        migrations.RemoveField(
            model_name='project',
            name='contact',
        ),
        migrations.RemoveField(
            model_name='project',
            name='department',
        ),
        migrations.RemoveField(
            model_name='project',
            name='owner',
        ),
        migrations.AddField(
            model_name='contacts',
            name='phone',
            field=models.CharField(blank=True, max_length=16, null=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+999999999'.", regex='\\+?\\d{9,15}')], verbose_name='phone number with area code'),
        ),
        migrations.AddField(
            model_name='project',
            name='benefits',
            field=models.TextField(blank=True, null=True, verbose_name='applicant benefits'),
        ),
        migrations.AddField(
            model_name='project',
            name='collab',
            field=models.TextField(blank=True, null=True, verbose_name='collaborations'),
        ),
        migrations.AddField(
            model_name='project',
            name='contact1',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.contacts'),
        ),
        migrations.AddField(
            model_name='project',
            name='contact2',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='hmsSite.contacts'),
        ),
        migrations.AddField(
            model_name='project',
            name='details',
            field=models.TextField(blank=True, null=True, verbose_name='project details'),
        ),
        migrations.AddField(
            model_name='project',
            name='end_date',
            field=models.DateField(default=datetime.date.today, verbose_name='project end date'),
        ),
        migrations.AddField(
            model_name='project',
            name='funds',
            field=models.TextField(blank=True, null=True, verbose_name='project funding'),
        ),
        migrations.AddField(
            model_name='project',
            name='other',
            field=models.TextField(blank=True, null=True, verbose_name='other information'),
        ),
        migrations.AddField(
            model_name='project',
            name='readings',
            field=models.TextField(blank=True, null=True, verbose_name='suggested readings'),
        ),
        migrations.AddField(
            model_name='project',
            name='scholarships',
            field=models.TextField(blank=True, null=True, verbose_name='scholarships fundings'),
        ),
        migrations.AddField(
            model_name='project',
            name='start_date',
            field=models.DateField(default=datetime.date.today, verbose_name='project start date'),
        ),
        migrations.AlterField(
            model_name='contacts',
            name='name',
            field=models.CharField(max_length=150, verbose_name='contact name'),
        ),
        migrations.AlterField(
            model_name='project',
            name='goals',
            field=models.TextField(blank=True, null=True, verbose_name='project goals'),
        ),
        migrations.AlterField(
            model_name='project',
            name='image',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='hmsSite.images'),
        ),
        migrations.AlterField(
            model_name='project',
            name='pref_qualifications',
            field=models.TextField(blank=True, verbose_name='additional preferred qualifications'),
        ),
        migrations.AlterField(
            model_name='project',
            name='qualifications',
            field=models.TextField(verbose_name='applicant mandatory qualifications'),
        ),
        migrations.AlterField(
            model_name='project',
            name='title',
            field=models.CharField(max_length=300, verbose_name='project title'),
        ),
        migrations.DeleteModel(
            name='Department',
        ),
        migrations.AddField(
            model_name='project',
            name='faculty',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.faculty'),
        ),
        migrations.AddField(
            model_name='project',
            name='school',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='hmsSite.school'),
        ),
    ]
