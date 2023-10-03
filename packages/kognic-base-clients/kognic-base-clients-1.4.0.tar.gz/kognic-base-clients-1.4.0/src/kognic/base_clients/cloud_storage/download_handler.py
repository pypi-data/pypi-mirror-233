import json
import logging
from typing import Dict

import httpx

from kognic.base_clients.async_retry_support import request_with_retry

log = logging.getLogger(__name__)


class DownloadHandler:
    def __init__(self, max_retry_attempts: int = 23, max_retry_wait_time: int = 60, timeout: int = 60) -> None:
        """
        :param max_retry_attempts: Max number of attempts to retry requests to GCS.
        :param max_retry_wait_time:  Max with time before retrying requests to GCS.
        :param timeout: Max time to wait for response from server.
        """
        self.max_num_retries = max_retry_attempts
        self.max_retry_wait_time = max_retry_wait_time  # seconds
        self.timeout = timeout  # seconds

    async def get_json(self, url: str) -> Dict:
        return json.loads(await self._download_file(url, self.max_num_retries))

    async def _download_file(self, url: str, number_of_retries: int) -> bytes:
        """
        Download a json file from cloud storage

        :param url: URL of file to download
        :param number_of_retries: Number of download attempts before we stop trying to download
        :return: JSON deserialized to dictionary
        """

        async with httpx.AsyncClient() as httpx_client:
            resp = await request_with_retry(
                httpx_client.get,
                number_of_retries,
                self.max_retry_wait_time,
                url=url,
                timeout=self.timeout,
            )

        return resp.content
