from .models import Todo
from .serializer import TodoSerializer

from rest_framework import viewsets, permissions

class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = TodoSerializer