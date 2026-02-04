# inira/app/communities/infrastructure/api/community_api.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import ValidationError

from inira.app.communities.infrastructure.docs.post_community_post_docs import (
    post_community_post_docs,
)
from inira.app.communities.infrastructure.docs.get_community_posts_docs import (
    get_community_posts_docs,
)
from inira.app.communities.infrastructure.docs.post_community_channel_docs import (
    post_community_channel_docs,
)
from inira.app.communities.infrastructure.docs.get_community_channels_docs import (
    get_community_channels_docs,
)
from inira.app.communities.infrastructure.docs.delete_community_member_docs import (
    delete_community_member_docs,
)
from inira.app.communities.infrastructure.docs.post_community_member_docs import (
    post_community_member_docs,
)
from inira.app.communities.infrastructure.docs.post_community_docs import (
    post_community_docs,
)
from inira.app.communities.infrastructure.docs.get_communities_docs import (
    get_communities_docs,
)
from inira.app.communities.infrastructure.out.member_output_serializer import (
    MemberOutputSerializer,
)
from inira.app.shared.container import container
from inira.app.communities.infrastructure.out.community_output_serializer import (
    ComunidadOutputSerializer,
    ComunidadDetailOutputSerializer,
)
from inira.app.communities.infrastructure.docs.get_community_members_docs import (
    get_community_members_docs,
)


class ComunidadAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_communities_docs
    def get(self, request, *args, **kwargs):
        """
        Query params:
        - id: UUID (opcional)
        - is_public: bool (opcional)
        - page: int (opcional, default=1)
        - page_size: int (opcional, default=10)
        """
        comunidad_id = request.query_params.get("id")
        is_public = request.query_params.get("is_public")
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

        use_case = container.communities().get_communities()

        if comunidad_id:
            comunidad = use_case.execute(id=comunidad_id, user_id=request.user.id)
            serializer = ComunidadDetailOutputSerializer(comunidad)
            return Response(serializer.data, status=status.HTTP_200_OK)

        filters = {}
        if is_public is not None:
            filters["is_public"] = is_public.lower() == "true"

        result = use_case.execute(
            user_id=request.user.id, page=page, page_size=page_size, **filters
        )

        comunidades = result["results"]
        total = result["count"]

        serializer = ComunidadOutputSerializer(comunidades, many=True)

        return Response(
            {
                "count": total,
                "page": page,
                "page_size": page_size,
                "results": serializer.data,
            },
            status=status.HTTP_200_OK,
        )

    @post_community_docs
    def post(self, request):
        """
        Body params:
        - name: str (requerido)
        - description: str (requerido)
        - image: str (requerido)
        - company: str (opcional)
        - location: str (requerido)
        - is_public: bool (opcional, default=True)
        """
        use_case = container.communities().create_community()

        try:
            comunidad = use_case.execute(
                name=request.data.get("name"),
                description=request.data.get("description"),
                image=request.data.get("image"),
                created_by_id=request.user.id,
                company=request.data.get("company"),
                location=request.data.get("location"),
                is_public=request.data.get("is_public", True),
            )

            serializer = ComunidadDetailOutputSerializer(comunidad)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ComunidadMemberAPIView(APIView):
    """
    Vista para gestionar miembros de comunidades.

    Endpoints:
    - GET: Obtener miembros de una comunidad O estadísticas del usuario
    - POST: Unirse a una comunidad
    - DELETE: Abandonar una comunidad
    """

    permission_classes = [IsAuthenticated]

    @get_community_members_docs
    def get(self, request, *args, **kwargs):
        """
        Dos modos de operación según los query params:

        1. Si incluye 'comunidad_id': Retorna los miembros de esa comunidad
           Query params:
           - comunidad_id: UUID (requerido para este modo)

        2. Si incluye 'stats=true': Retorna estadísticas del usuario autenticado
           Query params:
           - stats: bool (debe ser 'true')
        """
        comunidad_id = request.query_params.get("comunidad_id")
        get_stats = request.query_params.get("stats", "").lower() == "true"

        # Modo 1: Obtener estadísticas del usuario
        if get_stats:
            use_case = container.communities().get_user_community_stats()
            try:
                stats = use_case.execute(user_id=request.user.id)
                return Response(stats, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Modo 2: Obtener miembros de una comunidad
        if not comunidad_id:
            return Response(
                {"detail": "Se requiere 'comunidad_id' o 'stats=true'"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = container.communities().get_community_members()

        try:
            members = use_case.execute(
                comunidad_id=comunidad_id,
                user_id=request.user.id,
            )

            serializer = MemberOutputSerializer(members, many=True)
            return Response(
                {"count": len(members), "results": serializer.data},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @post_community_member_docs
    def post(self, request):
        """
        Body params:
        - comunidad_id: UUID (requerido)
        """
        comunidad_id = request.data.get("comunidad_id")

        if not comunidad_id:
            return Response(
                {"detail": "comunidad_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = container.communities().join_community()

        try:
            use_case.execute(
                comunidad_id=comunidad_id,
                user_id=request.user.id,
            )

            return Response(
                {"detail": "Te has unido a la comunidad exitosamente"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @delete_community_member_docs
    def delete(self, request):
        """
        Body params:
        - comunidad_id: UUID (requerido)
        """
        comunidad_id = request.data.get("comunidad_id")

        if not comunidad_id:
            return Response(
                {"detail": "comunidad_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = container.communities().leave_community()

        try:
            use_case.execute(
                comunidad_id=comunidad_id,
                user_id=request.user.id,
            )

            return Response(
                {"detail": "Has abandonado la comunidad"},
                status=status.HTTP_204_NO_CONTENT,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ComunidadCanalAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_community_channels_docs
    def get(self, request, *args, **kwargs):
        """
        Query params:
        - comunidad_id: UUID (requerido)
        """
        comunidad_id = request.query_params.get("comunidad_id")

        if not comunidad_id:
            return Response(
                {"detail": "comunidad_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        use_case = container.communities().get_community_channels()

        try:
            canales = use_case.execute(
                comunidad_id=comunidad_id,
                user_id=request.user.id,
            )

            from inira.app.communities.infrastructure.out.channel_output_serializer import (
                CanalOutputSerializer,
            )

            serializer = CanalOutputSerializer(canales, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @post_community_channel_docs
    def post(self, request):
        """
        Body params:
        - comunidad_id: UUID (requerido)
        - name: str (requerido)
        - description: str (opcional)
        - is_info: bool (opcional, default=False)
        - is_read_only: bool (opcional, default=False)
        """
        use_case = container.communities().create_channel()

        try:
            canal = use_case.execute(
                comunidad_id=request.data.get("comunidad_id"),
                name=request.data.get("name"),
                description=request.data.get("description", ""),
                is_info=request.data.get("is_info", False),
                is_read_only=request.data.get("is_read_only", False),
                user_id=request.user.id,
            )

            from inira.app.communities.infrastructure.out.channel_output_serializer import (
                CanalOutputSerializer,
            )

            serializer = CanalOutputSerializer(canal)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ComunidadPostAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @get_community_posts_docs
    def get(self, request, *args, **kwargs):
        """
        Query params:
        - canal_id: UUID (requerido)
        - page: int (opcional, default=1)
        - page_size: int (opcional, default=20)
        """
        canal_id = request.query_params.get("canal_id")
        page = request.query_params.get("page", 1)
        page_size = request.query_params.get("page_size", 20)

        if not canal_id:
            return Response(
                {"detail": "canal_id es requerido"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            page = int(page)
            page_size = int(page_size)
            if page <= 0 or page_size <= 0:
                raise ValueError
        except ValueError:
            raise ValidationError(
                {"detail": "page y page_size deben ser enteros positivos"}
            )

        use_case = container.communities().get_posts()

        try:
            result = use_case.execute(
                canal_id=canal_id,
                user_id=request.user.id,
                page=page,
                page_size=page_size,
            )

            posts = result["results"]
            total = result["count"]

            from inira.app.communities.infrastructure.out.post_output_serializer import (
                PostOutputSerializer,
            )

            serializer = PostOutputSerializer(posts, many=True)

            return Response(
                {
                    "count": total,
                    "page": page,
                    "page_size": page_size,
                    "results": serializer.data,
                },
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

    @post_community_post_docs
    def post(self, request):
        """
        Body params:
        - comunidad_id: UUID (requerido)
        - canal_id: UUID (requerido)
        - content: str (requerido)
        """
        use_case = container.communities().create_post()

        try:
            post = use_case.execute(
                comunidad_id=request.data.get("comunidad_id"),
                canal_id=request.data.get("canal_id"),
                author_id=request.user.id,
                content=request.data.get("content"),
            )

            from inira.app.communities.infrastructure.out.post_output_serializer import (
                PostOutputSerializer,
            )

            serializer = PostOutputSerializer(post)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
