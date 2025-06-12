from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import WorkInquiry, FranchiseInquiry
from .utils import handle_user_creation_and_email
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()

@receiver(post_save, sender=WorkInquiry)
def handle_work_inquiry(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        full_name = instance.name

        # Admin Email
        admin_html = f"""
        <p><strong>New Work Inquiry Received</strong></p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
            <tr><td><strong>Company Name</strong></td><td>{instance.company_name}</td></tr>
            <tr><td><strong>Name</strong></td><td>{instance.name}</td></tr>
            <tr><td><strong>Designation</strong></td><td>{instance.designation}</td></tr>
            <tr><td><strong>Mobile No</strong></td><td>{instance.mobile_no}</td></tr>
            <tr><td><strong>Email</strong></td><td>{instance.email}</td></tr>
            <tr><td><strong>Country</strong></td><td>{instance.country}</td></tr>
            <tr><td><strong>State</strong></td><td>{instance.state}</td></tr>
            <tr><td><strong>District</strong></td><td>{instance.district}</td></tr>
            <tr><td><strong>Service</strong></td><td>{instance.get_service_display()}</td></tr>
            <tr><td><strong>Description</strong></td><td>{instance.description}</td></tr>
        </table>
        """

        send_mail(
            subject="New Work Inquiry Received",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=admin_html,
            fail_silently=False,
        )

        # User Email and Creation
        user_msg = (
            "Thank you for submitting your work inquiry form.\n"
            "We have received your request and will get in touch with you soon."
        )
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': full_name,
                'password': get_random_string(12)
            }
        )
        
        # Associate inquiry with user
        instance.user = user
        instance.save()
        
        # Send email with credentials if user was just created
        if created:
            user_msg += f"\n\nLogin Credentials:\nUsername: {email}\nPassword: {user.password}"
            user.set_password(user.password)  # Hash the password
            user.save()
        
        try:
            send_mail(
                subject="Thank You for Your Submission",
                message=user_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to {email}: {e}")


@receiver(post_save, sender=FranchiseInquiry)
def handle_franchise_inquiry(sender, instance, created, **kwargs):
    if created:
        email = instance.email
        full_name = instance.name

        # Admin Email
        admin_html = f"""
        <p><strong>New Franchise Inquiry Received</strong></p>
        <table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse;">
            <tr><td><strong>Name</strong></td><td>{instance.name}</td></tr>
            <tr><td><strong>Mobile No</strong></td><td>{instance.mobile_no}</td></tr>
            <tr><td><strong>Email</strong></td><td>{instance.email}</td></tr>
            <tr><td><strong>Country</strong></td><td>{instance.country}</td></tr>
            <tr><td><strong>State</strong></td><td>{instance.state}</td></tr>
            <tr><td><strong>District</strong></td><td>{instance.district}</td></tr>
            <tr><td><strong>Address</strong></td><td>{instance.address}</td></tr>
            <tr><td><strong>Message</strong></td><td>{instance.message}</td></tr>
        </table>
        """

        send_mail(
            subject="New Franchise Inquiry Received",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=admin_html,
            fail_silently=False,
        )

        # User Email and Creation
        user_msg = (
            "Thank you for submitting your franchise inquiry.\n"
            "We will review your request and contact you shortly."
        )
        
        # Get or create user
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'name': full_name,
                'password': get_random_string(12)
            }
        )
        
        # Associate inquiry with user
        instance.user = user
        instance.save()
        
        # Send email with credentials if user was just created
        if created:
            user_msg += f"\n\nLogin Credentials:\nUsername: {email}\nPassword: {user.password}"
            user.set_password(user.password)  # Hash the password
            user.save()
        
        try:
            send_mail(
                subject="Thank You for Your Submission",
                message=user_msg,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email to {email}: {e}")
