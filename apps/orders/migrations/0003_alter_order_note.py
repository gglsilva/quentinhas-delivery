# Generated by Django 4.1.1 on 2023-02-21 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_order_note'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='note',
            field=models.TextField(blank=True, null=True),
        ),
    ]
