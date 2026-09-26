from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password

from .models import User


def home(request):
    return render(request, 'users/home.html')


def register(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        mobile_number = request.POST.get('phone')
        place = request.POST.get('place')

        # Required field validation
        if not user_name:
            return render(
                request,
                'users/register.html',
                {'error': 'User name is required'}
            )

        if not password:
            return render(
                request,
                'users/register.html',
                {'error': 'Password is required'}
            )

        if not mobile_number:
            return render(
                request,
                'users/register.html',
                {'error': 'Phone number is required'}
            )

        if not place:
            return render(
                request,
                'users/register.html',
                {'error': 'Place is required'}
            )

        # Password confirmation
        if password != confirm_password:
            return render(
                request,
                'users/register.html',
                {'error': 'Passwords do not match'}
            )

        # Check username
        if User.objects.filter(user_name=user_name).exists():
            return render(
                request,
                'users/register.html',
                {'error': 'Username already exists'}
            )

        # Create user
        user = User(
            user_name=user_name,
            password=make_password(password),
            mobile_number=mobile_number,
            place=place
        )

        user.save()

        return redirect('login')

    return render(
        request,
        'users/register.html'
    )


def login_view(request):

    if request.method == 'POST':

        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        if not user_name or not password:
            return render(
                request,
                'users/login.html',
                {
                    'error': 'User name and password are required'
                }
            )

        try:

            user = User.objects.get(
                user_name=user_name
            )

            if check_password(password, user.password):

                request.session['user_id'] = user.id
                request.session['user_name'] = user.user_name

                return redirect('dashboard')

            else:

                return render(
                    request,
                    'users/login.html',
                    {
                        'error': 'Invalid password'
                    }
                )

        except User.DoesNotExist:

            return render(
                request,
                'users/login.html',
                {
                    'error': 'User does not exist'
                }
            )


    return render(
        request,
        'users/login.html'
    )


def dashboard(request):

    if 'user_id' not in request.session:
        return redirect('login')

    try:

        user = User.objects.get(
            id=request.session['user_id']
        )

    except User.DoesNotExist:

        request.session.flush()
        return redirect('login')

    return render(
        request,
        'users/dashboard.html',
        {
            'user': user
        }
    )


def logout_view(request):

    request.session.flush()

    return redirect('home')