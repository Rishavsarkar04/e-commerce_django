# Generated by Django 4.1.1 on 2023-03-22 15:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_remove_orderplaced_customer_orderplaced_city_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('razorpay_order_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=200, null=True)),
                ('razorpay_signature_id', models.CharField(blank=True, max_length=200, null=True)),
                ('amount', models.FloatField()),
                ('paid', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
