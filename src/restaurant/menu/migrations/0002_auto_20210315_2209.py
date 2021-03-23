# Generated by Django 3.1.4 on 2021-03-15 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='calory_info',
            field=models.IntegerField(default=50),
        ),
        migrations.AddField(
            model_name='item',
            name='description',
            field=models.CharField(default='abc', max_length=200),
        ),
        migrations.AddField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, default=5.0, max_digits=4),
        ),
    ]