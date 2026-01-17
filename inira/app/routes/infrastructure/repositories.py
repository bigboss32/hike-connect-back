from typing import List, Tuple
from rest_framework.exceptions import NotFound

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

        model = RutaSenderismo.objects.create(**data)

        return self._to_entity(model)

    def find_by_id(self, id: str) -> RouteEntity:
        try:
            model = RutaSenderismo.objects.get(pk=id)
        except RutaSenderismo.DoesNotExist:
            raise NotFound(f"No existe una ruta con id {id}")

        return self._to_entity(model)

    def all(self) -> List[RouteEntity]:
        queryset = RutaSenderismo.objects.all().order_by("-created_at")
        return [self._to_entity(model) for model in queryset]
    

    def paginate(
        self,
        *,
        page: int,
        page_size: int,
        difficulty: str | None = None,
        category: str | None = None,
    ) -> Tuple[int, List[RouteEntity]]:

        queryset = RutaSenderismo.objects.all().order_by("-created_at")

        # 🔹 Filtros opcionales
        if difficulty:
            queryset = queryset.filter(difficulty=difficulty)

        if category:
            queryset = queryset.filter(category=category)

        total = queryset.count()

        offset = (page - 1) * page_size
        queryset = queryset[offset: offset + page_size]

        routes = [self._to_entity(model) for model in queryset]

        return total, routes


    # -------------------------
    # 🔧 MÉTODO PRIVADO DE MAPEO
    # -------------------------
    def _to_entity(self, model: RutaSenderismo) -> RouteEntity:
        return RouteEntity(
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
            company=model.company,
            phone=model.phone,
            email=model.email,
            whatsapp=model.whatsapp,
            coordinates=Coordinates(
                lat=model.coordinates.y,
                lng=model.coordinates.x,
            ),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )
