# Generated by Django 4.1.3 on 2023-02-17 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reservation', '0008_facility_facilitypic'),
    ]

    operations = [
        migrations.AddField(
            model_name='facility',
            name='facilityActive',
            field=models.BooleanField(default=False),
        ),
    ]
