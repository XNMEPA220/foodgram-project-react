from rest_framework.pagination import PageNumberPagination


class MyPagination(PageNumberPagination):
    """Собственный пагинатор, для установки лимита пользователями."""

    page_size_query_param = 'limit'
    page_size = 6
