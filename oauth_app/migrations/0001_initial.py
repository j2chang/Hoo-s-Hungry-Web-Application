# Generated by Django 4.2.5 on 2023-11-19 00:28

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
            name='myUser',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('userName', models.CharField(max_length=50)),
                ('firstName', models.CharField(max_length=50)),
                ('lastName', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('user_type', models.CharField(choices=[('a', 'Admin'), ('u', 'General')], max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='Restaurant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('place_id', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('star_rating', models.IntegerField(null=True)),
                ('cuisine_type', models.CharField(max_length=50, null=True)),
                ('price_range', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Star',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])),
                ('place_id', models.ForeignKey(db_column='place_id', on_delete=django.db.models.deletion.CASCADE, related_name='stars', to='oauth_app.restaurant', to_field='place_id')),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('review_text', models.CharField(max_length=500)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
                ('is_approved', models.BooleanField(default=False)),
                ('is_reviewed', models.BooleanField(default=False)),
                ('is_rejection_acknowledged', models.BooleanField(default=False)),
                ('status', models.CharField(default='Your submitted review is waiting for approval.', max_length=500)),
                ('place_id', models.ForeignKey(db_column='place_id', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='oauth_app.restaurant', to_field='place_id')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]