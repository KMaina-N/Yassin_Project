# Generated by Django 4.2.3 on 2023-08-25 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='image',
            field=models.BinaryField(blank=1, editable=True, null=True),
        ),
    ]
