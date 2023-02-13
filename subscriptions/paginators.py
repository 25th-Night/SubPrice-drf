from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    max_page_size = 20
    page_query_param = 'page'

    def set_page_size(self, page_size):
            self.page_size = page_size