# core/middleware.py
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

class LanguageMiddleware(MiddlewareMixin):
    """Middleware to persist language across all pages"""
    
    def process_request(self, request):
        # Check if user is authenticated and has language preference
        if request.user.is_authenticated and hasattr(request.user, 'preferred_language'):
            lang = request.user.preferred_language
            if lang:
                translation.activate(lang)
                request.session['django_language'] = lang
                return
        
        # Check session for language
        lang = request.session.get('django_language')
        if lang:
            translation.activate(lang)
        else:
            # Default to English
            translation.activate('en')