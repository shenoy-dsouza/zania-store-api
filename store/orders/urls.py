from django.urls import path
from store.orders.views import (
    OrderCreateAPIView,
)

app_name = "orders"

urlpatterns = [
    path(
        "",
        view=OrderCreateAPIView.as_view(),
        name="create",
    ),
]
