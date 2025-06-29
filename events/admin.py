from django.contrib import admin

from events.models import Event, Attendee


admin.site.register(Event)
admin.site.register(Attendee)
