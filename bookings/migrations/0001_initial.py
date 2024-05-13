# Generated by Django 4.2.1 on 2024-05-12 07:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('buses', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_seats_books', models.IntegerField()),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
                ('fare', models.CharField(max_length=8)),
                ('qr_code', models.CharField(max_length=300)),
                ('bus_booked', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='buses.bus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Booking',
                'verbose_name_plural': 'Bookings',
            },
        ),
    ]
