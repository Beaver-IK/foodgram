from django.shortcuts import get_object_or_404, redirect

from api.models import RecipeShortLink


def redirect_to_original(request, short_code):
    """
    Перенаправляет пользователя с короткой ссылки на оригинальный URL.
    """
    link = get_object_or_404(RecipeShortLink, short_code=short_code)
    return redirect(link.original_url)
