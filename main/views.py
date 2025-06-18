from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Feedback
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout

@login_required
def home(request):
    # Embed Tally.so with pre-filled user data using query params
    return render(request, 'home.html', {
        'user': request.user,
    })

@login_required
def feedback_list(request):
    feedbacks = Feedback.objects.all().order_by('-created_at')
    return render(request, 'feedback_list.html', {'feedbacks': feedbacks})

def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
def tally_webhook(request):
    print('WEBHOOK CALLED-----------')
    if request.method == 'POST':
        data = json.loads(request.body)
        fields = data.get('data', {}).get('fields', [])
        email = None
        message = None

        # Extract email and message from fields
        for field in fields:
            label = field.get('label', '').lower()
            if label == 'email':
                email = field.get('value')
            elif label == 'feedback':  # or check for empty label if it's unnamed
                message = field.get('value')
            elif label == '':  # If label is empty, assume it's the feedback
                message = field.get('value')

        if email and message:
            try:
                user = User.objects.get(email=email)
                obj = Feedback.objects.create(user=user, message=message)
                obj.save()
                print("Feedback saved:", obj)
            except User.DoesNotExist:
                print("User not found.")
        
        return JsonResponse({'status': 'success'})