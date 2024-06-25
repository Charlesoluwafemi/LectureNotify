from django.urls import path, include
from django.contrib import admin
from backend.views import UploadExcelView, CSRFView
from backend.views import root_view
from backend.views import upload_students


urlpatterns = [
    path('admin/', admin.site.urls),
    path('backend/', include('backend.urls')),
    path('upload/', UploadExcelView.as_view(), name='upload'),
    path('csrf/', CSRFView.as_view(), name='csrf'),
    path('', root_view, name='root'),  # Define a view for the root path
    path('upload-students/', upload_students, name='upload_students'),
    # Other URL patterns as needed
    # Other URL patterns as needed
]
