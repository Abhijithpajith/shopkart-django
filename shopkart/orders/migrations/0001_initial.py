# Generated by Django 3.1 on 2023-07-11 09:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_variation'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_number', models.CharField(max_length=20)),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=12)),
                ('email', models.EmailField(max_length=254)),
                ('address_line_1', models.CharField(max_length=100)),
                ('address_line_2', models.CharField(blank=True, max_length=100)),
                ('country', models.CharField(max_length=20)),
                ('state', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('order_note', models.CharField(blank=True, max_length=100)),
                ('order_total', models.FloatField()),
                ('tax', models.FloatField()),
                ('status', models.CharField(choices=[('New', 'New'), ('Accepted', 'Accepted'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='New', max_length=10)),
                ('ip', models.CharField(blank=True, max_length=20)),
                ('is_ordered', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('payment_method', models.CharField(max_length=100)),
                ('amount_paid', models.CharField(max_length=100)),
                ('status', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='orderproduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.CharField(max_length=50)),
                ('size', models.CharField(max_length=50)),
                ('quantity', models.IntegerField()),
                ('product_price', models.FloatField()),
                ('ordered', models.BooleanField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('payment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.payment')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.variation')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
