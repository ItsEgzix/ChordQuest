# Generated by Django 5.0.4 on 2024-04-24 16:52

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_message_post_init_message_message'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MidiFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='midi_files/')),
                ('name', models.CharField(max_length=100)),
                ('genere', models.CharField(max_length=100)),
                ('key', models.CharField(max_length=100)),
                ('emotion', models.CharField(max_length=100)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
