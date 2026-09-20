from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from portfolio.views import home, certificate_view, certificate_file_view, certification_view
from portfolio.sitemaps import PortfolioSitemap


sitemaps = {"portfolio": PortfolioSitemap()}


urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="django-sitemap"),
    path("", home, name="home"),
    path("certificate/<int:certificate_id>/", certificate_view, name="certificate_view"),
    path("certificate/<int:certificate_id>/file/", certificate_file_view, name="certificate_file_view"),
    path("certification/<int:certification_id>/", certification_view, name="certification_view"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
