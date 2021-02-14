from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    # auth and registration
    path('auth/', include('dj_rest_auth.urls')),
    path(
        'auth/registration/',
        include('dj_rest_auth.registration.urls')),

    path('posts/', views.PostList.as_view(), name='all'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name='detail'),
    path('posts/<int:pk>/like/', views.like, name='like'),
    path('posts/<int:pk>/unlike/', views.unlike, name='unlike'),

    path('analytics/', views.analytics, name='analytics'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
