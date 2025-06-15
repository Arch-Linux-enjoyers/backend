from rest_framework.serializers import ModelSerializer

from courses.models import CompletedCourse, Course


class CourseSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        model = Course
        fields = '__all__'


class CompletedCourseSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        model = CompletedCourse
        fields = '__all__'
