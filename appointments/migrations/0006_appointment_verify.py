# Generated by Django 5.0.4 on 2024-07-14 17:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appointments', '0005_paymentgatewaysettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='verify',
            field=models.BooleanField(default=False),
        ),
    ]
