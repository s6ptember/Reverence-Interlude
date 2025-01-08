from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm, UserLoginForm, \
    UserProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from orders.models import Order


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('users:user_login')
    else:
        form = UserRegistrationForm()

    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('users:profile')
            else:
                form.add_error(None, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required(login_url='/users/login')
def user_logout(request):
    logout(request)
    return redirect('users:user_login')


@login_required(login_url='/users/login')
def profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile')
        
    else:
        form = UserProfileForm(instance=user)
    orders = Order.objects.filter(user=user)

    return render(request, 'users/profile.html', {
        'form': form,
        'orders': orders,
    })