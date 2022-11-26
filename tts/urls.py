from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.index, name="index"),
    path('post/ajax/tts', views.speak, name="post_tts"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
