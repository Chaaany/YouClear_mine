# Generated by Django 3.2.9 on 2021-12-26 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='detail_address',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
