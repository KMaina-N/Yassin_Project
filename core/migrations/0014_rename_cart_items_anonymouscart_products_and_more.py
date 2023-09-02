# Generated by Django 4.2.3 on 2023-09-01 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_anonymouscart_anonymouscartitem_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='anonymouscart',
            old_name='cart_items',
            new_name='products',
        ),
        migrations.RemoveField(
            model_name='anonymouscart',
            name='created_at',
        ),
        migrations.AddField(
            model_name='anonymouscart',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='anonymouscartitem',
            name='cart',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.anonymouscart'),
        ),
    ]