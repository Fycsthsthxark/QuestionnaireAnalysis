import copy

from questionnaire.models import QuestionnaireRecords
from utils.custom import Response
from rest_framework.views import APIView
from Server.settings import formatResponseData


class GetCountView(APIView):
    # 局部(本视图有效)认证类
    authentication_classes = []
    # 局部(本视图有效)权限类
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        获取问卷数量
        """
        data = copy.deepcopy(formatResponseData)
        try:
            data["data"]["count"] = QuestionnaireRecords.objects.count()

            return Response(data=data, loggerMsg=f"获取问卷数量：成功")

        except Exception as e:
            return Response(data=data, responseMsg="ServerError",
                            loggerMsg=f"请求处理失败: {e}", isError=True)
