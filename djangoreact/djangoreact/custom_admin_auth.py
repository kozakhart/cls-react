# admin_views.py
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from knox.models import AuthToken
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login as auth_login
from axes.decorators import axes_dispatch
from axes.signals import user_login_failed
from axes.utils import reset

@axes_dispatch
def custom_admin_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = form.get_user()
            user = authenticate(request, username=username, password=password)

            if user is not None:
                # Authentication succeeded - Customize your token creation logic here
                try:
                    # Your token creation logic using Knox or any other method
                    # Example: Generate token and set cookie
                    token_tuple = AuthToken.objects.create(user=user)
                    token, _ = token_tuple
                    auth_login(request, user)
                    response = redirect('/admin/')  # Redirect to the admin site
                    # Set cookie or any other necessary response modifications
                    response.set_cookie(key='token', value=f'{token.token_key}:{user.username}', httponly=True, secure=True)
                    return response
                except Exception as e:
                    print(e)
                    return HttpResponse('Token authentication error', status=401)
            else:
                # Authentication failed
                user_login_failed.send(
                    sender=__name__,
                    credentials={'username': username},
                    request=request
                )
                return HttpResponse('Invalid credentials', status=400)
    else:
        # For GET requests, render the admin login form
        form = AuthenticationForm(request)
    
    context = {
        'form': form,
        'app_path': request.get_full_path(),
        'next': request.get_full_path(),
    }
    return render(request, 'admin/login.html', context)

def custom_admin_logout(request):
    response = redirect('/admin/login/')  # Redirect to the admin login page after logout

    # Delete the token cookie by setting an empty value and expiring it
    response.set_cookie('token', '', max_age=0)
    response.set_cookie('sessionid', '', max_age=0)

    return response
