from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import PaymentForm, ProfileForm, MyUserForm
from accounts.models import Payment

def login_view(request):
    next_url = request.GET.get('next')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            redirect_url = next_url if next_url else reverse('ticketing:showtime_list')
            return HttpResponseRedirect(reverse('ticketing:showtime_list'))
        else:
            context = {
                'username': username,
                'error': 'کاربری با این مشخصات یافت نشد'
            }
    else:
        context = {}
    return render(request, 'accounts/login.html', context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('accounts:login'))

def Showfullname (request):
    fullname =  request.user.get_full_name()
    return render(request, 'ticketing/base_page.html', {'fullname':fullname})

@login_required
def profile_details(request):
    profile = request.user.profile
    return render(request, 'accounts/profile_details.html', {"profile":profile})


@login_required
def payment_list(request):
    payments = Payment.objects.filter(profile=request.user.profile).order_by('-transaction_time')
    return render(request, 'accounts/payment_list.html', {"payments":payments})


@login_required
def payment_create(request):
    if request.method == 'POST':
        payment_form = PaymentForm(request.POST)
        if payment_form.is_valid():
            # create a payment
            payment = payment_form.save(commit=False)
            # نحوه‌ی کار کامیت به این شکل است که می‌اد از پیمنت یه \یزی می‌سازه
            # ولی سیو نمی‌کنه تا ما پروفایلش رو ست کنیم
            payment.profile = request.user.profile
            payment.save()
            request.user.profile.deposite(payment.amount)
            return HttpResponseRedirect(reverse('accounts:payment_list'))
    else:
        payment_form = PaymentForm()
    context = {
        'payment_form': payment_form
    }
    return render(request, 'accounts/payment_create.html', context)

@login_required
def profile_edit(request):
    if request.method == 'POST':
        user_form = MyUserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, files=request.FILES, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('accounts:profile_details'))
    else:
        user_form = MyUserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'accounts/profile_edit.html', context)