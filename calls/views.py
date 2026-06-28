from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions
from rest_framework import filters
from .serializers import CallSerializer
from .models import Call
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CallFilter
from auth.permissions import IsAdmin, IsAnalyst, IsUser
from rest_framework.decorators import api_view, action
from rest_framework import status
from rest_framework.response import Response
from django.db.models import Sum, Avg

class CallViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, DjangoModelPermissions]
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,  filters.SearchFilter,]
    filterset_class = CallFilter
    ordering_fields = ['id', 'callerName', 'callStartTime', 'callEndTime', 'callDuration', 'callCost']
    search_fields = ['callerName', 'city', 'callerNumber', 'receiverNumber']
    ordering = ['-callStartTime']

    @action(detail=False, methods=["get"])
    def latest(self, request):
        try:
            latest_call = Call.objects.latest("callStartTime")
            serializer = self.get_serializer(latest_call)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Call.DoesNotExist:
            return Response(
                {"message": "No calls found"},
                status=status.HTTP_404_NOT_FOUND
            )

        except Exception as e:
            return Response(
                {"message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    @action(detail=False, methods=["get"])
    def get_start_times(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        start_times = (
            queryset
            .values_list("callStartTime", flat=True)
            .order_by("callStartTime")
        )

        return Response(list(start_times), status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def city_cost(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        city_cost = queryset.values("city", "callCost")

        return Response(list(city_cost), status=status.HTTP_200_OK)

    @action(detail=False, methods=["get"])
    def analytics(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        total_calls = queryset.count()

        total_cost = queryset.aggregate(
            total_cost=Sum("callCost")
        )["total_cost"] or 0

        avg_duration = queryset.aggregate(
            avg_duration=Avg("callDuration")
        )["avg_duration"] or 0

        total_success = queryset.filter(callStatus=True).count()
        total_failed = queryset.filter(callStatus=False).count()

        success_rate = (
            (total_success / total_calls) * 100
            if total_calls > 0 else 0
        )

        return Response({
            "total_calls": total_calls,
            "total_cost": total_cost,
            "avg_duration": round(avg_duration),
            "total_success": total_success,
            "total_failed": total_failed,
            "success_rate": round(success_rate),
        }, status=status.HTTP_200_OK)
