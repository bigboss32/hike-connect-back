# inira/app/shared/app_container.py
from dependency_injector import containers, providers
from inira.app.shared.credentials import SharedContainer


class ApplicationContainer(containers.DeclarativeContainer):
    """Contenedor global de la aplicación."""
    
    config = providers.Configuration()
    shared = providers.Container(SharedContainer)
