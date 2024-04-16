# Generated by Django 4.1 on 2024-03-13 08:50

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('kanji_quiz_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Score',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_score', models.IntegerField()),
                ('question_count', models.IntegerField()),
                ('data_answered', models.DateField(default=django.utils.timezone.now)),
            ],
        ),
    ]
