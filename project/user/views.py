from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        identifier = request.POST.get('identifier')  # It will be username or email
        password = request.POST.get('password')

        # Check if the identifier is an email or username
        if '@' in identifier:
            # Try to get user by email
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                user = None
        else:
            # If it's not an email, treat it as a username
            try:
                user = User.objects.get(username=identifier)
            except User.DoesNotExist:
                user = None

        # Authenticate and log the user in
        if user is not None and user.check_password(password):
            auth_login(request, user)
            return redirect('app:home')  # Redirect to your desired home page
        else:
            messages.error(request, 'Invalid username/email or password')

    return render(request, 'user/login.html')
