from rest_framework.routers import DefaultRouter
from events.views import EventViewSet, AttendeeRegisterViewSet, AttendeeListViewSet

# Register EventViewSet with the router at the root of 'events/' URL
router = DefaultRouter()
router.register(r'', EventViewSet, basename='event')
router.register(r'(?P<event_id>\d+)/register', AttendeeRegisterViewSet, basename='register_attendee')
router.register(r'(?P<event_id>\d+)/attendees', AttendeeListViewSet, basename='list_attendee')

urlpatterns = router.urls
