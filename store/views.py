from django.shortcuts import render

def main(request):
    context = {}
    return render(request, 'store/main.html', context)

def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)

def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)

def categories(request):
    context = {}
    return render(request, 'store/categories.html', context)

def liked(request):
    context = {}
    return render(request, 'store/liked.html', context)

def profile(request):
    context = {}
    return render(request, 'store/profile.html', context)