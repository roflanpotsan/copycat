from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods


# Create your views here.

@require_http_methods(["GET"])
def index(request, context):
    return render(request, "index.html", {'username': context})


@require_http_methods(["GET", "POST"])
def signup(request):
    return HttpResponse("REGISTER AMOGUS")


@require_http_methods(["GET", "POST"])
def login(request):
    return HttpResponse("LOGIN AMOGUS")


@require_http_methods(["GET", "POST"])
def ask(request):
    return HttpResponse("ASK AMOGUS")


@require_http_methods(["GET"])
def tag(request, tag_name):
    return HttpResponse(f"TAG IS {tag_name} AMOGUS")


@require_http_methods(["GET"])
def question(request, question_id):
    if question_id.isdigit():
        print("OK")
        return HttpResponse(f"QUESTION {question_id} AMOGUS")
    else:
        return HttpResponse("This question does not exist.")


@require_http_methods(["GET"])
def hot(request):
    return HttpResponse("HOT AMOGUS")
