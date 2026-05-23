# core/context_processors.py
from django.utils import translation

def language_processor(request):
    """Make current language available to all templates"""
    return {
        'current_language': translation.get_language(),
    }