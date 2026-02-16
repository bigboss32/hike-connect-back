from dependency_injector import containers, providers

from inira.app.routes.application.use_cases.get_routes import GetRoutes
from inira.app.routes.infrastructure.repositories import RoutesRepositoryImpl


class RoutesContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo rutas inject."""

    routes_repository = providers.Factory(RoutesRepositoryImpl)
    get_routes = providers.Factory(GetRoutes, routes_repository=routes_repository)
