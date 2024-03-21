from rest_framework.pagination import PageNumberPagination

from backend.constants import PAGE_SIZE


class MyPagination(PageNumberPagination):
    """Собственный пагинатор, для установки лимита пользователями."""

    page_size_query_param = 'limit'
    page_size = PAGE_SIZE
