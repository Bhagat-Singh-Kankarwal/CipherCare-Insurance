# Generated by Django 5.0.3 on 2024-04-29 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0022_insurancedata_dl_no_insurancedata_enc_dl_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurancedata',
            name='dl_no',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
