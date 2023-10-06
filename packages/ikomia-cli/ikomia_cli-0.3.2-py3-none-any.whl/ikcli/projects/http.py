"""Manage deployment endpoint requests."""
import base64
import datetime
import logging
import time
from typing import Generator

import requests
from yarl import URL

import ikcli.net.http.auth
import ikcli.net.http.core

logger = logging.getLogger(__name__)


class DeploymentHTTPJWTAuth(ikcli.net.http.auth.HTTPTokenAuth):
    """
    Manage JWT token directly from ikscale Project dedicated endpoint.

    This permit to:
        * get a valid JWT from ikscale token API
        * avoid share sensible oauth client_id and client_secret with cli

    But:
        * we can't properly get token using oauth flow
        * we can't refresh token using oauth flow
        * we have to use token API authentication
    """

    def __init__(self, http_request: ikcli.net.http.core.HTTPRequest, project_url: URL):
        """
        Initialize a new deployment auth class.

        Args:
            http_request: A well configured HTTPRequest on ikscale URL
            project_url: Relative URL to project
        """
        # Concat JWT endpoint to project URL and call ancestor
        super().__init__(project_url / "jwt/", None)

        self.http = http_request
        self.expires_at = datetime.datetime.now()

    def refresh(self, force: bool = False):
        """
        Get a new fresh JWT if needed.

        Args:
            force: Get a new token, even if current one is still valid

        Raises:
            ValueError: when server response is invalid
        """
        # Check if token is still valid
        if self.expires_at > datetime.datetime.now() and not force:
            logger.debug("%s JWT is still valid (expires at %s)", self.url, self.expires_at)
            return

        # Call JWT endpoint to get token
        response = self.http.get(self.url)

        # Sanity check
        if "id_token" not in response or "expires_in" not in response:
            raise ValueError(f"Can't parse server response {response}")

        # Set values
        self.token = f"Bearer {response['id_token']}"
        self.expires_at = datetime.datetime.now() + datetime.timedelta(seconds=response["expires_in"])

    def __call__(self, r: requests.PreparedRequest) -> requests.PreparedRequest:
        """
        Modify a request to set authentication header.

        If JWT token is expired, refresh automatically.

        Args:
            r: a Prepared Request

        Returns:
            An authenticated and prepared request
        """
        # Call refresh without force
        self.refresh()

        # Call parent to set header
        return super().__call__(r)


class DeploymentHTTPRequest(ikcli.net.http.core.HTTPRequest):
    """
    An HTTPRequest object to call endpoint easily.

    It manages:
      * endpoint authentication if 'DeploymentHTTPJWTAuth' is given
      * initial request data format
      * service polling to wait for response
      * response data format
    """

    def run(self, task: str, image: str, output_indexes: list = None, polling: int = 5) -> Generator[dict, None, None]:
        """
        Call deployment endpoint.

        Args:
            task: Task name to call
            image: Image filename to give
            output_indexes: List of output index to retrieve. None = All
            polling: time in seconds between 2 poll when wait for response

        Yields:
            A dict with only one entry : 'type' as key and 'data' as value.
        """
        # Load image and encode to b64
        with open(image, "rb") as fh:
            b64_image = base64.b64encode(fh.read()).decode("UTF-8")

        # Craft data
        if output_indexes is None or len(output_indexes) == 0:
            outputs = [{"task_name": task, "task_index": 0}]
        else:
            outputs = [{"task_name": task, "task_index": 0, "output_index": index} for index in output_indexes]

        data = {
            "inputs": [{"image": b64_image}],
            "outputs": outputs,
            "parameters": [],
        }

        # Query endpoint and get request UUID
        uuid = self.put(URL("/api/run"), data)

        # Wait for response complete
        response = None
        result_url = URL("api/results") / uuid

        while True:
            if response is not None and len(response) > 0:
                break
            time.sleep(polling)
            response = self.get(result_url)

        # Process response
        for line in response:
            for typ, data in line.items():
                # Convert b64 to binary if needed
                if typ in ("image", "image_binary"):
                    yield {typ: base64.b64decode(data)}
                else:
                    yield line
