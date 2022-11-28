# Generated by Django 4.1.3 on 2022-11-16 12:43

from django.db import migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('autoservice', '0005_order_due_back_order_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='summary',
            field=tinymce.models.HTMLField(default=0, max_length=1000, verbose_name='summary'),
            preserve_default=False,
        ),
    ]
