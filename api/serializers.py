from os import environ
from enum import Enum

from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field


class JudgeSentence:
    def __init__(self, sentence1: str, sentence2: str):
        self.sentence1 = sentence1
        self.sentence2 = sentence2


class JudgeSentenceSerializer(serializers.Serializer):
    """Request to determine similarity between two sentences"""

    sentence1 = serializers.CharField(
        allow_blank=False, max_length=128, trim_whitespace=True
    )
    sentence2 = serializers.CharField(
        allow_blank=False, max_length=128, trim_whitespace=True
    )

    def create(self, validated_data):
        return JudgeSentence(**validated_data)  # ty: ignore


# 0.75 is good number
# Values below 0.70 always for sentences that are not similar enough while typical run on similar sentence give value within 0.8
ENTAIL_LIMIT = environ.get("ENTAIL_LIMIT", 0.75)


# inherit str to enable serialization into str
class JudgeLabel(str, Enum):
    ENTAIL = "ENTAIL"
    NO_ENTAIL = "NO_ENTAIL"


class JudgeResultSerializer(serializers.Serializer):
    label = serializers.SerializerMethodField("select_label")
    score = serializers.FloatField()

    def select_label(self, obj) -> JudgeLabel:
        return (
            JudgeLabel.ENTAIL if obj["score"] >= ENTAIL_LIMIT else JudgeLabel.NO_ENTAIL
        )


class PingSerializer(serializers.Serializer):
    status = serializers.CharField(required=False)
    max_seq_length = serializers.IntegerField()
    error = serializers.CharField(required=False)


class ErrorSerializer(serializers.Serializer):
    error = serializers.CharField()
