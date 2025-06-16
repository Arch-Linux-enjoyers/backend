from rest_framework.serializers import ModelSerializer

from courses.models import CompletedCourse, Course


class CourseSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        model = Course
        fields = '__all__'


class CompletedCourseWriteSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        model = CompletedCourse
        fields = '__all__'


class CompletedCourseReadSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        depth = 1
        model = CompletedCourse
        fields = '__all__'
