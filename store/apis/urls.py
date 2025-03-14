from django.urls import path
from django.http import FileResponse
from django.views.generic import TemplateView

app_name = "apis"

urlpatterns = [
    # Serve the existing OpenAPI YAML file
    path("api_doc.openapi.yaml", lambda request: FileResponse(open("store/apis/docs/api_doc.openapi.yaml", "rb"), content_type="text/yaml")),

    # Swagger UI (Manually specify schema URL)
    path("docs/", TemplateView.as_view(
        template_name="swagger_ui.html",
        extra_context={"schema_url": "/apis/api_doc.openapi.yaml"}
    ), name="swagger-ui"),
]
