import copy
from rest_framework.permissions import IsAuthenticated
from utils.util import Response
from rest_framework.views import APIView
from Server.settings import formatResponseData
from utils.custom import CustomJWTAuthentication


class DemoView(APIView):
    # 局部(本视图有效)认证类
    authentication_classes = [CustomJWTAuthentication]
    # 局部(本视图有效)权限类
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        demo
        """
        data = copy.deepcopy(formatResponseData)
        try:
            email = request.data.get("email")

            # 异常拦截
            if not email:
                return Response(data=data, responseMsg="请求参数缺失", loggerMsg="请求参数缺失", isError=True)

            # 响应
            data["data"]["响应的数据"] = email
            return Response(data=data, responseMsg="前端得到的回馈信息",
                            loggerMsg=f"demo：一些日志信息")

        except Exception as e:
            return Response(data=data, responseMsg="ServerError",
                            loggerMsg=f"请求处理失败: {e}", isError=True)
