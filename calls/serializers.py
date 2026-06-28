from rest_framework import serializers
from .models import Call

class CallSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Call
        fields = '__all__'

    def get_id(self, obj):
        return str(obj.id)