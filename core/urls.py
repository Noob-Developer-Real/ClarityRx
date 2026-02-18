from django.urls import path
from . import views
from django.conf.urls import handler404

urlpatterns = [
    path('', views.upload_prescription, name='upload_prescription'),
    path('simplify/<uuid:id>/', views.view_prescription, name='view_prescription'),
]
handler404 = 'core.views.error_404'
