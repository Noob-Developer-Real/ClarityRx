from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Prescription
from .services.ocr_space import extract_text_from_image
from .services.groq_simplifier import simplify_prescription

@login_required
def upload_prescription(request):
    if request.method == "POST" and request.FILES.get("image"):
        # 1. Create the object and link the 'patient' to the logged-in user
        prescription = Prescription.objects.create(
            patient=request.user, # This is the "Created By" link
            image=request.FILES["image"]
        )
        
        # 2. Process AI logic
        raw_text = extract_text_from_image(prescription.image.url)
        prescription.raw_text = raw_text
        prescription.simplified_text = simplify_prescription(raw_text)
        
        # 3. Save the final results
        prescription.save()
        
        return redirect('view_prescription', id=prescription.id)

    return render(request, "core/upload_form.html")

@login_required
def view_prescription(request, id):
    prescription = get_object_or_404(Prescription, id=id, patient=request.user)
    return render(request, "core/upload.html", {
        "prescription": prescription
    })

def error_404(request, exception):
    return render(request, '404.html', status=404)