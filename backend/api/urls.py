from django.urls import path, include

urlpatterns = [
    path('users/', include('api.users.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]