from dependency_injector import containers, providers
from inira.app.events.application.use_cases.get_events import GetEvents
from inira.app.events.application.use_cases.register_user_to_event import RegisterUserToEvent
from inira.app.events.infrastructure.repositories.event_registration_repository_impl import EventRegistrationRepositoryImpl
from inira.app.events.infrastructure.repositories.events_repository_impl import EventsRepositoryImpl



class EventsContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo rutas inject."""

    events_repository = providers.Factory(EventsRepositoryImpl)
    registration_repository= providers.Factory(EventRegistrationRepositoryImpl)


    register_user_to_event=providers.Factory(
        RegisterUserToEvent,
        events_repository=events_repository,
        registration_repository=registration_repository,
    )

    get_events=providers.Factory(
        GetEvents,
        events_repository=events_repository,
    )
