from pytest import fixture
from unittest.mock import MagicMock

from django.test import TestCase
from rest_framework.test import APIRequestFactory

from internal import core

MOCK_ST = MagicMock()
MOCK_ST.configure_mock(max_seq_length=256)


def mock_instance(model: str) -> MagicMock:
    return MOCK_ST


core.instance = mock_instance  # ty: ignore

from api import views


class TestEntail(TestCase):
    factory = APIRequestFactory()

    @fixture(autouse=True)
    def setup(self):
        MOCK_ST.determine_similarity = MagicMock(
            name="determine_similarity", return_value=[[0.92]]
        )

    def test_judge_entail(self):
        request = self.factory.post(
            "api/v1/judge",
            {"sentence1": "kotik", "sentence2": "cat"},
            content_type="application/json",
        )
        result = views.judge(request)
        assert result.status_code == 200
        assert result.data is not None
        assert result.data["score"] == 0.92
        assert result.data["label"] == "ENTAIL"

    def test_judge_bulk_entail(self):
        request = self.factory.post(
            "api/v1/judge/bulk",
            [{"sentence1": "kotik", "sentence2": "cat"}],
            content_type="application/json",
        )
        result = views.judge_bulk(request)
        assert result.status_code == 200
        assert result.data is not None
        assert result.data[0]["score"] == 0.92
        assert result.data[0]["label"] == "ENTAIL"


class TestNotEntail(TestCase):
    factory = APIRequestFactory()

    @fixture(autouse=True)
    def setup(self):
        MOCK_ST.determine_similarity = MagicMock(return_value=[[0.72]])

    def test_judge_not_entail(self):
        request = self.factory.post(
            "api/v1/judge",
            {"sentence1": "kotik", "sentence2": "cat"},
            content_type="application/json",
        )
        result = views.judge(request)
        assert result.status_code == 200
        assert result.data is not None
        assert result.data["score"] == 0.72
        assert result.data["label"] == "NO_ENTAIL"

    def test_judge_bulk_not_entail(self):
        request = self.factory.post(
            "api/v1/judge/bulk",
            [{"sentence1": "kotik", "sentence2": "cat"}],
            content_type="application/json",
        )
        result = views.judge_bulk(request)
        assert result.status_code == 200
        assert result.data is not None
        assert result.data[0]["label"] == "NO_ENTAIL"
        assert result.data[0]["score"] == 0.72
