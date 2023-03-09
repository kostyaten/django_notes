from rest_framework.routers import SimpleRouter

from .views import UserViewSet, AuthViewSet, NoteViewSet

router = SimpleRouter()
router.register('users', UserViewSet, basename='users')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'note', NoteViewSet, basename='note')

urlpatterns = []
urlpatterns += router.urls
