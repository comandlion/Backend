from django.db import models
from django.contrib.auth.models import User
from properties.models import Property

# Create your models here.

class Appointment(models.Model):
    APPOINTMENT_STATUS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('canceled', 'Canceled'),
        ('completed', 'Completed'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='appointments')
    requester = models.ForeignKey(User, on_delete=models.CASCADE, related_name='requested_appointments')
    agent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='agent_appointments')
    appointment_date = models.DateTimeField()
    duration = models.DurationField()
    status = models.CharField(max_length=10, choices=APPOINTMENT_STATUS, default='pending')
    purpose = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    content = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    read_date = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('message', 'New Message'),
        ('offer', 'New Offer'),
        ('appointment', 'Appointment Update'),
        ('property', 'New Property Matching Criteria'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    related_id = models.PositiveIntegerField()  # Generic foreign key alternative
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)