# Generated by Django 4.1.7 on 2023-04-28 17:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_favorite'),
    ]

    operations = [
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=5)),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='sizes',
            field=models.ManyToManyField(to='store.size'),
        ),
    ]
