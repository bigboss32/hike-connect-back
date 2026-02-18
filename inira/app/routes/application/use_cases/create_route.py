# inira/app/routes/application/use_cases/create_route.py

from inira.app.routes.domain.entities import RouteEntity, Coordinates
from inira.app.routes.domain.repositories import RoutesRepository


# inira/app/routes/application/use_cases/create_route.py


class CreateRoute:
    def __init__(self, routes_repository: RoutesRepository):
        self.routes_repository = routes_repository

    def execute(self, data: dict, user_id: str) -> RouteEntity:  # 👈
        coordinates = data.pop("coordinates", None)
        if coordinates:
            data["coordinates"] = Coordinates(
                lat=coordinates["lat"],
                lng=coordinates["lng"],
            )

        data["created_by"] = user_id  # 👈

        route = RouteEntity(**data)
        return self.routes_repository.save(route)
