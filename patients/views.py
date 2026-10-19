from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Patient
from .serializers import PatientSerializer


class PatientListCreateView(APIView):
    """
    GET  /api/patients/ - List all patients created by the authenticated user.
    POST /api/patients/ - Create a new patient.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all patients created by the currently authenticated user."""
        patients = Patient.objects.filter(created_by=request.user)
        serializer = PatientSerializer(patients, many=True, context={'request': request})
        return Response(
            {
                "count": patients.count(),
                "patients": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Create a new patient record."""
        serializer = PatientSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {
                    "message": "Patient created successfully.",
                    "patient": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class PatientDetailView(APIView):
    """
    GET    /api/patients/<id>/ - Get patient details.
    PUT    /api/patients/<id>/ - Update patient details.
    DELETE /api/patients/<id>/ - Delete a patient.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        """Retrieve a patient, ensuring the requesting user owns it."""
        return get_object_or_404(Patient, pk=pk, created_by=user)

    def get(self, request, pk):
        patient = self.get_object(pk, request.user)
        serializer = PatientSerializer(patient, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        patient = self.get_object(pk, request.user)
        serializer = PatientSerializer(
            patient, data=request.data, partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Patient updated successfully.",
                    "patient": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        patient = self.get_object(pk, request.user)
        patient.delete()
        return Response(
            {"message": "Patient deleted successfully."},
            status=status.HTTP_200_OK
        )
