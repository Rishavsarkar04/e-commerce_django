# Generated by Django 4.1.1 on 2023-03-22 15:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_orderplaced_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderplaced',
            name='payment',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='app.payment'),
        ),
    ]