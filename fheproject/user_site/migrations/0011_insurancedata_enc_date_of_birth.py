# Generated by Django 5.0.3 on 2024-04-14 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0010_insurancedata_enc_address_insurancedata_enc_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='insurancedata',
            name='enc_date_of_birth',
            field=models.BinaryField(null=True),
        ),
    ]