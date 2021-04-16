from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .models import Task
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrStaffOrReadOnly
from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class CreateTaskApp(CreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DetailUpdateDeleteTaskApi(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrStaffOrReadOnly)
    queryset = Task.objects.all()


class ListAllTasksApi(ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated,)
    pagination_class = Pagination


class ListUserTasksApi(ListAllTasksApi):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    pagination_class = Pagination

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
