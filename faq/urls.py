from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'faq'

urlpatterns = [
    path('', views.index, name='index'),
    #path('create/', views.create_pertanyaan, name='create'),
    path('<int:pertanyaan_id>/delete/', views.delete, name='delete'),
    path('<int:pertanyaan_id>/', views.detail, name='detail'),
    path('<int:pertanyaan_id>/results/', views.results, name='results'),
    path('<int:pertanyaan_id>/vote/', views.vote, name='vote'),
    path('<int:komen_id>/<int:pertanyaan_id>/',
         views.vote_komen, name='vote-komen'),
    path('register/', views.register_request , name='register'),
    path('login/', views.login_request, name='login'),
    path('logout/', views.logout_request, name= 'logout'),
    path('upload/', views.simple_upload, name= 'upload'),
    path('profile/', views.model_form_upload, name= 'profile'),
    path('search/', views.serach_user, name= 'search'),
    path('create/', views.create_post, name= 'create'),
    path('<int:profile_id>/search/', views.search_profile, name= 'search-profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

