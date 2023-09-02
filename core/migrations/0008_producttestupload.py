# Generated by Django 4.2.3 on 2023-08-31 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_alter_order_options_rename_city_order_buyer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductTestUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('product_image', models.BinaryField(blank=1, null=True)),
            ],
        ),
    ]