from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from .sitemaps import (
    StaticViewSitemap,
    HighPrioritySitemap,
    ServicesSitemap,
    WorkInquirySitemap,
    FranchiseInquirySitemap
)

sitemaps = {
    'static': StaticViewSitemap,
    'high_priority': HighPrioritySitemap,
    'services': ServicesSitemap,
    'work_inquiries': WorkInquirySitemap,
    'franchise_inquiries': FranchiseInquirySitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),  # All frontend routes
]
urlpatterns += [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
]
