# Generated by Django 4.1.7 on 2023-04-12 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_orderproduct_ordered'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='apartment_address',
            new_name='address',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='street_address',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='zip',
            new_name='state',
        ),
        migrations.AddField(
            model_name='address',
            name='zipcode',
            field=models.CharField(default='100', max_length=100),
        ),
    ]
