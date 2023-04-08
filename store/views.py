from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .utils import *
from .models import *
from .forms import *

def main(request):

    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/main.html', context)

def cart(request):
    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/checkout.html', context)

def categories(request):
    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/categories.html', context)

def liked(request):
    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/liked.html', context)

def profile(request):
    context = {}
    context = get_user_context(context,request)
    return render(request, 'store/profile.html', context)


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'store/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = {"title": "Register"}
        context = get_user_context(context,self.request)
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
        context = get_user_context(context,self.request)
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
    context = get_user_context(context,request)
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
    context = get_user_context(context,request)
    context["gender_selected"] = gender
    context["cat_selected"] = cat
    return render(request, 'store/category.html', context)


def add_to_cart(request, product_slug):
    if not request.user.is_authenticated:
        #messages.info(request, "This item was added to your cart.")
        return redirect("login")
    product = Product.objects.get(slug=product_slug)
    order_product, created = OrderProduct.objects.get_or_create(
        product=product,
        user=request.user,
    )
    order_qs = Order.objects.filter(user=request.user)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__slug=product.slug).exists():
            order_product.quantity += 1
            order_product.save()
            #messages.info(request, "This item quantity was updated.")
            return redirect("main")
        else:
            order.products.add(order_product)
            return redirect("main")
    else:
        order = Order.objects.create(user=request.user)
        order.products.add(order_product)
        #messages.info(request, "This item was added to your cart.")
        return redirect("main")

def change_quantity(request, order_product_pk, plus):
    order_product = OrderProduct.objects.get(pk=order_product_pk)
    if plus:
        order_product.quantity += 1
    else:
        order_product.quantity -= 1
        if order_product.quantity == 0:
            order_product.delete()
    order_product.save()
    return redirect("cart")
