from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


# Create your views here.

@require_http_methods(["GET"])
def index(request):
    return render(request, "index.html", {'username': 1})


@require_http_methods(["GET", "POST"])
def signup(request):
    return render(request, "signup.html", {'username': 1})


@require_http_methods(["GET", "POST"])
def login(request):
    return render(request, "login.html")


@require_http_methods(["GET", "POST"])
def ask(request):
    return render(request, "ask.html", {'username': 1})


@require_http_methods(["GET"])
def tag(request, tag_name):
    return render(request, "index.html")


@require_http_methods(["GET"])
def question(request, question_id):
    if question_id.isdigit():
        print("OK")
        return render(request, "question.html", {'question_id': question_id})
    else:
        return HttpResponse("This question does not exist.")


@require_http_methods(["GET"])
def hot(request):
    return render(request, "index.html", {'username': 1})
