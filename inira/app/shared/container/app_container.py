# inira/app/shared/app_container.py
from dependency_injector import containers, providers
from inira.app.communities.infrastructure.container import CommunitiesContainer
from inira.app.events.infrastructure.container import EventsContainer
from inira.app.routes.infrastructure.container import RoutesContainer

class ApplicationContainer(containers.DeclarativeContainer):
    """Contenedor global de la aplicación."""
    
    config = providers.Configuration()
    routes=providers.Container(RoutesContainer)
    events=providers.Container(EventsContainer)
    communities=providers.Container(CommunitiesContainer)
