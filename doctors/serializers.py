from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
    """Serializer for Doctor CRUD operations."""
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'email', 'phone', 'specialization',
            'license_number', 'experience_years', 'hospital', 'bio',
            'created_by', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_by', 'created_at', 'updated_at']

    def get_created_by(self, obj):
        return {
            "id": obj.created_by.id,
            "name": obj.created_by.first_name,
            "email": obj.created_by.email,
        }

    def validate_email(self, value):
        """Ensure email uniqueness during create and update."""
        instance = self.instance
        qs = Doctor.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A doctor with this email already exists.")
        return value

    def validate_license_number(self, value):
        """Ensure license number uniqueness during create and update."""
        if not value:
            return value
        instance = self.instance
        qs = Doctor.objects.filter(license_number=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A doctor with this license number already exists.")
        return value
