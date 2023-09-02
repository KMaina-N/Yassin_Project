# Generated by Django 4.2.3 on 2023-08-26 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_remove_orderitem_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'ordering': ('-date_ordered',)},
        ),
        migrations.RenameField(
            model_name='order',
            old_name='city',
            new_name='buyer',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='created',
            new_name='date_ordered',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='paid',
            new_name='ordered',
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='order',
            name='updated',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='core.order'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('buyer', models.CharField(max_length=100)),
                ('ordered', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.products')),
            ],
        ),
    ]