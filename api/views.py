from internal import core
from api import serializers
from rest_framework import status, fields
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

# Note when behind reverse proxy, need to pass IP properly
# But ideally you want to delegate ratelimit to reverse proxy in first place
from django_ratelimit.decorators import ratelimit

try:
    ST_ERROR = None
    ST = core.instance("Gameselo/STS-multilingual-mpnet-base-v2")
except Exception as error:
    ST_ERROR = str(error)
    ST = None


def convert_similarity_array(
    similarity: list[list[float]], is_bulk: bool = False
) -> Response:
    print("similarity=", len(similarity))
    data = [{"score": similarity[0]} for similarity in similarity]
    response = (
        serializers.JudgeResultSerializer(data, many=True)
        if is_bulk
        else serializers.JudgeResultSerializer(data[0], many=False)
    )
    return Response(response.data, status=status.HTTP_200_OK)


def unexpected_internal_error() -> Response:
    data = {"error": "Unexpected error"}
    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def internal_st_error() -> Response:
    data = {"error": ST_ERROR}
    return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@extend_schema(
    request=None,
    auth=None,
    responses={200: serializers.PingSerializer, 500: serializers.PingSerializer},
)
@api_view(["GET"])
def ping(request):
    """PING endpoint"""
    data = {}
    if ST is not None:
        data["status"] = "OK"
        data["max_seq_length"] = ST.max_seq_length  # ty: ignore
    else:
        data["status"] = "FAILED"
        data["error"] = ST_ERROR
    return Response(serializers.PingSerializer(data).data, status=status.HTTP_200_OK)


@extend_schema(
    request=serializers.JudgeSentenceSerializer,
    responses={
        200: serializers.JudgeResultSerializer,
        500: serializers.ErrorSerializer,
    },
)
@api_view(["POST"])
@ratelimit(key="ip", rate="5/s")
def judge(request):
    """Determine similarity between two sentences"""
    if ST is None:
        return internal_st_error()

    serializer = serializers.JudgeSentenceSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    request_data = serializer.save()

    if isinstance(request_data, serializers.JudgeSentence):
        similarity = ST.determine_similarity(
            [request_data.sentence1], [request_data.sentence2]
        )
        return convert_similarity_array(similarity)
    else:
        return unexpected_internal_error()


@extend_schema(
    request=serializers.JudgeSentenceSerializer,
    responses={
        200: serializers.JudgeResultSerializer,
        500: serializers.ErrorSerializer,
    },
)
@api_view(["POST"])
@ratelimit(key="ip", rate="5/s")
def judge_bulk(request):
    """Determine similarity between batch of the two sentences"""
    if ST is None:
        return internal_st_error()

    serializer = serializers.JudgeSentenceSerializer(
        data=request.data, many=True, max_length=100
    )
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    request_data = serializer.save()

    if isinstance(request_data, list):
        left = [data.sentence1 for data in request_data]
        right = [data.sentence2 for data in request_data]
        similarity = ST.determine_similarity(left, right)
        return convert_similarity_array(similarity, is_bulk=True)
    else:
        return unexpected_internal_error()
