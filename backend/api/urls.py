from django.urls import path, include


urlpatterns = [
    path('users/',  include('users.for_api.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]