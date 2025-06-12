from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']  # Changed from 'full_name' to 'name'

    def __str__(self):
        return self.email


class WorkInquiry(models.Model):
    SERVICE_CHOICES = [
        ('graphic_designing', 'Graphic Designing'),
        ('web_designing', 'Web Designing'),
        ('portal_development', 'Portal Development'),
        ('digital_marketing', 'Digital Marketing'),
        ('app_development', 'App Development'),
        ('promotional_film_making', 'Promotional Film Making'),
    ]

    # Corrected ForeignKey relationship (removed nested class)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='work_inquiries',
        null=True,  # For existing data compatibility
        blank=True  # For existing data compatibility
    )
    company_name = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    service = models.CharField(max_length=50, choices=SERVICE_CHOICES)
    email = models.EmailField()
    description = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.name} - {self.service}"


class FranchiseInquiry(models.Model):
    # Corrected ForeignKey relationship (removed nested class)
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='franchise_inquiries',
        null=True,  # For existing data compatibility
        blank=True  # For existing data compatibility
    )
    name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=15)
    email = models.EmailField()
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    address = models.TextField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    def __str__(self):
        return f"{self.name} - {self.email}"
