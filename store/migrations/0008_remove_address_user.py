# Generated by Django 4.1.7 on 2023-04-12 10:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_alter_address_zipcode'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='user',
        ),
    ]
