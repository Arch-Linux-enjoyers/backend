from rest_framework.serializers import ModelSerializer

from courses.models import Course


class CourseSerializer(ModelSerializer):

    class Meta:  # noqa: D106
        model = Course
        fields = '__all__'
