import pathlib
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Union

from slack_sdk import WebClient, errors
from slack_sdk.web.async_client import AsyncWebClient

from connectify.datetime_services import current_timestamp_utc
from connectify.slack_services.enums import SlackMessageResponseEnum
from connectify.slack_services.errors import SlackNotAFutureDateException


class BaseSlackConnection(ABC):
    def __init__(self, access_token: str, channel_id: str, timeout: Optional[int] = 30):
        self._access_token: str = access_token
        self._channel_id: str = channel_id
        self._client: WebClient = WebClient(self._access_token, timeout=timeout)

    @property
    def channel_id(self):
        return self._channel_id

    @abstractmethod
    def channel_conversation_history(self,
                                     channel_id: str = None,
                                     after_timestamp: Optional[int] = None,
                                     before_timestamp: Optional[int] = None,
                                     limit: int = 100
                                     ) -> Tuple[str, list]:
        raise NotImplementedError

    @abstractmethod
    def get_channel_latest_message(self, channel_id: str = None) -> Tuple[str, dict]:
        raise NotImplementedError

    @abstractmethod
    def send_text_message(self, msg: str, channel_id: str = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def send_scheduled_text_message(self, msg: str, timestamp: int, channel_id: str = None) -> str:
        raise NotImplementedError

    @abstractmethod
    def send_file_message(self,
                          file_path: Union[str, pathlib.Path],
                          title: Optional[str] = None,
                          msg: Optional[str] = None,
                          channel_id: Optional[str] = None) -> str:
        raise NotImplementedError


class SlackConnection(BaseSlackConnection):
    def __init__(self, access_token: str, channel_id: str, timeout: Optional[int] = 30):
        super().__init__(access_token=access_token, channel_id=channel_id, timeout=timeout)

    def channel_conversation_history(self,
                                     channel_id: str = None,
                                     after_timestamp: Optional[int] = None,
                                     before_timestamp: Optional[int] = None,
                                     limit: int = 100
                                     ) -> Tuple[str, list]:
        """
        Get channel conversion history for given channel
        :param channel_id: specific channel id or initialized one
        :param after_timestamp: only messages after this timestamp will be fetched, default to 1 minute before
        :param before_timestamp: only messages before this timestamp will be fetched
        :param limit: number of messages to read
        :return: status, messages list

        """
        channel_id = channel_id or self.channel_id

        before_timestamp = str(before_timestamp) if before_timestamp else None
        after_timestamp = str(after_timestamp) if after_timestamp else None

        try:
            messages: List[dict] = list()
            cursor = None
            while True:
                response = self._client.conversations_history(channel=channel_id,
                                                              cursor=cursor,
                                                              inclusive=True,
                                                              latest=before_timestamp,
                                                              oldest=after_timestamp,
                                                              limit=100)
                if response.status_code != 200:
                    raise errors.SlackApiError

                cursor_messages = response.data.get("messages", [])
                if not cursor_messages:
                    break

                messages.extend(cursor_messages)

                cursor = response.data.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break

                if len(messages) > limit:
                    break

            return SlackMessageResponseEnum.SUCCESS, messages[: limit]
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR, []

    def get_channel_latest_message(self, channel_id: str = None) -> Tuple[str, dict]:
        """
        Fetch latest message from specific channel.
        :param channel_id:  channel or initialized id
        :return: status, message tuple
        """
        status, messages = self.channel_conversation_history(channel_id, limit=1)
        if status == SlackMessageResponseEnum.ERROR:
            return status, {}

        if not messages:
            return status, {}

        return status, messages[0]

    def send_text_message(self, msg: str, channel_id: str = None) -> str:
        """
        Send text type message to specific channel
        :param msg: message to send
        :param channel_id: specific channel id or initialized one
        :return: status
        """
        channel_id = channel_id or self.channel_id
        try:
            response = self._client.chat_postMessage(channel=channel_id, text=msg)
            if response["ok"]:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError:
            return SlackMessageResponseEnum.ERROR

    def send_scheduled_text_message(self, msg: str, timestamp: int, channel_id: str = None) -> str:
        """
        Schedule text message send for specific time
        :param msg: message to send
        :param timestamp: unix epoch timestamp UTX, should be at least 15 seconds after current time
        :param channel_id: specific channel id or initialized one
        :return: status
        """
        channel_id = channel_id or self.channel_id

        # slack api doesn't work for time closer to 10 seconds
        if timestamp <= current_timestamp_utc() + 10:
            raise SlackNotAFutureDateException

        try:
            response = self._client.chat_scheduleMessage(channel=channel_id, post_at=timestamp, text=msg)

            if response:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR

    def send_file_message(self,
                          file_path: Union[str, pathlib.Path],
                          title: Optional[str] = None,
                          msg: Optional[str] = None,
                          channel_id: Optional[str] = None) -> str:
        """
        Send file to channel
        :param file_path: local path to file.
        :param title: file title
        :param msg: text message to send along with file
        :param channel_id: specific channel id or initialized one
        :return: status
        """

        channel_id = channel_id or self.channel_id
        try:
            response = self._client.files_upload_v2(filename=pathlib.Path(file_path).name,
                                                    file=str(file_path),
                                                    channel=channel_id,
                                                    title=title,
                                                    initial_comment=msg)
            if response["ok"]:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR


class AsyncSlackConnection(BaseSlackConnection):
    def __init__(self, access_token: str, channel_id: str, timeout: Optional[int] = 30):
        super().__init__(access_token=access_token, channel_id=channel_id, timeout=timeout)
        self._client = AsyncWebClient(token=self._access_token, timeout=timeout)

    async def channel_conversation_history(self,
                                           channel_id: str = None,
                                           after_timestamp: Optional[int] = None,
                                           before_timestamp: Optional[int] = None,
                                           limit: int = 100
                                           ) -> Tuple[str, list]:
        """
        Get channel conversion history for given channel
        :param channel_id: specific channel id or initialized one
        :param after_timestamp: only messages after this timestamp will be fetched, default to 1 minute before
        :param before_timestamp: only messages before this timestamp will be fetched
        :param limit: number of messages to read
        :return: status, messages list

        """
        channel_id = channel_id or self.channel_id

        before_timestamp = str(before_timestamp) if before_timestamp else None
        after_timestamp = str(after_timestamp) if after_timestamp else None

        try:
            messages: List[dict] = list()
            cursor = None
            while True:
                response = await self._client.conversations_history(channel=channel_id,
                                                                    cursor=cursor,
                                                                    inclusive=True,
                                                                    latest=before_timestamp,
                                                                    oldest=after_timestamp,
                                                                    limit=100)
                if response.status_code != 200:
                    raise errors.SlackApiError

                cursor_messages = response.data.get("messages", [])
                if not cursor_messages:
                    break

                messages.extend(cursor_messages)

                cursor = response.data.get("response_metadata", {}).get("next_cursor")
                if not cursor:
                    break

                if len(messages) > limit:
                    break

            return SlackMessageResponseEnum.SUCCESS, messages[: limit]
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR, []

    async def get_channel_latest_message(self, channel_id: str = None) -> Tuple[str, dict]:
        """
        Fetch latest message from specific channel.
        :param channel_id:  channel or initialized id
        :return: status, message tuple
        """
        status, messages = await self.channel_conversation_history(channel_id, limit=1)
        if status == SlackMessageResponseEnum.ERROR:
            return status, {}

        if not messages:
            return status, {}

        return status, messages[0]

    async def send_text_message(self, msg: str, channel_id: str = None) -> str:
        """
        Send text type message to specific channel
        :param msg: message to send
        :param channel_id: specific channel id or initialized one
        :return: status
        """
        channel_id = channel_id or self.channel_id
        try:
            response = await self._client.chat_postMessage(channel=channel_id, text=msg)
            if response["ok"]:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError:
            return SlackMessageResponseEnum.ERROR

    async def send_scheduled_text_message(self, msg: str, timestamp: int, channel_id: str = None) -> str:
        """
        Schedule text message send for specific time
        :param msg: message to send
        :param timestamp: unix epoch timestamp UTX, should be at least 15 seconds after current time
        :param channel_id: specific channel id or initialized one
        :return: status
        """
        channel_id = channel_id or self.channel_id

        # slack api doesn't work for time closer to 10 seconds
        if timestamp <= current_timestamp_utc() + 10:
            raise SlackNotAFutureDateException

        try:
            response = await self._client.chat_scheduleMessage(channel=channel_id, post_at=timestamp, text=msg)

            if response:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR

    async def send_file_message(self,
                                file_path: Union[str, pathlib.Path],
                                title: Optional[str] = None,
                                msg: Optional[str] = None,
                                channel_id: Optional[str] = None) -> str:
        """
        Send file to channel
        :param file_path: local path to file.
        :param title: file title
        :param msg: text message to send along with file
        :param channel_id: specific channel id or initialized one
        :return: status
        """

        channel_id = channel_id or self.channel_id
        try:
            response = await self._client.files_upload_v2(filename=pathlib.Path(file_path).name,
                                                          file=str(file_path),
                                                          channel=channel_id,
                                                          title=title,
                                                          initial_comment=msg)
            if response["ok"]:
                return SlackMessageResponseEnum.SUCCESS

            raise errors.SlackApiError
        except errors.SlackApiError as e:
            return SlackMessageResponseEnum.ERROR
