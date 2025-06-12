from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser, WorkInquiry, FranchiseInquiry

User = get_user_model()

# JWT Custom Token Serializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the JWT itself (optional)
        token['email'] = user.email
        token['name'] = user.name
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        # Add role to the response (used by frontend)
        data['email'] = self.user.email
        data['name'] = self.user.name
        data['role'] = 'admin' if self.user.is_staff else 'user'

        return data


# Custom User Serializer
class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name', 'mobile_no',
                  'is_active', 'is_staff', 'date_joined']
        read_only_fields = ['is_active', 'is_staff', 'date_joined']


# Work Inquiry Serializer (now handles user creation)
class WorkInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkInquiry
        fields = '__all__'
        read_only_fields = ('user', 'submitted_at')
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'mobile_no': {'required': True}
        }


# Franchise Inquiry Serializer (now handles user creation)
class FranchiseInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = FranchiseInquiry
        fields = '__all__'
        read_only_fields = ('user', 'submitted_at')
        extra_kwargs = {
            'email': {'required': True},
            'name': {'required': True},
            'mobile_no': {'required': True}
        }


class ChangePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def validate(self, data):
        if data['new_password'] != data['confirm_password']:
            raise serializers.ValidationError("New passwords do not match.")
        return data
