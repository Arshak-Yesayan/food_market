# Generated by Django 3.1 on 2020-08-24 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_selling_item_item_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='selling_item',
            name='item_image',
            field=models.ImageField(default='selling_items/default.jpg', upload_to='selling_items'),
        ),
    ]
