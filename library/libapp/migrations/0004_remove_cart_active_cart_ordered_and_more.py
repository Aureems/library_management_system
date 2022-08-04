# Generated by Django 4.0 on 2022-08-03 12:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0003_alter_order_due_to_date_cart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='active',
        ),
        migrations.AddField(
            model_name='cart',
            name='ordered',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cart',
            name='order_date',
            field=models.DateField(default=datetime.datetime(2022, 8, 3, 15, 15, 53, 128303), null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='due_to_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 2, 15, 15, 53, 129302)),
        ),
    ]
