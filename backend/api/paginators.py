from rest_framework.pagination import PageNumberPagination


class LimitSizePagination(PageNumberPagination):
    """Пагинатор с параметром limit и size"""

    page_size_query_param = 'limit'
    page_size = 6