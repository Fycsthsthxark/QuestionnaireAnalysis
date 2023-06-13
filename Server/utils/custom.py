import copy
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.settings import api_settings
from Server.settings import formatResponseData
from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework import status
from utils.loggingConfig import logger
from rest_framework.response import Response as rest_framework_response


# 自定义请求的响应
def Response(data, responseMsg=None, loggerMsg=None, isError=False, status=None, **kwargs):
    # 状态码处理
    if status:
        pass
    else:
        if isError:
            status = 2001
        else:
            status = 200

    # 日志处理
    if loggerMsg:
        if isError:
            logger.error(loggerMsg)
        else:
            logger.info(loggerMsg)

    data["status"] = status
    data["msg"] = responseMsg

    return rest_framework_response(data, status=status, **kwargs)


def CustomExceptionHandler(exc, context):
    """
    自定义DRF异常处理响应格式
    """
    response = drf_exception_handler(exc, context)

    data = copy.deepcopy(formatResponseData)
    loggerMsg = "%s - %s - %s" % (context["view"], context["request"].method, exc)

    if response:
        return Response(data=data, responseMsg=str(exc), loggerMsg=loggerMsg, isError=True, status=response.status)
    else:
        return Response(data=data, responseMsg=str(exc), loggerMsg=loggerMsg, isError=True,
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CustomJWTAuthentication(JWTAuthentication):
    """
    自定义JWT认证逻辑
    """

    def authenticate(self, request):
        """
        重写DRF认证类验证token逻辑：验证token是否合法
        返回 None => 继续验证其他正在使用的身份验证方案
        返回 (user, token) => 代表合法用户
        抛AuthenticationFailed异常 => 代表非法用户
        """
        # 取出前端传来的 token
        token = None
        headerToken = request.META.get(api_settings.AUTH_HEADER_NAME, "")
        tokenTopAndEnd = headerToken.split(" ")

        if len(tokenTopAndEnd) == 2:
            token = tokenTopAndEnd[1]

        # token为空，不进行token验证，继续验证其他正在使用的身份验证方案
        if token is None:
            return None

        # 验证token
        validated_token = self.get_validated_token(token)
        user = self.get_user(validated_token)
        return user, validated_token
