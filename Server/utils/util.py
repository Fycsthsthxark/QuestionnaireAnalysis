import uuid
from rest_framework_simplejwt.authentication import JWTAuthentication
# from 示例APP.models import User
from utils.loggingConfig import logger


def newID():
    """
    生成一个唯一ID
    """
    return str(uuid.uuid1())


def verifyID(id):
    """
    验证ID是否正确
    """
    try:
        uuid.UUID(id)
        return True
    except Exception as e:
        logger.warning(f"不是一个正确的UUID：{id} - {e}")
        return False


# def newUserName():
#     """
#     生成一个唯一用户名
#     """
#     username = None
#     exists = True
#     while exists:
#         username = str(random.randint(1000000000, 9999999999))
#         exists = User.objects.filter(username=username).exists()
#     return username


# def newBindCode():
#     """
#     生成一个唯一监护码
#     """
#     bindCode = None
#     exists = True
#     while exists:
#         bindCode = str(newID())[:6]
#         exists = User.objects.filter(bindCode=bindCode).exists()
#     return bindCode


# 判断用户是否登录
def checkUserLoginStatus(request):
    try:
        return bool(request.user and request.user.is_authenticated)
    except Exception as e:
        return False


# 通过token得到user模型对象
def getUserByToken(token):
    jwtAuthentication = JWTAuthentication()
    validated_token = jwtAuthentication.get_validated_token(token)
    user = jwtAuthentication.get_user(validated_token)
    return user


