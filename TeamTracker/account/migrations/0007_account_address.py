# Generated by Django 4.2.2 on 2023-06-27 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_bank_account'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='address',
            field=models.CharField(default='DOUZ', max_length=200),
            preserve_default=False,
        ),
    ]
