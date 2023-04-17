from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, generics
from task_api.models import TaskModel
from task_api.serializers import TaskSerializer
import math
from datetime import datetime


class Tasks(generics.GenericAPIView):
    serializer_class = TaskSerializer
    queryset = TaskModel.objects.all()

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        tasks = TaskModel.objects.all()
        total_tasks = tasks.count()
        if search_param:
            tasks = tasks.filter(title__icontains=search_param)
        serializer = self.serializer_class(tasks[start_num:end_num], many=True)
        return Response(
            {
                "status": "success",
                "total": total_tasks,
                "page": page_num,
                "last_page": math.ceil(total_tasks / limit_num),
                "tasks": serializer.data,
            }
        )

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"status": "success", "task": serializer.data},
                status=status.HTTP_201_CREATED,
            )
        else:
            return Response(
                {"status": "fail", "message": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )


class TaskDetail(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_task(self, pk):
        try:
            return TaskModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        task = self.get_task(pk=pk)
        if task is None:
            return Response(
                {"status": "fail", "message": f"Task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task)
        return Response({"status": "success", "task": serializer.data})

    def patch(self, request, pk):
        task = self.get_task(pk)
        if task is None:
            return Response(
                {"status": "fail", "message": f"Task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = self.serializer_class(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data["updatedAt"] = datetime.now()
            serializer.save()
            return Response({"status": "success", "task": serializer.data})
        return Response(
            {"status": "fail", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, pk):
        task = self.get_task(pk)
        if task is None:
            return Response(
                {"status": "fail", "message": f"Task with Id: {pk} not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
