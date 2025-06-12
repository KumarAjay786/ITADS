from django.urls import path, re_path
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.generic import TemplateView
from .views import (
    CustomTokenObtainPairView, logout_view,
    get_all_users, manage_user, user_profile,
    submit_work_inquiry, get_all_work_inquiries, manage_work_inquiry,
    submit_franchise_inquiry, get_all_franchise_inquiries, manage_franchise_inquiry,
    frontend, frontend_page, forgot_password_view, reset_password_view, change_password, serve_reset_html,
)

urlpatterns = [
    # JWT Auth
    path('api/token/', CustomTokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/logout/', logout_view, name='logout'),
    path('api/change-password/', change_password, name='change-password'),
    path('api/forgot-password/', forgot_password_view, name='forgot_password'),

    # Reset password endpoints
    path('api/reset-password/<uidb64>/<token>/',
         reset_password_view, name='reset_password'),
    
    # Serve reset password page
    path('reset-password/<uidb64>/<token>/',
         serve_reset_html, name='serve_reset_html'),

    # User Endpoints
    path('api/users/', get_all_users, name='get_all_users'),
    path('api/users/<int:user_id>/', manage_user, name='manage_user'),
    path('api/profile/', user_profile, name='user_profile'),

    # Work Inquiry
    path('api/work-inquiries/submit/',
         submit_work_inquiry, name='submit_work_inquiry'),
    path('api/work-inquiries/', get_all_work_inquiries,
         name='get_all_work_inquiries'),
    path('api/work-inquiries/<int:inquiry_id>/',
         manage_work_inquiry, name='manage_work_inquiry'),

    # Franchise Inquiry
    path('api/franchise-inquiries/submit/',
         submit_franchise_inquiry, name='submit_franchise_inquiry'),
    path('api/franchise-inquiries/', get_all_franchise_inquiries,
         name='get_all_franchise_inquiries'),
    path('api/franchise-inquiries/<int:inquiry_id>/',
         manage_franchise_inquiry, name='manage_franchise_inquiry'),

    # Frontend Fallbacks
    path('', frontend, name='frontend'),

    # Only one catch-all, after all specific routes
    re_path(r'^(?P<page>[\w\-/]+?)(?:\.html)?/?$',
            frontend_page, name='frontend_page'),
]
