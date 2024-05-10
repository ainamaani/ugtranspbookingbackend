# Generated by Django 4.2.1 on 2024-05-10 16:42

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
            name='BusCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=20)),
                ('company_description', models.CharField(max_length=500)),
                ('contact_information', models.CharField(max_length=14, unique=True)),
                ('company_email', models.EmailField(max_length=254, unique=True)),
                ('company_bus_image', models.ImageField(upload_to='bus_images/')),
                ('company_manager', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bus company',
                'verbose_name_plural': 'Bus companies',
            },
        ),
    ]
