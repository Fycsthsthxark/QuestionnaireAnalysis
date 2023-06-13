from rest_framework import serializers

from questionnaire.models import QuestionnaireRecords


class QuestionnaireRecordsSerializers(serializers.ModelSerializer):
    class Meta:
        model = QuestionnaireRecords
        fields = "__all__"
