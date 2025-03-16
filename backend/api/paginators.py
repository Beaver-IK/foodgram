from rest_framework.pagination import PageNumberPagination

from api.constants import PAGE_SIZE


class LimitSizePagination(PageNumberPagination):
    """Пагинатор с параметром limit и size"""

    page_size_query_param = 'limit'
    page_size = PAGE_SIZE
