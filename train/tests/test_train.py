import pytest
from unittest.mock import patch, MagicMock
from train.app import app, broadcast_speed, broadcast_station
from train.tests.conf import STATIONS


class TestTrainService:
    @pytest.fixture(autouse=True)
    def setup(self, mocker):
        self.app = app.test_client()

    @patch("train.app.redis_client", new_callable=MagicMock)
    def test_broadcast_speed(self, mock_redis):
        speed = broadcast_speed()

        mock_redis.publish.assert_called_once()

        assert 0 <= speed <= 180

    @patch("train.app.redis_client", new_callable=MagicMock)
    def test_broadcast_station(self, mock_redis):
        station = broadcast_station()

        mock_redis.publish.assert_called_once()

        assert station in STATIONS
