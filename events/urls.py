from rest_framework.routers import DefaultRouter
from events.views import EventViewSet

# Register EventViewSet with the router at the root of 'events/' URL
router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')

urlpatterns = router.urls
