# Generated by Django 5.0.3 on 2024-04-14 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_site', '0012_insurancedata_enc_coverage_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='insurancedata',
            name='coverage_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='insurancedata',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='insurancedata',
            name='phone_number',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='insurancedata',
            name='zip_code',
            field=models.IntegerField(null=True),
        ),
    ]