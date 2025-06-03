from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from biometric_auth.views import home

extra_data = None  # Global temp storage

def login_view(request):
    global extra_data
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)

            # Apply extra data if available
            if extra_data:
                user.email = extra_data.get('email', '')
                user.first_name = extra_data.get('first_name', '')
                user.last_name = extra_data.get('last_name', '')
                user.save()
                extra_data = None  # clear it

            return redirect("home")  # or redirect('home') if preferred

    return render(request, 'login.html')


def register_view(request):
    global extra_data
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            # Collect extra fields from the form
            extra_data = {
                'email': request.POST.get('email'),
                'first_name': request.POST.get('first_name'),
                'last_name': request.POST.get('last_name')
            }

            # Manual login after registration
            username = request.POST.get('username')
            password = request.POST.get('password1')  # Use 'password1' here

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

                # Apply extra data here too
                user.email = extra_data.get('email', '')
                user.first_name = extra_data.get('first_name', '')
                user.last_name = extra_data.get('last_name', '')
                user.save()
                extra_data = None
                return home(request)

            return redirect('login')  # fallback

    else:
        form = UserCreationForm()

    return render(request, 'register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')  # or wherever you want
