# Generated by Django 5.1.5 on 2025-01-21 14:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Follower',
                'verbose_name_plural': 'Followers',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['follower'], name='relationshi_followe_6e5373_idx'), models.Index(fields=['following'], name='relationshi_followi_1d2046_idx')],
                'unique_together': {('follower', 'following')},
            },
        ),
        migrations.CreateModel(
            name='UserAction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.CharField(choices=[('HIDE', 'Hide'), ('BLOCK', 'Block')], max_length=5)),
                ('status', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('target_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_received', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='actions_performed', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Action',
                'verbose_name_plural': 'User Actions',
                'ordering': ['-created_at'],
                'indexes': [models.Index(fields=['user'], name='relationshi_user_id_f2a188_idx'), models.Index(fields=['target_user'], name='relationshi_target__d0a737_idx'), models.Index(fields=['action'], name='relationshi_action_aa130c_idx')],
                'unique_together': {('user', 'target_user', 'action')},
            },
        ),
    ]
