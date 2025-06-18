from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Feedback

User = get_user_model()  # ✅ Get the custom user model

@admin.register(User)  # ✅ Register the actual model, not the admin class
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        ("Extra Info", {
            "fields": (
                "branch_location",
                "course_details",
                "enrolment_number",
                "batch_date",
                "staff_first_name",
                "staff_last_name",
            )
        }),
    )

    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ("Extra Info", {
            "fields": (
                "branch_location",
                "course_details",
                "enrolment_number",
                "batch_date",
                "staff_first_name",
                "staff_last_name",
            )
        }),
    )

    list_display = (
        "username",
        "email",
        "branch_location",
        "course_details",
        "enrolment_number",
    )

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        "user", "rating", "source_of_visit",
        "received_books", "received_kit"
    )
    search_fields = ("user__username", "user__email")
    list_filter = ("rating", "source_of_visit", "received_books", "received_kit")
