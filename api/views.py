from django.core.exceptions import ValidationError
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import render
from django.http import HttpResponse, Http404
import os
import json
from django.contrib.auth import update_session_auth_hash
from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.contrib.auth import authenticate
from .models import WorkInquiry, FranchiseInquiry
from .serializers import (
    CustomUserSerializer,
    WorkInquirySerializer,
    FranchiseInquirySerializer,
    CustomTokenObtainPairSerializer,
    ChangePasswordSerializer
)

User = get_user_model()

# --------------------
# JWT Login View
# --------------------


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# --------------------
# Logout View
# --------------------
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        refresh_token = request.data['refresh']
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response({'message': 'Logged out successfully.'}, status=status.HTTP_205_RESET_CONTENT)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


# --------------------
# Work Inquiry Submission (Creates User)
# --------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_work_inquiry(request):
    serializer = WorkInquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # signals will handle user creation + email
        return Response({'message': 'Work Inquiry submitted successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------
# Franchise Inquiry Submission (Creates User)
# --------------------

@api_view(['POST'])
@permission_classes([AllowAny])
def submit_franchise_inquiry(request):
    serializer = FranchiseInquirySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  # signals will handle user creation + email
        return Response({'message': 'Franchise Inquiry submitted successfully.'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------
# Admin: Get All Users
# --------------------
@api_view(['GET'])
@permission_classes([IsAdminUser])
def get_all_users(request):
    users = User.objects.all()
    serializer = CustomUserSerializer(users, many=True)
    return Response(serializer.data)


# --------------------
# Admin: Manage User by ID
# --------------------
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def manage_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted successfully'})


# --------------------
# Logged-In User Profile (GET / PUT)
# --------------------
@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    user = request.user
    if request.method == 'GET':
        serializer = CustomUserSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CustomUserSerializer(
            user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# --------------------
# Get Work Inquiries (User sees only their own, Admin sees all)
# --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_work_inquiries(request):
    user = request.user
    try:
        if user.is_staff:
            # Admin: see all
            inquiries = WorkInquiry.objects.all().order_by('-submitted_at')
        else:
            # User: see only own
            inquiries = WorkInquiry.objects.filter(user=user).order_by('-submitted_at')
        
        serializer = WorkInquirySerializer(inquiries, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching work inquiries: {str(e)}")  # Debug log
        return Response({'error': 'Failed to fetch work inquiries'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------
# Admin: Manage Specific Work Inquiry
# --------------------
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def manage_work_inquiry(request, inquiry_id):
    try:
        inquiry = WorkInquiry.objects.get(id=inquiry_id)
    except WorkInquiry.DoesNotExist:
        return Response({'error': 'Work Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = WorkInquirySerializer(inquiry)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = WorkInquirySerializer(
            inquiry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Work Inquiry updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        inquiry.delete()
        return Response({'message': 'Work Inquiry deleted successfully'})


# --------------------
# Get Franchise Inquiries (User sees only their own, Admin sees all)
# --------------------
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_franchise_inquiries(request):
    user = request.user
    try:
        if user.is_staff:
            # Admin: see all
            inquiries = FranchiseInquiry.objects.all().order_by('-submitted_at')
        else:
            # User: see only own
            inquiries = FranchiseInquiry.objects.filter(user=user).order_by('-submitted_at')
        
        serializer = FranchiseInquirySerializer(inquiries, many=True)
        return Response(serializer.data)
    except Exception as e:
        print(f"Error fetching franchise inquiries: {str(e)}")  # Debug log
        return Response({'error': 'Failed to fetch franchise inquiries'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# --------------------
# Admin: Manage Specific Franchise Inquiry
# --------------------
@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAdminUser])
def manage_franchise_inquiry(request, inquiry_id):
    try:
        inquiry = FranchiseInquiry.objects.get(id=inquiry_id)
    except FranchiseInquiry.DoesNotExist:
        return Response({'error': 'Franchise Inquiry not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = FranchiseInquirySerializer(inquiry)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = FranchiseInquirySerializer(
            inquiry, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Franchise Inquiry updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        inquiry.delete()
        return Response({'message': 'Franchise Inquiry deleted successfully'})


@csrf_exempt
def forgot_password_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            user = User.objects.get(email=email)

            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # Frontend link for reset password with path parameters
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"
            print(f"Generated reset URL: {reset_url}")  # Debug log

            try:
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {reset_url}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(f"Reset email sent successfully to {email}")  # Debug log
                return JsonResponse({'success': True, 'message': 'Password reset email sent.'})
            except Exception as email_error:
                print(f"Failed to send email: {str(email_error)}")  # Debug log
                return JsonResponse({'success': False, 'error': f'Failed to send email: {str(email_error)}'}, status=500)

        except User.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User with this email does not exist.'}, status=400)
        except Exception as e:
            print(f"Error in forgot_password_view: {str(e)}")  # Debug log
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@csrf_exempt
def reset_password_view(request, uidb64, token):
    if request.method == 'GET':
        # Render the reset password page template, pass uidb64 and token to JS
        return render(request, 'reset-password.html', {'uidb64': uidb64, 'token': token})

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_password = data.get('password')

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return JsonResponse({'success': True, 'message': 'Password has been reset successfully.'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid or expired token.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': 'Something went wrong.'}, status=400)

    return JsonResponse({'error': 'Invalid request method.'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    serializer = ChangePasswordSerializer(data=request.data)
    if serializer.is_valid():
        user = request.user
        current_password = serializer.validated_data['current_password']
        new_password = serializer.validated_data['new_password']
        if not user.check_password(current_password):
            return Response({'error': 'Current password is incorrect'}, status=400)
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        return Response({'success': True, 'message': 'Password changed successfully'})
    return Response(serializer.errors, status=400)


# Frontend Views


def frontend(request):
    return render(request, 'index.html')


def frontend_page(request, page):
    safe_page = os.path.basename(page)
    if not safe_page or not all(c.isalnum() or c in ('-', '_') for c in safe_page.replace('.html', '')):
        raise Http404()
    if safe_page.endswith('.html'):
        safe_page = safe_page[:-5]
    static_exts = ('.js', '.css', '.png', '.jpg', '.jpeg', '.gif', '.svg',
                   '.ico', '.map', '.woff', '.woff2', '.ttf', '.eot', '.json')
    if any(safe_page.endswith(ext) for ext in static_exts):
        raise Http404()
    template_name = f"{safe_page}.html"
    return render(request, template_name)


def serve_reset_html(request, uidb64, token):
    try:
        print(f"Serving reset HTML for uidb64: {uidb64}, token: {token}")  # Debug log
        file_path = os.path.join(settings.BASE_DIR, 'frontend', 'reset-password.html')
        print(f"Looking for template at: {file_path}")  # Debug log
        
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Replace the JavaScript to use path parameters instead of query parameters
                content = content.replace(
                    'const uidb64 = getQueryParam("uidb64");',
                    f'const uidb64 = "{uidb64}";'
                ).replace(
                    'const token = getQueryParam("token");',
                    f'const token = "{token}";'
                )
                print("Successfully read and modified reset password template")  # Debug log
                return HttpResponse(content, content_type='text/html')
        else:
            print(f"Template file not found at: {file_path}")  # Debug log
            raise Http404("Reset password page not found")
    except Exception as e:
        print(f"Error serving reset HTML: {str(e)}")  # Debug log
        raise Http404(f"Error serving reset password page: {str(e)}")
