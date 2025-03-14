from django.urls import path
from store.products.views import (
    ProductsListCreateAPIView,
)

app_name = "products"

urlpatterns = [
    path(
        "",
        view=ProductsListCreateAPIView.as_view(),
        name="list-create",
    ),
]
