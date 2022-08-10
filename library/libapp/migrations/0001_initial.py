# Generated by Django 4.0 on 2022-08-10 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bookapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref_code', models.CharField(blank=True, max_length=9, null=True)),
                ('is_ordered', models.BooleanField(blank=True, default=False, null=True)),
                ('date_ordered', models.DateTimeField(blank=True, null=True)),
                ('until_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_ordered', models.BooleanField(blank=True, default=False, null=True)),
                ('date_added', models.DateTimeField(auto_now=True, null=True)),
                ('date_ordered', models.DateTimeField(blank=True, null=True)),
                ('date_returned', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('books', models.ManyToManyField(blank=True, to='bookapp.Book')),
            ],
        ),
    ]
