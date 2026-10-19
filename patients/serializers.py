from rest_framework import serializers
from .models import Patient


class PatientSerializer(serializers.ModelSerializer):
    """Serializer for Patient CRUD operations."""
    created_by = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Patient
        fields = [
            'id', 'name', 'email', 'phone', 'date_of_birth',
            'gender', 'address', 'medical_history',
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
        """Check email uniqueness but allow the same patient to update their own email."""
        request = self.context.get('request')
        instance = self.instance

        qs = Patient.objects.filter(email=value)
        if instance:
            qs = qs.exclude(pk=instance.pk)
        if qs.exists():
            raise serializers.ValidationError("A patient with this email already exists.")
        return value
