# Generated by Django 5.1.2 on 2024-10-19 23:02

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("stock_data", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stockprice",
            name="adjusted_close_price",
        ),
        migrations.RemoveField(
            model_name="stockprice",
            name="dividend_amount",
        ),
    ]
