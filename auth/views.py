from django.contrib.auth.models import Group, User, Permission
from rest_framework.permissions import IsAuthenticated
from django.contrib.contenttypes.models import ContentType
from rest_framework import permissions, viewsets, views, status
from rest_framework.response import Response
from rest_framework.authentication import authenticate
from rest_framework.decorators import api_view, action
from .serializers import (GroupSerializer, 
                            UserSerializer, 
                            LoginSerializer, 
                            RegisterSerializer,
                            ContentTypeSerializer,
                            PermissionSerializer
                        )
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """

    queryset = Group.objects.all().order_by("name")
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class ContentTypeView(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        content_types = ContentType.objects.all()
        serializer = ContentTypeSerializer(content_types, many=True)
        return Response(serializer.data)

class PermissionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=["post"])
    def assign_group(self, request):
        group = request.data.get("group")
        permissions = request.data.get("permissions", [])

        if not group or not permissions:
            return Response(
                {"message": "group and permissions are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            group_obj = Group.objects.get(name=group)
        except Group.DoesNotExist:
            return Response(
                {"message": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        permission_objs = Permission.objects.filter(
            codename__in=permissions
        )

        group_obj.permissions.add(*permission_objs)

        return Response(
            {
                "message": "Permissions assigned successfully",
                "group": group,
                "permissions": list(permission_objs.values_list("codename", flat=True))
            },
            status=status.HTTP_200_OK
        )

    @action(detail=False, methods=["post"])
    def remove_group(self, request):
        group = request.data.get("group")
        permissions = request.data.get("permissions", [])

        if not group or not permissions:
            return Response(
                {"message": "group and permissions are required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            group_obj = Group.objects.get(name=group)
        except Group.DoesNotExist:
            return Response(
                {"message": "Group not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        permission_objs = Permission.objects.filter(
            codename__in=permissions
        )

        group_obj.permissions.remove(*permission_objs)

        return Response(
            {
                "message": "Permissions removed successfully",
                "group": group,
                "permissions": list(permission_objs.values_list("codename", flat=True))
            },
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
def assign_group(request):
    user_id = request.data.get('user_id')
    group_id = request.data.get('group_id')

    if not user_id or not group_id:
        return Response(
            {"message": "user_id and group_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response(
            {"message": "User not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    try:
        group = Group.objects.get(id=group_id)
    except Group.DoesNotExist:
        return Response(
            {"message": "Group not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    user.groups.add(group)

    return Response(
        {
            "message": "Group assigned successfully",
        },
        status=status.HTTP_200_OK
    )

@api_view(['POST'])
def remove_group(request):
    user_id = request.data.get('user_id')
    group_id = request.data.get('group_id')

    if not user_id or not group_id:
        return Response(
            {"message": "user_id and group_id are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(id=user_id)
        group = Group.objects.get(id=group_id)
    except User.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
    except Group.DoesNotExist:
        return Response({"message": "Group not found"}, status=status.HTTP_404_NOT_FOUND)

    if not user.groups.filter(id=group_id).exists():
        return Response(
            {"message": "User is not assigned to this group"},
            status=status.HTTP_404_NOT_FOUND
        )

    user.groups.remove(group)

    return Response(
        {"message": "Group removed successfully"},
        status=status.HTTP_200_OK
    )
    
class LoginView(views.APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        user = authenticate(username=username, password=password)

        if user is None:
            return Response(
                {"message": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if not user.is_active:
            return Response(
                {"message": "User is not active"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response({
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        })

class RegisterView(views.APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data

        user = User.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
        )

        group, created = Group.objects.get_or_create(name="User")
        user.groups.add(group)

        return Response(
            {
                "message": "User registered successfully",
                "user": {
                    "id": str(user.id),
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status=status.HTTP_201_CREATED
        )
                



