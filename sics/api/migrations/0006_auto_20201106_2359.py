# Generated by Django 3.0.6 on 2020-11-06 23:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_auto_20201106_2358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reading',
            name='station',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.Station'),
        ),
    ]