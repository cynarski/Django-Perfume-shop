# Generated by Django 5.0.6 on 2024-06-14 17:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('perfumeshop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='perfume',
            name='discount',
        ),
    ]
