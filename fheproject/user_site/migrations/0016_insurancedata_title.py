# Generated by Django 5.0.3 on 2024-04-15 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0015_remove_insurancedata_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancedata',
            name='title',
            field=models.CharField(blank=True, max_length=255),
        ),
    ]
