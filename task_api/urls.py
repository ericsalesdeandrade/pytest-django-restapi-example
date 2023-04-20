from django.urls import path
from task_api.views import Tasks, TaskDetail

urlpatterns = [path("", Tasks.as_view()),
               path("<str:pk>", TaskDetail.as_view())]
