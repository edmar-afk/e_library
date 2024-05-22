# Generated by Django 5.0.4 on 2024-05-17 12:25

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_classroom_room_code_remove_classroom_subject_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='comment_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 12, 25, 29, 527293, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='forum',
            name='upload_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 12, 25, 29, 527293, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='date_posted',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 17, 12, 25, 29, 527293, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_file',
            field=models.FileField(blank=True, null=True, upload_to='media/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'docx', 'ppt', 'xls', 'mp3', 'mp4'])]),
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='profile_pics/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
