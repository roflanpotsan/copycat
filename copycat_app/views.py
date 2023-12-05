from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.shortcuts import redirect
from django.urls import reverse, resolve
from copycat_app.models import Profile, Question, Answer, Tag, User
from django.core.paginator import Paginator
from django.contrib.auth import logout as log_out, authenticate as auth, login as log_in
from copycat_app.forms import LoginForm, SignupForm, QuestionForm, AnswerForm, ProfileForm
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required


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
@csrf_protect
def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('index_page'))
    if request.method == "GET":
        signup_form = SignupForm()
    if request.method == "POST":
        signup_form = SignupForm(request.POST)
        if signup_form.is_valid():
            new_user = signup_form.save()
            if new_user:
                log_in(request, new_user)
                return redirect(reverse('index_page'))
            else:
                signup_form.add_error(None, "The data provided is invalid")
    return render(request, "signup.html", {"form": signup_form})


@require_http_methods(["GET", "POST"])
@csrf_protect
def login(request):
    if request.user.is_authenticated:
        return redirect(reverse('index_page'))
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = auth(request, **login_form.cleaned_data)
            if user:
                log_in(request, user)
                resolved_path = resolve(request.GET.get('continue', '/'))
                return redirect(resolved_path.url_name, **resolved_path.captured_kwargs)
            else:
                login_form.add_error(None, "Wrong username or password.")
    return render(request, "login.html", {"form": login_form})


def logout(request):
    log_out(request)
    resolved_path = resolve(request.GET.get('continue', '/'))
    return redirect(resolved_path.url_name, **resolved_path.captured_kwargs)


@require_http_methods(["GET", "POST"])
@login_required(redirect_field_name='continue', login_url='/login')
@csrf_protect
def ask(request):
    if request.method == "GET":
        question_form = QuestionForm()
    if request.method == "POST":
        question_form = QuestionForm(request.POST)
        if question_form.is_valid():
            new_question = question_form.save(request.user.profile)
            return redirect('question_page', question_id=new_question.id)
    return render(request, "ask.html", {"form": question_form})


@require_http_methods(["GET"])
def tag(request, tag_name):
    questions_ = Question.objects.have_tags([tag_name])
    return render(request, "index.html", {'page': paginate(questions_, request, 20)})


@require_http_methods(["GET", "POST"])
def question(request, question_id):
    question_ = Question.objects.specific(question_id)
    if request.method == "GET":
        if not question_:
            raise Http404()
        answers = Answer.objects.useful(question_)
        answer_form = AnswerForm()
    if request.method == "POST":
        if request.user.is_authenticated:
            answers = Answer.objects.useful(question_)
            answer_form = AnswerForm(request.POST)
            if answer_form.is_valid():
                answer = answer_form.save(request.user.profile, question_)
                return redirect((reverse(question, kwargs={'question_id': question_id})) + f'?page={len(answers) // 10 + 1}#ans{answer.id - 1}')
            else:
                answer_form.add_error(None, "Invalid input.")
        else:
            return redirect('question_page', question_id=question_id)

    return render(request, "question.html", {'question': question_,
                                             'page': paginate(answers, request, 10),
                                             'form': answer_form})


@require_http_methods(["GET"])
def hot(request):
    questions = Question.objects.hot()
    return render(request, "index.html", {'page': paginate(questions, request, 20)})


@require_http_methods(["GET", "POST"])
@csrf_protect
@login_required(redirect_field_name='continue', login_url='/login')
def settings(request):
    if request.method == "GET":
        profile_form = ProfileForm()
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, request.FILES)
        print(request.FILES)
        if profile_form.is_valid():
            profile_form.save(request.user)
    return render(request, "settings.html", {'form': profile_form})


def page_not_found(request, exception):
    return HttpResponseNotFound(render(request, '404.html'))


def profile(request, username):
    raise Http404()
