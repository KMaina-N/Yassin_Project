# Generated by Django 4.2.3 on 2023-09-29 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_remove_order_cost_of_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='order_id',
            field=models.SlugField(blank=True, max_length=100, null=True),
        ),
    ]
