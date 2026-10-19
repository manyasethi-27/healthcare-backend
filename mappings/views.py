from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import PatientDoctorMapping
from patients.models import Patient
from .serializers import MappingSerializer, PatientDoctorListSerializer


class MappingListCreateView(APIView):
    """
    POST /api/mappings/ - Assign a doctor to a patient.
    GET  /api/mappings/ - Retrieve all patient-doctor mappings.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all patient-doctor mappings."""
        mappings = PatientDoctorMapping.objects.select_related('patient', 'doctor').all()
        serializer = MappingSerializer(mappings, many=True, context={'request': request})
        return Response(
            {
                "count": mappings.count(),
                "mappings": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Assign a doctor to a patient."""
        serializer = MappingSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Doctor assigned to patient successfully.",
                    "mapping": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class PatientDoctorsView(APIView):
    """
    GET /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, patient_id):
        """Retrieve all doctors assigned to a given patient."""
        # Verify the patient exists
        patient = get_object_or_404(Patient, pk=patient_id)
        mappings = PatientDoctorMapping.objects.filter(patient=patient).select_related('doctor')
        serializer = PatientDoctorListSerializer(mappings, many=True, context={'request': request})
        return Response(
            {
                "patient": {
                    "id": patient.id,
                    "name": patient.name,
                    "email": patient.email,
                },
                "assigned_doctors_count": mappings.count(),
                "assigned_doctors": serializer.data
            },
            status=status.HTTP_200_OK
        )


class MappingDeleteView(APIView):
    """
    DELETE /api/mappings/<id>/ - Remove a doctor from a patient (delete by mapping ID).
    """
    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        mapping = get_object_or_404(PatientDoctorMapping, pk=pk)
        patient_name = mapping.patient.name
        doctor_name = mapping.doctor.name
        mapping.delete()
        return Response(
            {
                "message": f"Doctor '{doctor_name}' successfully removed from patient '{patient_name}'."
            },
            status=status.HTTP_200_OK
        )
