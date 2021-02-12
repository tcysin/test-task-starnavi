from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # auth and registration
    path('auth/', include('dj_rest_auth.urls')),
    path(
        'auth/registration/',
        include('dj_rest_auth.registration.urls')),

    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/<int:pk>/like/', views.like),
    path('posts/<int:pk>/unlike/', views.unlike),

    path('analytics/', views.analytics),
]

urlpatterns = format_suffix_patterns(urlpatterns)