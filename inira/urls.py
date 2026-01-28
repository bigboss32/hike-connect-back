from django.contrib import admin
from django.urls import include, path
from scalar.scalar import urlpatterns_scalar, scalar_viewer

urlpatterns = [
    path('', scalar_viewer, name='root'),  
    
    path('admin/', admin.site.urls),
    
    path(
        "api/v1/",
        include("inira.app.accounts.infrastructure.urls"),
    ),
        path(
        "api/v1/",
        include("inira.app.routes.infrastructure.urls"),
    ),
        path(
        "api/v1/",
        include("inira.app.events.infrastructure.urls"),
    ),
    
        path(
        "api/v1/",
        include("inira.app.communities.infrastructure.urls"),
    ),
      path(
        "api/v1/",
        include("inira.app.core.infrastructure.urls"),
    ),



]

urlpatterns += urlpatterns_scalar
