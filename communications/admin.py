from django.contrib import admin
from .models import Appointment, Message, Notification

# Register your models here.

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('property', 'requester', 'agent', 'appointment_date', 'status')
    list_filter = ('status', 'appointment_date')
    search_fields = ('purpose', 'notes', 'requester__username', 'agent__username')

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'property', 'sent_date', 'is_read')
    list_filter = ('is_read', 'sent_date')
    search_fields = ('content', 'sender__username', 'recipient__username')

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'notification_type', 'related_id', 'is_read', 'created_at')
    list_filter = ('notification_type', 'is_read', 'created_at')
    search_fields = ('content', 'user__username')
