from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    # 1. Columns to show in the list view
    list_display = (
        "id", 
        "get_patient_email", 
        "created_at", 
        "has_raw_text", 
        "short_summary"
    )
    
    # 2. Sidebar filters
    list_filter = ("created_at", "patient")
    
    # 3. Search box (allows searching by patient email or UUID)
    search_fields = ("patient__email", "id")
    
    # 4. Read-only fields (prevents editing AI results manually)
    readonly_fields = ("id", "created_at", "raw_text", "simplified_text")

    # Custom Method: Show patient email
    def get_patient_email(self, obj):
        return obj.patient.email
    get_patient_email.short_description = 'Patient Email'

    # Custom Method: Visual indicator if OCR worked
    def has_raw_text(self, obj):
        return bool(obj.raw_text)
    has_raw_text.boolean = True
    has_raw_text.short_description = 'OCR Done'

    # Custom Method: Snippet of the simplified text
    def short_summary(self, obj):
        if obj.simplified_text:
            return obj.simplified_text[:75] + "..."
        return "Processing..."
    short_summary.short_description = 'Simplified Summary'