from rest_framework.routers import SimpleRouter

from courses.views import CompletedCoursesViewSet, CoursesViewSet


router = SimpleRouter()
router.register('courses', CoursesViewSet)
router.register('completedcourses', CompletedCoursesViewSet)
