from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, ValidationError

from inira.app.shared.container import container
from inira.app.routes.infrastructure.out.route_output_serializer import (
    RouteOutputSerializer
)
from inira.app.routes.infrastructure.docs.get_routes_docs import get_routes_docs


class RutaSenderismoAPIView(APIView):
    permission_classes = [AllowAny]

    @get_routes_docs
    def get(self, request, *args, **kwargs):
        """
        Query params soportados:
        - id: UUID (opcional)
        - page: int (opcional, default=1)
        - page_size: int (opcional, default=10)
        """

        route_id = request.query_params.get("id")
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 10)

        # 🔹 Validaciones básicas
        try:
            page = int(page)
            page_size = int(page_size)
            if page <= 0 or page_size <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError(
                {"detail": "page y page_size deben ser enteros positivos"}
            )

        use_case = container.routes().get_routes()

        # =========================
        # 🔹 UNA SOLA RUTA
        # =========================
        if route_id:
            route = use_case.execute(id=route_id)
            serializer = RouteOutputSerializer(route)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # =========================
        # 🔹 LISTADO PAGINADO
        # =========================
        result = use_case.execute()

        routes = result["results"]
        total = result["count"]

        start = (page - 1) * page_size
        end = start + page_size
        paginated_routes = routes[start:end]

        serializer = RouteOutputSerializer(paginated_routes, many=True)

        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )
