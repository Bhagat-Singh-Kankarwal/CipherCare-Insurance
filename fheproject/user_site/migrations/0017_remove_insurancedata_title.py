# Generated by Django 5.0.3 on 2024-04-15 12:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0016_insurancedata_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='insurancedata',
            name='title',
        ),
    ]
