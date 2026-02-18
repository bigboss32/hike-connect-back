from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import NotFound, ValidationError
from rest_framework.permissions import IsAuthenticated
from inira.app.routes.infrastructure.docs.create_route_docs import create_route_docs
from inira.app.routes.infrastructure.docs.get_user_route_rating_docs import (
    get_user_route_rating_docs,
)
from inira.app.routes.infrastructure.docs.get_routes_banner_docs import (
    get_routes_banner_docs,
)
from inira.app.routes.infrastructure.docs.rate_route_docs import rate_route_docs
from inira.app.routes.infrastructure.input.route_input_serializer import (
    RouteInputSerializer,
)
from inira.app.routes.infrastructure.input.ruta_rating_serializer import (
    RutaRatingInputSerializer,
)
from inira.app.routes.infrastructure.models import RutaRating, RutaSenderismo
from inira.app.routes.infrastructure.out.ruta_banner_serializer import (
    RutaBannerSerializer,
)
from inira.app.routes.infrastructure.out.ruta_user_rating_serializer import (
    RutaUserRatingSerializer,
)
from inira.app.shared.container import container
from inira.app.routes.infrastructure.out.route_output_serializer import (
    RouteOutputSerializer,
)
from inira.app.routes.infrastructure.docs.get_routes_docs import get_routes_docs

from django.db.models import Avg, Count

from inira.app.shared.permissions import require_group


class RutaSenderismoAPIView(APIView):
    permission_classes = [IsAuthenticated]

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
        if route_id:
            route = use_case.execute(id=route_id)
            serializer = RouteOutputSerializer(route)
            return Response(serializer.data, status=status.HTTP_200_OK)
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

    @require_group("Ofertante")
    @create_route_docs
    def post(self, request, *args, **kwargs):
        serializer = RouteInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        use_case = container.routes().create_route()
        route = use_case.execute(
            data=serializer.validated_data.copy(),
            user_id=str(request.user.id),
        )

        return Response(
            RouteOutputSerializer(route).data,
            status=status.HTTP_201_CREATED,
        )


class RutaBannerAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_routes_banner_docs
    def get(self, request):
        rutas = RutaSenderismo.objects.annotate(
            rating_avg=Avg("ratings__score"),
            rating_count=Count("ratings"),
        ).order_by("-created_at")[:5]

        serializer = RutaBannerSerializer(rutas, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class RutaRatingAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_user_route_rating_docs
    def get(self, request):
        ruta_id = request.query_params.get("ruta_id")
        ruta = get_object_or_404(RutaSenderismo, id=ruta_id)
        user_rating = RutaRating.objects.filter(ruta=ruta, user=request.user).first()
        stats = RutaRating.objects.filter(ruta=ruta).aggregate(
            rating_avg=Avg("score"),
            rating_count=Count("id"),
        )

        return Response(
            {
                "score": user_rating.score if user_rating else None,
                "rating_avg": (
                    round(stats["rating_avg"], 1) if stats["rating_avg"] else None
                ),
                "rating_count": stats["rating_count"],
            },
            status=status.HTTP_200_OK,
        )

    @rate_route_docs
    def post(self, request):
        serializer = RutaRatingInputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        ruta_id = serializer.validated_data["ruta_id"]
        score = serializer.validated_data["score"]
        ruta = get_object_or_404(RutaSenderismo, id=ruta_id)
        rating = RutaRating.objects.filter(ruta=ruta, user=request.user).first()

        if rating:
            rating.score = score
            rating.save(update_fields=["score"])

            return Response(
                {
                    "detail": "Calificación actualizada",
                    "created": False,
                    "ruta_id": str(ruta.id),
                    "score": rating.score,
                },
                status=status.HTTP_200_OK,
            )
        rating = RutaRating.objects.create(
            ruta=ruta,
            user=request.user,
            score=score,
        )

        return Response(
            {
                "detail": "Ruta calificada correctamente",
                "created": True,
                "ruta_id": str(ruta.id),
                "score": rating.score,
            },
            status=status.HTTP_201_CREATED,
        )
