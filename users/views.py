from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.shortcuts import render, redirect
from django.views.generic import FormView, CreateView
from django.views import generic
from braces.views import SelectRelatedMixin
from django.contrib.auth.models import User
from . import forms


class Dashboard(
    LoginRequiredMixin,
    SelectRelatedMixin,
    generic.DetailView
):
    model = User
    select_related = ('thoughts',)
    template_name = 'users/dashboard.html'

    def get_object(self, queryset=None):
        return self.request.user

class LogoutView(LoginRequiredMixin, FormView):
    form_class = forms.LogoutForm
    template_name = 'users/logout.html'

    def form_valid(self, form):
        if self.request.POST.get("nope"): #neste caso, o usuario mudou de ideia e nao fara logout
            return HttpResponseRedirect(reverse('home'))
        else:
            logout(self.request) #neste caso, o usuario confirma o desejo de fazer logout
            return HttpResponseRedirect(reverse('home'))

class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = 'users/signup.html'
    success_url = reverse_lazy('users:login') #direciona de Signup para Login



