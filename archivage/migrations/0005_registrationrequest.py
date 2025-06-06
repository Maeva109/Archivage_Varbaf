# Generated by Django 5.1.4 on 2025-05-18 23:54

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('archivage', '0004_alter_document_visibilite'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=128)),
                ('date_requested', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_approved', models.BooleanField(default=False)),
                ('is_rejected', models.BooleanField(default=False)),
                ('admin_note', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name': "Demande d'inscription",
                'verbose_name_plural': "Demandes d'inscription",
                'ordering': ['-date_requested'],
            },
        ),
    ]
