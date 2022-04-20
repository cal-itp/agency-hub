# Generated by Django 4.0.4 on 2022-04-20 18:04

from django.db import migrations, models
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('agency', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='agency',
            name='url_count',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agency',
            name='id',
            field=main.models.ULIDField(editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='agencyuser',
            name='id',
            field=main.models.ULIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
