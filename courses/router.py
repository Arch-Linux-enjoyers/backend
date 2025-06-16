from rest_framework.routers import SimpleRouter

from courses.views import CompletedCoursesViewSet, CoursesViewSet


router = SimpleRouter()
router.register('completedcourses', CompletedCoursesViewSet)
router.register('', CoursesViewSet)
