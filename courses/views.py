import typing as ty

from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.models import Course
from courses.serializers import CourseSerializer


class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes: ty.ClassVar[list[BasePermission]] = [IsAuthenticated]
    queryset = Course.objects.all()
