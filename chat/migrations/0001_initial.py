# Generated by Django 3.2 on 2021-04-23 15:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_name', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('passwd', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='AppToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('app_token', models.CharField(max_length=200)),
                ('ttl', models.DateTimeField(verbose_name='date published')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.user')),
            ],
        ),
    ]
