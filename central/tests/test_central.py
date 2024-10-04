from unittest.mock import patch, ANY
from central.app import (
    handle_speed_message,
    handle_station_message,
    raise_gate,
)
from central.tests.conf import (
    GATEKEEPER_URL,
    SLOW_LOG,
    NORMAL_LOG,
    FAST_LOG,
)


class TestCentralService:

    @patch("central.app.log_speed")
    def test_handle_speed_message_slow(self, mock_log_speed):
        message = {"data": b"35"}
        handle_speed_message(message)

        mock_log_speed.assert_called_once_with(SLOW_LOG, 35.0, ANY)

    @patch("central.app.log_speed")
    def test_handle_speed_message_normal(self, mock_log_speed):
        message = {"data": b"100"}
        handle_speed_message(message)

        mock_log_speed.assert_called_once_with(NORMAL_LOG, 100.0, ANY)

    @patch("central.app.log_speed")
    def test_handle_speed_message_fast(self, mock_log_speed):
        message = {"data": b"150"}
        handle_speed_message(message)

        mock_log_speed.assert_called_once_with(FAST_LOG, 150.0, ANY)

    @patch("central.app.requests.post")
    @patch("central.app.requests.get")
    @patch("central.app.logging.info")
    @patch("central.app.logging.error")
    def test_handle_station_message_gate_open(
        self, mock_error, mock_info, mock_get, mock_post
    ):
        message = {"data": b"Warszawa Centralna"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": True}

        handle_station_message(message)

        mock_get.assert_called_once_with(GATEKEEPER_URL)
        mock_post.assert_called_once_with(
            GATEKEEPER_URL, json={"status": False}
        )
        mock_info.assert_any_call(
            "Gate is open. Requesting to lower the gate."
        )

    @patch("central.app.requests.post")
    @patch("central.app.requests.get")
    @patch("central.app.logging.info")
    @patch("central.app.logging.error")
    def test_handle_station_message_gate_closed(
        self, mock_error, mock_info, mock_get, mock_post
    ):
        message = {"data": b"Warszawa Centralna"}
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {"status": False}

        handle_station_message(message)

        mock_get.assert_called_once_with(GATEKEEPER_URL)
        mock_post.assert_not_called()
        mock_error.assert_called_once_with("Gate is closed. No action taken.")

    @patch("central.app.requests.post")
    @patch("central.app.logging.info")
    def test_raise_gate(self, mock_info, mock_post):
        raise_gate()

        mock_post.assert_called_once_with(
            GATEKEEPER_URL, json={"status": True}
        )
        mock_info.assert_called_once_with("Raising gate after 10 seconds.")
