# Generated by Django 3.2.5 on 2021-07-28 18:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_profile_user_folllows'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='user_folllows',
        ),
        migrations.AddField(
            model_name='profile',
            name='user_folllows',
            field=models.ForeignKey(blank=True, default=True, on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL),
        ),
    ]