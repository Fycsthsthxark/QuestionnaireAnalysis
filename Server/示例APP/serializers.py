from rest_framework import serializers
from 示例APP.models import User


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
