from os import environ
from rest_framework import serializers

class JudgeSentence:
    def __init__(self, sentence1: str, sentence2: str):
        self.sentence1 = sentence1
        self.sentence2 = sentence2

class JudgeSentenceSerializer(serializers.Serializer):
    """Request to determine similarity between two sentences"""
    sentence1 = serializers.CharField(allow_blank=False, max_length=128, trim_whitespace=True)
    sentence2 = serializers.CharField(allow_blank=False, max_length=128, trim_whitespace=True)

    def create(self, validated_data):
        return JudgeSentence(**validated_data) #ty: ignore

ENTAIL_LIMIT = environ.get("ENTAIL_LIMIT", 0.75)

class JudgeResultSerializer(serializers.Serializer):
    label = serializers.SerializerMethodField('select_label')
    score = serializers.FloatField()

    def select_label(self, obj):
        return "ENTAIL" if obj['score'] >= ENTAIL_LIMIT else "NO_ENTAIL"
