from django.shortcuts import render


def index(request):
    return render(request,"courses/index.html")

def tests(request):
    return render(request,"courses/tests.html")

def courses(request):
    return render(request,"courses/courses.html")

def module(request, test_type, module):
    return render(request,"courses/module.html",{
        'test': test_type,
        'module' : module
    })

def course(request, slug):
    return render(request,"courses/course.html")