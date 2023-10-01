import asyncio
import inspect
import os
import unittest
from datetime import datetime, timezone

from connectify.configuration_services import load_env_variables_from_file
from connectify.datetime_services import current_timestamp_utc, timestamp_utc_before_n_seconds
from connectify.file_services import TempFileWithContent
from connectify.slack_services.slack_connection import SlackConnection, AsyncSlackConnection


class TestSlackConnection(unittest.TestCase):
    def setUp(self) -> None:
        load_env_variables_from_file(".env.dev")
        self.connection = SlackConnection(access_token=os.environ.get("SLACK_ACCESS_TOKEN"),
                                          channel_id=os.environ.get("SLACK_CHANNEL_ID"))

    @property
    def test_message(self):
        current_time_str = datetime.now(tz=timezone.utc).isoformat(sep=" ", timespec="seconds")
        return f"test: {inspect.stack()[1][3]}, time: {current_time_str}"

    def test_send_text_message(self):
        status = self.connection.send_text_message(self.test_message)
        assert status == "success", "failed to send text message"

    def test_send_scheduled_text_message(self):
        timestamp_after_5_seconds = current_timestamp_utc() + 15

        status = self.connection.send_scheduled_text_message(msg=self.test_message, timestamp=timestamp_after_5_seconds)
        assert status == "success", "failed to send scheduled text message"

    def test_channel_history(self):
        status = self.connection.send_text_message(self.test_message)
        assert status == "success", "couldn't send message to test channel message history"

        after_timestamp = timestamp_utc_before_n_seconds(60)
        status, data = self.connection.channel_conversation_history(after_timestamp=after_timestamp)

        assert status == "success", "failed to get channel history"
        assert len(data) > 0, "number of messages should be > 0"

    def test_get_latest_message(self):
        """May fail in case of async tests"""
        test_message = self.test_message
        status = self.connection.send_text_message(self.test_message)
        assert status == "success", "couldn't send message to test channel message history"

        status, message = self.connection.get_channel_latest_message()

        assert status == "success"
        assert message["text"] == test_message, \
            f"incorrect message fetched. should be: {test_message}, actual: {message['text']}"

    def test_file_upload(self):
        with TempFileWithContent(self.test_message, "test.txt") as temp_file:
            status = self.connection.send_file_message(temp_file.path, title="Test file")

        assert status == "success", "couldn't upload the file"


class TestAsyncSlackConnection(unittest.TestCase):
    def setUp(self) -> None:
        load_env_variables_from_file(".env.dev")
        self.connection = AsyncSlackConnection(access_token=os.environ.get("SLACK_ACCESS_TOKEN"),
                                               channel_id=os.environ.get("SLACK_CHANNEL_ID"))

    @property
    def test_message(self):
        current_time_str = datetime.now(tz=timezone.utc).isoformat(sep=" ", timespec="seconds")
        return f"test: {inspect.stack()[1][3]}, time: {current_time_str}"

    def test_channel_history(self):
        loop = asyncio.new_event_loop()

        status = loop.run_until_complete(self.connection.send_text_message(self.test_message))
        assert status == "success", "couldn't send message to test channel message history"

        after_timestamp = timestamp_utc_before_n_seconds(60)

        status, data = loop.run_until_complete(
            self.connection.channel_conversation_history(after_timestamp=after_timestamp))

        assert status == "success", "failed to get channel history"
        assert len(data) > 0, "number of messages should be > 0"

    def test_send_text_message(self):
        loop = asyncio.new_event_loop()

        status = loop.run_until_complete(self.connection.send_text_message(self.test_message))
        assert status == "success", "failed to send text message"

    def test_send_scheduled_text_message(self):
        timestamp_after_5_seconds = current_timestamp_utc() + 15
        loop = asyncio.new_event_loop()
        status = loop.run_until_complete(
            self.connection.send_scheduled_text_message(msg=self.test_message, timestamp=timestamp_after_5_seconds))
        assert status == "success", "failed to send scheduled text message"

    def test_get_latest_message(self):
        """May fail in case of async tests"""
        test_message = self.test_message
        loop = asyncio.new_event_loop()
        status = loop.run_until_complete(self.connection.send_text_message(self.test_message))
        assert status == "success", "couldn't send message to test channel message history"

        status, message = loop.run_until_complete(self.connection.get_channel_latest_message())

        assert status == "success"
        assert message["text"] == test_message, \
            f"incorrect message fetched. should be: {test_message}, actual: {message['text']}"

    def test_file_upload(self):
        with TempFileWithContent(self.test_message, "test.txt") as temp_file:
            loop = asyncio.new_event_loop()
            status = loop.run_until_complete(self.connection.send_file_message(temp_file.path, title="Test file"))

        assert status == "success", "couldn't upload the file"
