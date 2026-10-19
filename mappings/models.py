from django.db import models
from patients.models import Patient
from doctors.models import Doctor


class PatientDoctorMapping(models.Model):
    """
    Model representing the many-to-many assignment of doctors to patients.
    A patient can have multiple doctors and a doctor can have multiple patients.
    """
    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='doctor_mappings',
        help_text="The patient being assigned a doctor."
    )
    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='patient_mappings',
        help_text="The doctor being assigned to the patient."
    )
    assigned_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True, help_text="Optional notes about this assignment.")

    class Meta:
        ordering = ['-assigned_at']
        verbose_name = 'Patient-Doctor Mapping'
        verbose_name_plural = 'Patient-Doctor Mappings'
        # Prevent duplicate doctor-patient assignments
        unique_together = ('patient', 'doctor')

    def __str__(self):
        return f"{self.patient.name} → Dr. {self.doctor.name}"
