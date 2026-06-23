from rest_framework import permissions, viewsets
from rest_framework import filters
# from rest_framework.decorators import api_view
from .serializers import CallSerializer
from .models import Call
from .pagination import CustomPagination
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CallFilter

class CallViewSet(viewsets.ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter,  filters.SearchFilter,]
    filterset_class = CallFilter
    ordering_fields = ['id', 'callerName', 'callStartTime', 'callEndTime', 'callDuration', 'callCost']
    search_fields = ['callerName', 'city', 'callerNumber', 'receiverNumber']
    ordering = ['-callStartTime']