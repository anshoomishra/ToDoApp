from task.models import Task
from task.serializers import TaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework import status
# Create your views here.

class TaskListCreateView(APIView):
    authentication_classes = [BasicAuthentication]
    def get(self, request):
        user = request.user
        tasks = Task.objects.filter(owner=user)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TaskDetailView(APIView):
    authentication_classes = [BasicAuthentication]
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk, owner=self.request.user)
        except Task.DoesNotExist:
            return None

    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)