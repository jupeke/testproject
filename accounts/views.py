from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm, AccountForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView


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

'''
Works but replaces by the class approach
def my_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            return redirect('url_home')
    else:
        form = AccountForm(instance=request.user)
    return render(request, 'edit_account.html', {'form': form})
'''
@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email', )
    template_name = 'edit_account.html'
    success_url = reverse_lazy('url_my_account')

    def get_object(self):
        return self.request.user
