from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Feedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True, default=0)
    source_of_visit = models.TextField(max_length=100, null=True, blank=True,)
    received_books = models.TextField(max_length=100, null=True, blank=True,)
    received_kit = models.TextField(max_length=100, null=True, blank=True,)
    message = models.TextField(null=True, blank=True,)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.message[:30]}"
    
class User(AbstractUser):
    branch_location = models.CharField(max_length=100, null=True, blank=True,)
    course_details = models.CharField(max_length=100, null=True, blank=True,)
    enrolment_number = models.CharField(max_length=100, null=True, blank=True,)
    batch_date = models.DateField(null=True, blank=True)
    staff_first_name = models.CharField(max_length=100, null=True, blank=True,)
    staff_last_name = models.CharField(max_length=100, null=True, blank=True,)
    phone_number = models.CharField(unique=True, max_length=10, db_index=True, null=True, blank=True,)

    def __str__(self):
        return self.username
