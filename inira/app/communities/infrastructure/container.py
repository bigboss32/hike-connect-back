# inira/app/communities/infrastructure/container.py

from dependency_injector import containers, providers

from inira.app.communities.infrastructure.repositories.comunidad_repository_impl import ComunidadRepositoryImpl
from inira.app.communities.infrastructure.repositories.member_repository_impl import MemberRepositoryImpl
from inira.app.communities.infrastructure.repositories.canal_repository_impl import CanalRepositoryImpl
from inira.app.communities.infrastructure.repositories.post_repository_impl import PostRepositoryImpl

from inira.app.communities.application.use_cases.get_communities import GetCommunities
from inira.app.communities.application.use_cases.create_community import CreateCommunity
from inira.app.communities.application.use_cases.join_community import JoinCommunity
from inira.app.communities.application.use_cases.leave_community import LeaveCommunity
from inira.app.communities.application.use_cases.get_community_channels import GetCommunityChannels
from inira.app.communities.application.use_cases.create_channel import CreateChannel
from inira.app.communities.application.use_cases.get_posts import GetPosts
from inira.app.communities.application.use_cases.create_post import CreatePost


class CommunitiesContainer(containers.DeclarativeContainer):
    """Contenedor de dependencias del módulo comunidades."""

    # Repositories
    comunidad_repository = providers.Factory(ComunidadRepositoryImpl)
    member_repository = providers.Factory(MemberRepositoryImpl)
    canal_repository = providers.Factory(CanalRepositoryImpl)
    post_repository = providers.Factory(PostRepositoryImpl)

    # Use Cases - Comunidades
    get_communities = providers.Factory(
        GetCommunities,
        comunidad_repository=comunidad_repository,
    )

    create_community = providers.Factory(
        CreateCommunity,
        comunidad_repository=comunidad_repository,
        member_repository=member_repository,
    )

    join_community = providers.Factory(
        JoinCommunity,
        comunidad_repository=comunidad_repository,
        member_repository=member_repository,
    )

    leave_community = providers.Factory(
        LeaveCommunity,
        member_repository=member_repository,
    )

    # Use Cases - Canales
    get_community_channels = providers.Factory(
        GetCommunityChannels,
        canal_repository=canal_repository,
        member_repository=member_repository,
    )

    create_channel = providers.Factory(
        CreateChannel,
        canal_repository=canal_repository,
        member_repository=member_repository,
    )

    # Use Cases - Posts
    get_posts = providers.Factory(
        GetPosts,
        post_repository=post_repository,
        canal_repository=canal_repository,
        member_repository=member_repository,
    )

    create_post = providers.Factory(
        CreatePost,
        post_repository=post_repository,
        canal_repository=canal_repository,
        member_repository=member_repository,
    )