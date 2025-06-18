from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('feedbacks/', views.feedback_list, name='feedback_list'),
    path('logout/', views.logout_view, name='logout'),
    path('tally/webhook/', views.tally_webhook, name='tally_webhook'),
]
