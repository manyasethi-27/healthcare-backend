from rest_framework import serializers
from .models import PatientDoctorMapping
from patients.models import Patient
from doctors.models import Doctor


class MappingSerializer(serializers.ModelSerializer):
    """Serializer for PatientDoctorMapping with nested patient and doctor details."""
    patient_details = serializers.SerializerMethodField(read_only=True)
    doctor_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = PatientDoctorMapping
        fields = [
            'id', 'patient', 'doctor', 'notes',
            'patient_details', 'doctor_details', 'assigned_at'
        ]
        read_only_fields = ['id', 'assigned_at', 'patient_details', 'doctor_details']

    def get_patient_details(self, obj):
        return {
            "id": obj.patient.id,
            "name": obj.patient.name,
            "email": obj.patient.email,
        }

    def get_doctor_details(self, obj):
        return {
            "id": obj.doctor.id,
            "name": obj.doctor.name,
            "specialization": obj.doctor.specialization,
            "email": obj.doctor.email,
        }

    def validate(self, data):
        """Validate that the patient-doctor pair doesn't already exist."""
        patient = data.get('patient')
        doctor = data.get('doctor')

        if patient and doctor:
            if PatientDoctorMapping.objects.filter(patient=patient, doctor=doctor).exists():
                raise serializers.ValidationError(
                    f"Doctor '{doctor.name}' is already assigned to patient '{patient.name}'."
                )
        return data


class PatientDoctorListSerializer(serializers.ModelSerializer):
    """Serializer for listing doctors assigned to a specific patient."""
    doctor_details = serializers.SerializerMethodField()

    class Meta:
        model = PatientDoctorMapping
        fields = ['id', 'doctor', 'doctor_details', 'notes', 'assigned_at']

    def get_doctor_details(self, obj):
        return {
            "id": obj.doctor.id,
            "name": obj.doctor.name,
            "specialization": obj.doctor.specialization,
            "email": obj.doctor.email,
            "phone": obj.doctor.phone,
            "hospital": obj.doctor.hospital,
        }
