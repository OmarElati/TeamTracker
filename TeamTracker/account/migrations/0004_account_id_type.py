# Generated by Django 4.2.2 on 2023-06-27 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_account_bank'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='id_type',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]