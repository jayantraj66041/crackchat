
from django.contrib import admin
from django.urls import path
from datawork import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_signup, name="login_signup"),
    path('home/', views.index, name="home"),
    path('logout/', views.logout, name="logout"),
    path('login/', views.login, name="login"),
    path('post/', views.post, name="post"),
    path('profile/', views.private_profile, name="private_profile"),
    path('user_update/', views.user_update, name="user_update"),
    path('delete_post/<int:p_id>/', views.delete_post, name="delete_post"),
    path('like_dislike/<int:p_id>/', views.like_dislike, name="like_dislike"),
    path('filter_user/<int:u_id>/', views.public_profile, name="filter_user"),
    path('message/', views.message, name="msg"),
    path('message/<int:u_id>/', views.message, name="message"),
    path('send_message/<int:u_id>/', views.send_message, name="send_message")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

