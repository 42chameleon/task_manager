from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Task


class TaskSerializer(ModelSerializer):
    user_id = serializers.CharField(read_only=True)

    class Meta:
        model = Task
        fields = [
            'user_id',
            'name',
            'description',
            'date_end',
            'file'
        ]

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return Task.objects.create(**validated_data)
