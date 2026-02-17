# inira/app/routes/infrastructure/repositories/routes_repository_impl.py

from typing import List, Tuple, Optional
from rest_framework.exceptions import NotFound
from django.db.models import Avg, Count
from decimal import Decimal

from inira.app.routes.domain.entities import RouteEntity, Coordinates
from inira.app.routes.domain.repositories import RoutesRepository
from inira.app.routes.infrastructure.models import RutaSenderismo


class RoutesRepositoryImpl(RoutesRepository):
    """Implementación concreta usando Django ORM."""

    def save(self, route: RouteEntity) -> RouteEntity:
        data = route.__dict__.copy()

        # 🔹 Mapear coordenadas dominio → ORM
        coordinates = data.pop("coordinates", None)
        if coordinates:
            data["coordinates"] = f"POINT({coordinates.lng} {coordinates.lat})"

        # 🔹 Remover campos calculados que no existen en el modelo
        data.pop("rating_avg", None)
        data.pop("rating_count", None)

        model = RutaSenderismo.objects.create(**data)

        return self._to_entity(model)

    def find_by_id(self, id: str) -> RouteEntity:
        try:
            model = RutaSenderismo.objects.annotate(
                rating_avg=Avg("ratings__score"),
                rating_count=Count("ratings"),
            ).get(pk=id)
        except RutaSenderismo.DoesNotExist:
            raise NotFound(f"No existe una ruta con id {id}")

        return self._to_entity(model)

    def all(self) -> List[RouteEntity]:
        queryset = RutaSenderismo.objects.annotate(
            rating_avg=Avg("ratings__score"),
            rating_count=Count("ratings"),
        ).order_by("-created_at")
        return [self._to_entity(model) for model in queryset]

    def paginate(
        self,
        *,
        page: int,
        page_size: int,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
        requires_payment: Optional[bool] = None,
        is_active: Optional[bool] = None,
    ) -> Tuple[int, List[RouteEntity]]:

        queryset = RutaSenderismo.objects.annotate(
            rating_avg=Avg("ratings__score"),
            rating_count=Count("ratings"),
        ).order_by("-created_at")

        # 🔹 Filtros opcionales
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if category:
            queryset = queryset.filter(category=category)

        # 🆕 Nuevos filtros
        if requires_payment is not None:
            queryset = queryset.filter(requires_payment=requires_payment)

        if is_active is not None:
            queryset = queryset.filter(is_active=is_active)
        else:
            # Por defecto, solo mostrar rutas activas
            queryset = queryset.filter(is_active=True)

        total = queryset.count()

        offset = (page - 1) * page_size
        queryset = queryset[offset : offset + page_size]

        routes = [self._to_entity(model) for model in queryset]

        return total, routes

    # 🆕 Método para obtener disponibilidad de una ruta en una fecha
    def get_availability_for_date(
        self, ruta_id: str, date
    ) -> Optional["RutaAvailability"]:
        """
        Obtiene o crea la disponibilidad para una fecha específica.
        """
        from inira.app.routes.infrastructure.models import RutaAvailability

        try:
            ruta = RutaSenderismo.objects.get(pk=ruta_id)
        except RutaSenderismo.DoesNotExist:
            raise NotFound(f"No existe una ruta con id {ruta_id}")

        # Obtener o crear disponibilidad
        availability, created = RutaAvailability.objects.get_or_create(
            ruta=ruta,
            date=date,
            defaults={
                "available_slots": ruta.max_capacity,
                "is_available": True,
            },
        )

        return availability

    # 🆕 Método para verificar si hay cupos disponibles
    def check_availability(self, ruta_id: str, date, number_of_people: int) -> bool:
        """
        Verifica si hay cupos disponibles para una fecha y cantidad de personas.
        """
        availability = self.get_availability_for_date(ruta_id, date)

        if not availability:
            return False

        return (
            availability.is_available
            and availability.available_slots >= number_of_people
        )

    # -------------------------
    # 🔧 MÉTODO PRIVADO DE MAPEO
    # -------------------------
    def _to_entity(self, model: RutaSenderismo) -> RouteEntity:
        # Obtener rating_avg y rating_count si están disponibles (vienen de annotate)
        rating_avg = getattr(model, "rating_avg", None)
        rating_count = getattr(model, "rating_count", None)

        return RouteEntity(
            # Campos originales obligatorios
            id=str(model.id),
            title=model.title,
            location=model.location,
            distance=model.distance,
            duration=model.duration,
            difficulty=model.difficulty,
            image=model.image,
            type=model.type,
            category=model.category,
            description=model.description,
            coordinates=Coordinates(
                lat=model.coordinates.y,
                lng=model.coordinates.x,
            ),
            # Campos opcionales originales
            company=model.company,
            phone=model.phone,
            email=model.email,
            whatsapp=model.whatsapp,
            created_at=model.created_at,
            updated_at=model.updated_at,
            # 🆕 Nuevos campos de pricing y configuración
            base_price=model.base_price,
            requires_payment=model.requires_payment,
            max_capacity=model.max_capacity,
            min_participants=model.min_participants,
            max_participants_per_booking=model.max_participants_per_booking,
            requires_date_selection=model.requires_date_selection,
            is_active=model.is_active,
            # 🆕 Información adicional
            included_services=model.included_services,
            requirements=model.requirements,
            what_to_bring=model.what_to_bring,
            # 🆕 Campos calculados (del annotate)
            rating_avg=float(rating_avg) if rating_avg else None,
            rating_count=rating_count or 0,
        )
