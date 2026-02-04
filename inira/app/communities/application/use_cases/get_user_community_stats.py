# inira/app/communities/domain/use_cases/get_user_community_stats.py

from inira.app.communities.domain.repositories.member_repository import MemberRepository


class GetUserCommunityStats:

    def __init__(self, member_repository: MemberRepository):
        self.member_repository = member_repository

    def execute(self, *, user_id: int) -> dict:
        """
        Obtiene estadísticas del usuario sobre comunidades

        Returns:
            dict con la estructura:
            {
                'total_communities': int  # Total de comunidades donde el usuario es miembro
            }
        """
        total_communities = self.member_repository.count_by_user(user_id=user_id)

        return {"total_communities": total_communities}
