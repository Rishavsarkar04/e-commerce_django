# Generated by Django 4.1.1 on 2023-03-22 15:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_payment_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='payment',
        ),
    ]
