# Generated by Django 4.2.5 on 2023-11-30 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('oauth_app', '0002_myuser_american_food_myuser_asian_food_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurant',
            name='place_id',
            field=models.CharField(blank=True, default='default', max_length=255, null=True, unique=True),
        ),
    ]