# Generated by Django 3.0.6 on 2020-10-17 00:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_auto_20201013_1126'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plantation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('farm', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.DeleteModel(
            name='Sensor',
        ),
        migrations.AddField(
            model_name='user',
            name='is_responsible',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram',
            field=models.CharField(max_length=30, unique=True),
        ),
        migrations.AddField(
            model_name='plantation',
            name='employees',
            field=models.ManyToManyField(blank=True, related_name='employee_plantation', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plantation',
            name='responsible',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='responsible_plantation', to=settings.AUTH_USER_MODEL),
        ),
    ]
