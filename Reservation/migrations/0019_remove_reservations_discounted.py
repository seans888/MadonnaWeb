# Generated by Django 4.1.3 on 2023-02-23 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0018_remove_reservations_discounted_alter_prices_daytime_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reservations',
            name='discounted',
        ),
    ]
