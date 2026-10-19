from django.urls import path
from .views import MappingListCreateView, PatientDoctorsView, MappingDeleteView

urlpatterns = [
    path('', MappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:patient_id>/', PatientDoctorsView.as_view(), name='patient-doctors'),
    path('delete/<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete'),
    # Spec-compliant alias: DELETE /api/mappings/<id>/
    path('remove/<int:pk>/', MappingDeleteView.as_view(), name='mapping-delete-by-id'),
]
