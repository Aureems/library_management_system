# Generated by Django 4.0 on 2022-08-01 09:09

from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bookapp', '0019_alter_category_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='MPTTCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categ_name', models.CharField(blank=True, max_length=100)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='bookapp.mpttcategory')),
            ],
            options={
                'verbose_name_plural': 'MPTTCategories',
            },
        ),
    ]
