from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Feedback, User
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
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
    if request.method != 'POST':
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

    try:
        data = json.loads(request.body)
        fields = data.get('data', {}).get('fields', [])

        field_lookup = {
            field.get('label', '').strip().lower(): field
            for field in fields if 'label' in field
        }

        def get_value(label, default=None):
            field = field_lookup.get(label.strip().lower())
            return field.get('value') if field else default

        def get_option_text(label):
            field = field_lookup.get(label.strip().lower())
            if not field:
                return None
            values = field.get('value', [])
            if not values or not isinstance(values, list):
                return None
            selected_id = values[0]
            return next((opt['text'] for opt in field.get('options', []) if opt['id'] == selected_id), None)

        phone = get_value('phone_number')
        if not phone:
            return JsonResponse({'error': 'Phone number not provided'}, status=400)

        try:
            user = User.objects.get(phone_number=phone)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

        feedback = Feedback.objects.create(
            user=user,
            rating=int(get_value('how was the counselling?', 0)),
            source_of_visit=get_option_text('source of visit'),
            received_books=get_option_text('did you receive all the course books?'),
            received_kit=get_option_text('did you receive the bag &amp; id card?'),
            message=get_value('any suggestions'),
        )

        return JsonResponse({'status': 'success', 'id': feedback.id})

    except Exception as e:
        return JsonResponse({'error': f'Internal error: {str(e)}'}, status=500)