from rest_framework.pagination import PageNumberPagination

from core.constants import PAGE_SIZE


class PageLimitPagination(PageNumberPagination):
    page_size = PAGE_SIZE
    page_size_query_param = 'limit'
