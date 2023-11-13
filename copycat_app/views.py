from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
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


def paginate(objects_list, request, per_page=10):
    pages = Paginator(objects_list, per_page)
    page_number = request.GET.get('page')
    if page_number:
        if page_number.isdigit() and 1 <= int(page_number) <= pages.num_pages:
            return pages.get_page(page_number)
        else:
            raise Http404()
    return pages.get_page(1)


@require_http_methods(["GET"])
def index(request):
    questions = Question.objects.default()
    return render(request, "index.html", {'page': paginate(questions, request, 20)})


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
    return render(request, "index.html", {'page': paginate(questions_, request, 20)})


@require_http_methods(["GET"])
def question(request, question_id):
    question_ = Question.objects.specific(question_id)
    if not question_:
        raise Http404()
    answers = Answer.objects.useful(question_)
    return render(request, "question.html", {'question': question_,
                                             'page': paginate(answers, request, 10)})


@require_http_methods(["GET"])
def hot(request):
    questions = Question.objects.hot()
    return render(request, "index.html", {'page': paginate(questions, request, 20)})


@require_http_methods(["GET", "POST"])
def settings(request):
    return render(request, "settings.html")


def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))


def user(request, username):
    raise Http404()
