# Generated by Django 3.2.24 on 2024-02-11 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_item_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='tags',
            field=models.ManyToManyField(to='inventory.Tags'),
        ),
        migrations.DeleteModel(
            name='ItemTags',
        ),
    ]
