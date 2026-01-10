from rest_framework.views import APIView
from rest_framework.response import Response
from inira.app.core.infrastructure.docs.docs import core_api_post_schema,core_api_get_schema

class CoreAPIView(APIView):

    @core_api_get_schema()
    def get(self, request, *args, **kwargs):
        return self._process(request)

    @core_api_post_schema()
    def post(self, request, *args, **kwargs):
        return self._process(request)






