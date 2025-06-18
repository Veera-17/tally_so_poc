from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Feedback(models.Model):
    class RatingChoices(models.IntegerChoices):
        ONE = 1, '1 - Poor'
        TWO = 2, '2 - Fair'
        THREE = 3, '3 - Good'
        FOUR = 4, '4 - Very Good'
        FIVE = 5, '5 - Excellent'

    class SourceOfVisitChoices(models.TextChoices):
        GOOGLE = 'Google', 'Google'
        FRIEND = 'Friend', 'Friend'
        SOCIAL_MEDIA = 'Social Media', 'Social Media'
        OTHER = 'Other', 'Other'

    class YesNoChoices(models.TextChoices):
        YES = 'Yes', 'Yes'
        NO = 'No', 'No'
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RatingChoices.choices, null=True, blank=True,)
    source_of_visit = models.CharField(max_length=50, choices=SourceOfVisitChoices.choices, null=True, blank=True,)
    received_books = models.CharField(max_length=3, choices=YesNoChoices.choices, null=True, blank=True,)
    received_kit = models.CharField(max_length=3, choices=YesNoChoices.choices, null=True, blank=True,)
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

    def __str__(self):
        return self.username
