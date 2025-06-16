from rest_framework.permissions import IsAuthenticated
from rest_framework.serializers import ModelSerializer
from rest_framework.viewsets import ModelViewSet

from courses.models import CompletedCourse
from courses.serializers import CompletedCourseReadSerializer, CompletedCourseWriteSerializer, CourseSerializer


class CoursesViewSet(ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]
    queryset = serializer_class.Meta.model.objects.all()


class CompletedCoursesViewSet(ModelViewSet):
    def get_serializer_class(self) -> type[ModelSerializer]:
        '''Return serializer class by HTTP method.'''
        if self.request.method == 'GET':
            return CompletedCourseReadSerializer
        return CompletedCourseWriteSerializer

    permission_classes = [IsAuthenticated]
    queryset = CompletedCourse.objects.all()
