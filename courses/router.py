from rest_framework.routers import SimpleRouter

from courses.views import CoursesViewSet


router = SimpleRouter()
router.register('courses', CoursesViewSet)
