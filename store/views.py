from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import *

from .forms import *

def main(request):

    context = {}
    context = get_user_context(context)
    return render(request, 'store/main.html', context)

def cart(request):
    context = {}
    context = get_user_context(context)
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    context = get_user_context(context)
    return render(request, 'store/checkout.html', context)

def categories(request):
    context = {}
    context = get_user_context(context)
    return render(request, 'store/categories.html', context)

def liked(request):
    context = {}
    context = get_user_context(context)
    return render(request, 'store/liked.html', context)

def profile(request):
    context = {}
    context = get_user_context(context)
    return render(request, 'store/profile.html', context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Register"}
        context = get_user_context(context)
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('main')


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'store/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Login"}
        context = get_user_context(context)
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self):
        return reverse_lazy('main')


def logout_user(request):
    logout(request)
    return redirect('login')


def gender(request, gender_slug):
    gender = Gender.objects.get(slug=gender_slug)
    cats = gender.categories_id.all()
    products = Product.objects.filter(gender=gender)
    context = {
               "cats": cats,
                "products": products
    }
    context = get_user_context(context)
    context["gender_selected"] = gender
    return render(request, 'store/gender.html', context)


def category(request, gender_slug,category_slug):
    gender = Gender.objects.get(slug=gender_slug)
    cat = Category.objects.get(slug=category_slug)
    products = Product.objects.filter(gender=gender, cat=cat)

    cats = gender.categories_id.all()
    context = {
               "cats": cats,
                "products" : products,

    }
    context = get_user_context(context)
    context["gender_selected"] = gender
    context["cat_selected"] = cat
    return render(request, 'store/category.html', context)
