from django.contrib import admin
from .models import Movie, Cinema, ShowTime, Ticket
# Register your models here.


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    pass

@admin.register(Cinema)
class CinemaAdmin(admin.ModelAdmin):
    pass

@admin.register(ShowTime)
class ShowTimeAdmin(admin.ModelAdmin):
    pass


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass
