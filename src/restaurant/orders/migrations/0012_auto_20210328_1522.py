# Generated by Django 3.1.7 on 2021-03-28 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0011_orderitem_owner'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='order_item',
        ),
    ]