from django.contrib import admin
from django.urls import include, path
from scalar.scalar import urlpatterns_scalar, scalar_viewer

urlpatterns = [
    path('', scalar_viewer, name='root'),  
    
    path('admin/', admin.site.urls),
    
    path(
        "api/core/",
        include("inira.app.core.infrastructure.urls"),
    ),

]

urlpatterns += urlpatterns_scalar
