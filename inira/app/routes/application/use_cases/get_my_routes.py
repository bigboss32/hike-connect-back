# inira/app/routes/application/use_cases/get_my_routes.py

from typing import Optional
from inira.app.routes.domain.repositories import RoutesRepository


class GetMyRoutes:
    def __init__(self, routes_repository: RoutesRepository):
        self.routes_repository = routes_repository

    def execute(self, *, user_id: str, page: int = 1, page_size: int = 10):
        total, routes = self.routes_repository.paginate_by_user(
            user_id=user_id,
            page=page,
            page_size=page_size,
        )

        return {
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": routes,
        }
