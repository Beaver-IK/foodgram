from django.contrib import admin
from django.urls import path, include

from foodgram.views import redirect_to_original

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',  include('api.urls')),
    path('s/<str:short_code>', redirect_to_original, name='redirect'),
]
