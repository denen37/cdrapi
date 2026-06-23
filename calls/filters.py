import django_filters
from .models import Call

class CallFilter(django_filters.FilterSet):
    caller_name = django_filters.CharFilter(field_name='callerName', lookup_expr='icontains')
    caller_number = django_filters.CharFilter(field_name='callerNumber', lookup_expr='icontains')
    receiver_number = django_filters.CharFilter(field_name='receiverNumber', lookup_expr='icontains')
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    start_date = django_filters.DateFromToRangeFilter(field_name='callStartTime',)
    start_datetime = django_filters.DateTimeFromToRangeFilter(field_name='callStartTime')
    dir = django_filters.BooleanFilter(field_name='callDirection')
    status = django_filters.BooleanFilter(field_name='callStatus')
    cost = django_filters.RangeFilter(field_name='callCost')
    duration = django_filters.RangeFilter(field_name='callDuration')


    class Meta:
        model = Call
        fields = [
            'caller_name',
            'caller_number',
            'receiver_number',
            'city',
            'start_date',
            'start_datetime',
            'dir',
            'status',
            'cost',
            'duration',
        ]