# Generated by Django 4.0.4 on 2022-04-21 21:08

from django.db import migrations
import main.models


class Migration(migrations.Migration):

    dependencies = [
        ('metabase', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dashboard',
            old_name='feed_name',
            new_name='url_number',
        ),
        migrations.AlterField(
            model_name='dashboard',
            name='id',
            field=main.models.ULIDField(editable=False, primary_key=True, serialize=False),
        ),
    ]
