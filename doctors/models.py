from django.db import models
from django.contrib.auth.models import User


class Doctor(models.Model):
    """Model representing a doctor in the healthcare system."""

    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='doctors',
        help_text="The authenticated user who created this doctor record."
    )
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    specialization = models.CharField(max_length=200)
    license_number = models.CharField(max_length=100, unique=True, blank=True, null=True)
    experience_years = models.PositiveIntegerField(default=0)
    hospital = models.CharField(max_length=300, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctors'

    def __str__(self):
        return f"Dr. {self.name} - {self.specialization}"
