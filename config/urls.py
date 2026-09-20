from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from portfolio.views import home, certificate_view, certificate_file_view, certification_view


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("certificate/<int:certificate_id>/", certificate_view, name="certificate_view"),
    path("certificate/<int:certificate_id>/file/", certificate_file_view, name="certificate_file_view"),
    path("certification/<int:certification_id>/", certification_view, name="certification_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)