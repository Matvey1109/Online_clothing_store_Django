# Generated by Django 4.1.7 on 2023-04-11 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_remove_orderproduct_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
    ]