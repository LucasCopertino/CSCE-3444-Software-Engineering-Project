# Generated by Django 3.1.7 on 2021-03-28 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20210327_2357'),
        ('orders', '0010_auto_20210328_1455'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='owner',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='accounts.customer'),
        ),
    ]