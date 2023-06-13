import copy

from questionnaire.models import QuestionnaireRecords
from utils.custom import Response
from rest_framework.views import APIView
from Server.settings import formatResponseData
from utils.util import newID


class SubmitView(APIView):
    # 局部(本视图有效)认证类
    authentication_classes = []
    # 局部(本视图有效)权限类
    permission_classes = []

    def post(self, request, *args, **kwargs):
        """
        提交问卷
        """
        data = copy.deepcopy(formatResponseData)
        try:
            problemList = request.data.get("problemList")

            # 异常拦截
            if not problemList:
                return Response(data=data, responseMsg="请求参数缺失", loggerMsg="请求参数缺失", isError=True)

            QuestionnaireRecords.objects.create(uid=newID(), problemList=str(problemList)).save()

            # 响应
            return Response(data=data, responseMsg="提交成功",
                            loggerMsg=f"提交问卷：提交成功")

        except Exception as e:
            return Response(data=data, responseMsg="ServerError",
                            loggerMsg=f"请求处理失败: {e}", isError=True)
