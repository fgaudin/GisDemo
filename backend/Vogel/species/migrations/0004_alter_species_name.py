# Generated by Django 5.1.6 on 2025-02-13 08:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('species', '0003_species_avatar_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='species',
            name='name',
            field=models.CharField(max_length=150, unique=True, verbose_name='Name'),
        ),
    ]
