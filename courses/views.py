from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from courses.serializers import CompletedCourseSerializer, CourseSerializer


class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = (IsAuthenticated)
    queryset = serializer_class.Meta.model.objects.all()


class CompletedCoursesViewSet(ModelViewSet):
    serializer_class = CompletedCourseSerializer
    permission_classes = (IsAuthenticated)
    queryset = serializer_class.Meta.model.objects.all()
