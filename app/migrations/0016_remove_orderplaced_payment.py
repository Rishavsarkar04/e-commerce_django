# Generated by Django 4.1.1 on 2023-03-22 15:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_orderplaced_payment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderplaced',
            name='payment',
        ),
    ]
