from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from .models import CustomUser, WorkInquiry, FranchiseInquiry


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'name', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'is_superuser', 'groups')
    search_fields = ('email', 'name')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name', 'mobile_no')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active',
         'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'mobile_no', 'password1', 'password2', 'is_staff', 'is_active')}
         ),
    )


@admin.register(WorkInquiry)
class WorkInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'service', 'company_name', 'email', 'submitted_at')
    search_fields = ('name', 'company_name', 'email', 'service')
    list_filter = ('service', 'submitted_at')


@admin.register(FranchiseInquiry)
class FranchiseInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile_no',
                    'country', 'state', 'submitted_at')
    search_fields = ('name', 'email', 'mobile_no', 'country', 'state')
    list_filter = ('country', 'state', 'submitted_at')


admin.site.register(CustomUser, CustomUserAdmin)
