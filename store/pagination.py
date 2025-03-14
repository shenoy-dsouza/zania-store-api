from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class CustomPagination(PageNumberPagination):

    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            {
                "pagination": {
                    "count": self.page.paginator.count,
                    "per_page": self.page.paginator.per_page,
                    "total_pages": self.page.paginator.num_pages,
                    "current": self.page.number,
                },
                "data": data,
            }
        )
