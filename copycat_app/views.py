from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from copycat_app.models import User
from copycat_app.models import Profile, Question, Answer, Tag
from django.core.paginator import Paginator
from django.contrib.auth import logout as log_out
# Create your views here.

# temporary one-time side-block generation
top_users = Profile.objects.top_last_week()
top_tags = Tag.objects.top_last_week()


def paginate(items_, per_page_=20, page_number_=None):
    if not page_number_:
        page_number_ = '1'
    pages = Paginator(items_, per_page_)
    return pages.get_page(page_number_)


@require_http_methods(["GET"])
def index(request):
    questions = Question.objects.default()
    page_number = request.GET.get('page')
    return render(request, "index.html", {'questions': paginate(questions, 20, page_number)})


@require_http_methods(["GET", "POST"])
def signup(request):
    return render(request, "signup.html")


@require_http_methods(["GET", "POST"])
def login(request):
    return render(request, "login.html")


def logout(request):
    log_out(request)
    return index(request)


@require_http_methods(["GET", "POST"])
def ask(request):
    return render(request, "ask.html")


@require_http_methods(["GET"])
def tag(request, tag_name):
    questions_ = Question.objects.have_tags([tag_name])
    page_number = request.GET.get('page')
    return render(request, "index.html", {'questions': paginate(questions_, 20, page_number)})


@require_http_methods(["GET"])
def question(request, question_id):
    question_ = Question.objects.specific(question_id)
    if question_:
        answers = Answer.objects.useful(question_)
        page_number = request.GET.get('page')
        return render(request, "question.html", {
            'question': question_,
            'answers': paginate(answers, 10, page_number)})
    return page_not_found(request, 404)


@require_http_methods(["GET"])
def hot(request):
    questions = Question.objects.hot()
    page_number = request.GET.get('page')
    return render(request, "index.html", {'questions': paginate(questions, 20, page_number)})


@require_http_methods(["GET", "POST"])
def settings(request):
    return render(request, "settings.html")


def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))
