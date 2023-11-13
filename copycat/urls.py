from copycat_app import urls as copycat_app_urls
from django.conf.urls import include

urlpatterns = [
    copycat_app_urls.path('', include(copycat_app_urls))
]
