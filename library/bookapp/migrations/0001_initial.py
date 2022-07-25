# Generated by Django 4.0 on 2022-07-25 18:47

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('author_id', models.AutoField(primary_key=True, serialize=False)),
                ('author_first_name', models.CharField(max_length=100)),
                ('author_last_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('category_name', models.CharField(max_length=100)),
                ('subcategory_name', models.CharField(blank=True, max_length=100)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('isbn', models.CharField(max_length=13, primary_key=True, serialize=False, unique=True)),
                ('title', models.CharField(max_length=250)),
                ('description', models.CharField(max_length=9999)),
                ('date_published', models.DateField()),
                ('page_number', models.IntegerField(validators=[django.core.validators.MaxValueValidator(9999)])),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('photo', models.ImageField(default='covers/default.jpg', upload_to='covers')),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookapp.author')),
                ('category', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='bookapp.category')),
            ],
        ),
    ]
