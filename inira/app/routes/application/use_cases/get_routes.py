from typing import Optional
from inira.app.routes.domain.repositories import RoutesRepository


class GetRoutes:
    def __init__(self, routes_repository: RoutesRepository):
        self.routes_repository = routes_repository

    def execute(
        self,
        *,
        id: Optional[str] = None,
        page: int = 1,
        page_size: int = 10,
        difficulty: Optional[str] = None,
        category: Optional[str] = None,
    ):
        # 🔹 UNA RUTA
        if id:
            return self.routes_repository.find_by_id(id)

        # 🔹 MUCHAS RUTAS (PAGINADAS)
        total, routes = self.routes_repository.paginate(
            page=page,
            page_size=page_size,
            difficulty=difficulty,
            category=category,
        )
        print(total)

        return {
            "count": total,
            "page": page,
            "page_size": page_size,
            "results": routes,
        }
