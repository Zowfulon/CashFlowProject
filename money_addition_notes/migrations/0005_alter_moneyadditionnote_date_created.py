# Generated by Django 5.1.4 on 2025-01-12 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('money_addition_notes', '0004_alter_moneyadditionnote_date_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='moneyadditionnote',
            name='date_created',
            field=models.DateField(blank=True, null=True, verbose_name='Дата создания записи'),
        ),
    ]