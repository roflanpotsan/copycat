from django.contrib import admin
from django.urls import path, re_path
from copycat_app import views
from django.conf.urls.static import static, serve
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index_page"),
    path('signup/', views.signup, name="signup_page"),
    path('login/', views.login, name="login_page"),
    path('profile/edit', views.settings, name="settings_page"),
    path('ask/', views.ask, name="question_creation_page"),
    path('tag/<str:tag_name>', views.tag, name="questions_with_tag_page"),
    path('question/<int:question_id>', views.question, name="question_page"),
    path('hot/', views.hot, name="top_questions_page"),
    path('admin/', admin.site.urls, name="admin_panel"),
    path('logout/', views.logout, name="logout_page"),
    path('profile/id/<str:display_name>', views.profile, name="user_profile_page"),
    path('rate/', views.rate, name='api_rate'),
    path('correct/', views.correct, name='api_correct'),
    # re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

handler404 = "copycat_app.views.page_not_found"
