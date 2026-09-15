from pathlib import Path
import uuid
from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from .predictor import predict_image

ALLOWED_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.bmp', '.webp'}
MAX_BYTES = 10 * 1024 * 1024


def home(request):
    return render(request, 'detector/home.html')


@require_http_methods(['POST'])
def predict(request):
    uploaded = request.FILES.get('image')
    if not uploaded:
        return render(request, 'detector/home.html', {'error': 'Please select an endoscopy image first.'})
    if uploaded.size > MAX_BYTES:
        return render(request, 'detector/home.html', {'error': 'Image must be smaller than 10 MB.'})
    if Path(uploaded.name).suffix.lower() not in ALLOWED_EXTENSIONS:
        return render(request, 'detector/home.html', {'error': 'Supported formats: JPG, PNG, BMP and WEBP.'})
    name = f'uploads/{uuid.uuid4().hex}{Path(uploaded.name).suffix.lower()}'
    saved_path = default_storage.save(name, uploaded)
    try:
        with default_storage.open(saved_path, 'rb') as image_file:
            result = predict_image(image_file)
        return render(request, 'detector/home.html', {
            'result': result,
            'image_url': settings.MEDIA_URL + saved_path,
        })
    except Exception as exc:
        return render(request, 'detector/home.html', {
            'error': f'Prediction could not be completed: {exc}',
            'image_url': settings.MEDIA_URL + saved_path,
        })
