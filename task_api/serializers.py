from rest_framework import serializers
from task_api.models import TaskModel


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = "__all__"
