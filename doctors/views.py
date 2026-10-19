from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import Doctor
from .serializers import DoctorSerializer


class DoctorListCreateView(APIView):
    """
    GET  /api/doctors/ - Retrieve all doctors (any authenticated user).
    POST /api/doctors/ - Add a new doctor (authenticated users only).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve all doctors in the system."""
        doctors = Doctor.objects.all()
        serializer = DoctorSerializer(doctors, many=True, context={'request': request})
        return Response(
            {
                "count": doctors.count(),
                "doctors": serializer.data
            },
            status=status.HTTP_200_OK
        )

    def post(self, request):
        """Create a new doctor record."""
        serializer = DoctorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(
                {
                    "message": "Doctor created successfully.",
                    "doctor": serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )


class DoctorDetailView(APIView):
    """
    GET    /api/doctors/<id>/ - Get doctor details.
    PUT    /api/doctors/<id>/ - Update doctor details.
    DELETE /api/doctors/<id>/ - Delete a doctor.
    """
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Doctor, pk=pk)

    def get(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(doctor, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        doctor = self.get_object(pk)
        serializer = DoctorSerializer(
            doctor, data=request.data, partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Doctor updated successfully.",
                    "doctor": serializer.data
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {"errors": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        doctor = self.get_object(pk)
        doctor.delete()
        return Response(
            {"message": "Doctor deleted successfully."},
            status=status.HTTP_200_OK
        )
