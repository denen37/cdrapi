from django.contrib.auth.models import Group, User, Permission
from django.contrib.contenttypes.models import ContentType
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password


class UserSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    groups = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "groups"]

    def get_id(self, obj):
        return str(obj.id)

    def get_groups(self, obj):
        return [
            {
                "id": str(group.id),
                "name": group.name
            }
            for group in obj.groups.all()
        ]


class GroupSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    permissions = serializers.SerializerMethodField()
    
    class Meta:
        model = Group
        fields = ["id", "name", "permissions"]

    def get_id(self, obj):
        return str(obj.id)

    def get_permissions(self, obj):
        return [
            {
                "id": str(permission.id),
                "codename": permission.codename,
                "name": permission.name
            }
            for permission in obj.permissions.all()
        ]


class ContentTypeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = ContentType
        fields = ["id", "app_label", "model"]

    def get_id(self, obj):
        return str(obj.id)

class PermissionSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Permission
        fields = ["id", "name", "codename"]

    def get_id(self, obj):
        return str(obj.id)

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, 
            required=True, 
            validators=[validate_password]
        )
    password2 = serializers.CharField(write_only=True, 
            required=True
        )
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists")
        return value

    def validate(self, data):
        password = data["password"]

        if password != data["password2"]:
            raise serializers.ValidationError(
                "Passwords do not match"
            )

        return data
