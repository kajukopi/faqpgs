from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('', include('faq.urls')),
    path('admin/', admin.site.urls),
]