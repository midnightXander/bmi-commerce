from django.shortcuts import render



def index(request):
    return render(request,"core/index.html")

def products(request):
    return render(request,"core/products.html")

def services(request):
    return render(request, "core/services.html")

def product(request, id):
    return render(request,"core/product.html")

