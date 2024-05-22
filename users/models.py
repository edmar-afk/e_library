from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.

now = timezone.now()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=250)
   
    def __str__(self):
        return self.user.username
    
class Classroom(models.Model):
    class_name = models.CharField(max_length=250)
    section = models.CharField(max_length=250)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='instructor')
    students = models.ManyToManyField(User)
    
    def verify_room_code(self, entered_room_code):
        """
        Verify if the entered room code matches the classroom's room code.
        """
        return self.room_code == entered_room_code
    
class Lesson(models.Model):
    title = models.CharField(max_length=1000)
    description = models.TextField()
    lesson_file = models.FileField(upload_to='media/',blank=True, null=True, validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'docx', 'ppt', 'xls', 'mp3', 'mp4'])])
    teacher = models.ForeignKey(User, on_delete=models.CASCADE)
    date_posted = models.DateTimeField(default=now)
    
class Forum(models.Model):
    title = models.CharField(max_length=10000)
    type = models.CharField(max_length=250)
    file = models.FileField(
        upload_to='media/forum',
        validators=[ 
            FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'pdf', 'word', 'ppt', 'xlsx', 'csv', 'gif'])
        ],
        null=True,  # Allow null values
        blank=True  # Also allow empty values (in forms)
    )
    upload_date = models.DateTimeField(default=now)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)

class Comments(models.Model):
    post = models.ForeignKey(Forum, on_delete=models.CASCADE)
    commentors = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=now)
