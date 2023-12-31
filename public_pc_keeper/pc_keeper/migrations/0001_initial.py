# Generated by Django 4.2.7 on 2023-11-06 09:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(blank=True, default='')),
                ('seat', models.CharField(blank=True, default='', max_length=200)),
                ('status', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '피씨',
                'verbose_name_plural': '피씨',
                'db_table': 'pc',
            },
        ),
        migrations.CreateModel(
            name='UseHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(default='', max_length=100)),
                ('password', models.CharField(max_length=4)),
                ('start_at', models.DateTimeField(auto_now_add=True)),
                ('end_at', models.DateTimeField(auto_now=True)),
                ('status', models.BooleanField(default=True)),
                ('pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pc_keeper.pc')),
            ],
            options={
                'verbose_name': '사용 이력',
                'verbose_name_plural': '사용 이력',
                'db_table': 'use_history',
            },
        ),
    ]
