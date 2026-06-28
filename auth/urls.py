from django.urls import include, path
from rest_framework import routers
import auth.views as views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"permissions", views.PermissionViewSet, basename="permission")

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('groups/assign/', views.assign_group, name='assign_group'),
    path('groups/remove/', views.remove_group, name='remove_group'),
    path('content_types/', views.ContentTypeView.as_view(), name='content_types'),
    path("", include(router.urls)),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
