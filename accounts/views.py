from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm, AccountForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('url_home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def my_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('url_home')
    else:
        form = AccountForm(instance=request.user)
    return render(request, 'edit_account.html', {'form': form})
