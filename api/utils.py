from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string

User = get_user_model()


def handle_user_creation_and_email(full_name, email, message):
    if not email:
        return

    email = email.strip().lower()
    full_name = full_name.strip() if full_name else ""

    if not User.objects.filter(email=email).exists():

        password = get_random_string(
            length=12,
            allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
        )

        user = User.objects.create_user(

            email=email,
            password=password,
            name=full_name
        )

        message += f"\n\nLogin Credentials:\nUsername: {email}\nPassword: {password}"

    try:
        send_mail(
            subject="Thank You for Your Submission",
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Error sending email to {email}: {e}")
