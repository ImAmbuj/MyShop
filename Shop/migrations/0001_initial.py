# Generated by Django 3.0.1 on 2021-07-15 10:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Adress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('first_adress', models.CharField(max_length=300)),
                ('second_adress', models.CharField(blank=True, max_length=300, null=True)),
                ('state', models.CharField(max_length=30)),
                ('pin_code', models.IntegerField()),
                ('contact', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('slug', models.SlugField(blank=True, max_length=20, null=True)),
                ('full_name', models.CharField(max_length=80)),
                ('product_image', models.ImageField(upload_to='Product_img')),
                ('price', models.FloatField()),
                ('category', models.CharField(choices=[('A', 'Accessories'), ('S', 'Stationary')], max_length=20)),
                ('product_desc', models.CharField(max_length=200)),
                ('featured', models.BooleanField(default=False)),
                ('latest', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Shop.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(default=0, primary_key=True, serialize=False)),
                ('total_amount', models.IntegerField(default=0)),
                ('ordered', models.BooleanField(default=False)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField()),
                ('adress', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Shop.Adress')),
                ('items', models.ManyToManyField(to='Shop.OrderItem')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200)),
                ('email', models.CharField(max_length=30)),
                ('phone', models.IntegerField()),
                ('text', models.TextField(max_length=1000)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
