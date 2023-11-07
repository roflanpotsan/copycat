"""
URL configuration for copycat project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views
# cписок новых вопросов (главная страница) (URL = /)
# cписок “лучших” вопросов (URL = /hot/)
# cписок вопросов по тэгу (URL = /tag/blablabla/)
# cтраница одного вопроса со списком ответов (URL = /question/35/)
# форма логина (URL = /login/)
# форма регистрации (URL = /signup/)
# форма создания вопроса (URL = /ask/)
urlpatterns = [
    path('', views.index, name="index_page"),
    path('signup/', views.signup, name="signup"),
    path('login/', views.login, name="login_page"),
    path('ask/', views.ask, name="question_creation_page"),
    path('tag/<str:tag_name>', views.tag, name="sorted_questions_page"),
    path('question/<str:question_id>', views.question, name="question_page"),
    path('hot/', views.hot, name="top_questions_page")
]
