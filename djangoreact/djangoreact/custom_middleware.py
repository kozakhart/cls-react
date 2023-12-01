# custom_middleware.py
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse, JsonResponse
from knox.auth import TokenAuthentication
from rest_framework.decorators import authentication_classes
from rest_framework import status
from knox.models import AuthToken
from django.utils import timezone

class CustomAdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path == '/admin/login/':
            return HttpResponseRedirect('/cls/')  # Redirect to your custom login URL
        return self.get_response(request)
    
# custom_middleware.py
class TokenVerificationMiddleware:
    EXCLUDED_URLS = ('/cls/', '/admin/login/')  # URLs excluded from token verification

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not self.should_exclude(request.path):
            if 'token' not in request.COOKIES:
                if not request.path.startswith('/cls/'):
                    return HttpResponseRedirect('/cls/')  # Redirect if token is not present and not in excluded URLs

            token = request.COOKIES.get('token')
            if token:
                try:
                    token, username = token.split(':')
                    auth_token = AuthToken.objects.get(token_key=token, user__username=username)
                    if auth_token and auth_token.user.username == username and auth_token.expiry > timezone.now():
                        return self.get_response(request)  # Continue to the requested view
                    else:
                        if not request.path.startswith('/cls/'):
                            return HttpResponseRedirect('/cls/')  # Redirect if token is invalid and not in excluded URLs
                except AuthToken.DoesNotExist:
                    if not request.path.startswith('/cls/'):
                        return HttpResponseRedirect('/cls/')  # Redirect if token does not exist and not in excluded URLs

        response = self.get_response(request)
        return response

    def should_exclude(self, path):
        return any(path.startswith(url) for url in self.EXCLUDED_URLS)


