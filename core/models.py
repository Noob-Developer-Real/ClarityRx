from django.db import models
from django.conf import settings
import uuid
class Prescription(models.Model):
    id=models.UUIDField(default=uuid.uuid4,unique=True,editable=False,primary_key=True)
    image = models.ImageField(upload_to="prescriptions/")
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        related_name="prescriptions"
    )
    raw_text = models.TextField(blank=True)
    simplified_text = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
