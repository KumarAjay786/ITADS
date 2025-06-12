from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from api.models import WorkInquiry, FranchiseInquiry


class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return [
            'frontend',  # Homepage
            'frontend_page',  # This will handle all other static pages
        ]

    def location(self, item):
        if item == 'frontend':
            return reverse(item)
        # For other pages, we'll use the frontend_page view with the page parameter
        return reverse('frontend_page', kwargs={'page': item})


class HighPrioritySitemap(Sitemap):
    priority = 0.9
    changefreq = 'weekly'

    def items(self):
        return [
            'about-us',
            'contact-us',
            'our-vision-mission',
            'our-management',
            'our-clients',
            'group-of-company',
            'more-pragathi',
            'gallery'
        ]

    def location(self, item):
        return reverse('frontend_page', kwargs={'page': item})


class ServicesSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return [
            'web-solutions',
            'software-development',
            'social-media-marketing',
            'services-to-education-institutions',
            'radio-jungle',
            'public-relation',
            'product-activation',
            'printing-services',
            'print-media',
            'payroll-services',
            'outdoor-branding',
            'mobile-promotions',
            'liaison-services',
            'internship-services',
            'hr-consultency',
            'full-time-staffing',
            'events-exhibitions',
            'financial-service',
            'education-consultency',
            'direct-marketing',
            'digital-marketing',
            'corporate-gifting',
            'contract-staffing',
            'broadcasting-management',
            'app-development',
            'accounting-audit',
            '3d-design',
            '2d-design',
            'branding',
            'bellow-the-line'
        ]

    def location(self, item):
        return reverse('frontend_page', kwargs={'page': item})


class WorkInquirySitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        # Only approved Work Inquiries should be in sitemap for SEO
        return WorkInquiry.objects.filter(status='approved')

    def location(self, item):
        # Since we don't have individual pages for inquiries, we'll point to the work inquiries list
        return reverse('frontend_page', kwargs={'page': 'work-inquiries'})

    def lastmod(self, obj):
        return obj.submitted_at


class FranchiseInquirySitemap(Sitemap):
    priority = 0.6
    changefreq = 'weekly'

    def items(self):
        # Only approved Franchise Inquiries should be in sitemap for SEO
        return FranchiseInquiry.objects.filter(status='approved')

    def location(self, item):
        # Since we don't have individual pages for inquiries, we'll point to the franchise inquiries list
        return reverse('frontend_page', kwargs={'page': 'franchise-inquiries'})

    def lastmod(self, obj):
        return obj.submitted_at
