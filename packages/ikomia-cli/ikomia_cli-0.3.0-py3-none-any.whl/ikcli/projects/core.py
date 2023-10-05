"""Project API Object."""
import re
from pathlib import Path

from yarl import URL

from ikcli.common.core import Members
from ikcli.net.api import List, Object
from ikcli.net.http.core import HTTPRequest

from .archive import Archive
from .http import DeploymentHTTPJWTAuth, DeploymentHTTPRequest


class Deployment(Object):
    """Deployment API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Deployment object.

        Returns:
            Deployment object representation
        """
        return f"Deployment {self['provider']} {self['region']} {self['flavour']} {self['endpoint']}"

    def get_endpoint_http_request(self) -> DeploymentHTTPRequest:
        """
        Return a HTTPRequest object configured to easily call deployment endpoint.

        Returns:
            A fully configured HTTPRequest object

        Raises:
            ValueError: when can't extract project url from this deployment url
        """
        # Extract project url from deployment url
        m = re.match(r"^(?P<project_url>.*projects\/[0-9a-f-]+\/)", format(self._url))
        if m is None:
            raise ValueError(f"Can't extract project URL from '{self._url}'")
        project_url = URL(m.group("project_url"))

        # Get endpoint authenticator
        auth = DeploymentHTTPJWTAuth(self._http, project_url)

        # Get deployment endpoint HTTP request
        return DeploymentHTTPRequest(URL(self["endpoint"]), auth=auth, timeout=180)


class Deployments(List):
    """Deployment API List."""

    def __init__(self, http: HTTPRequest, url: URL):
        """
        Initialize a new Deployments object.

        Args:
            http: A HTTPRequest object to talk with api
            url: Absolute or relative path to Deployments
        """
        super().__init__(http, url, Deployment)


class Workflow(Object):
    """Workflow API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of Workflow object.

        Returns:
            Workflow object representation
        """
        return f"Workflow {self['name']}"

    @property
    def deployments(self) -> Deployments:
        """
        Return workflow deployment list.

        Returns:
            workflow deployment list
        """
        return Deployments(self._http, self._url / "deployments/")


class Workflows(List):
    """Workflow API List."""

    def __init__(self, http: HTTPRequest, url: URL):
        """
        Initialize a new Workflows object.

        Args:
            http: A HTTPRequest object to talk with api
            url: Absolute or relative path to Workflows
        """
        super().__init__(http, url, Workflow)

    def create(self, filename: Path) -> Workflow:
        """
        Create a new workflow from filename.

        Args:
            filename: Workflow json file name

        Returns:
            A new workflow
        """
        with Archive(filename) as zfh:
            data = self._http.post(self._url, None, files={"archive": zfh})
            return Workflow(self._http, URL(data["url"]), data=data)


class Project(Object):
    """Project API Object."""

    def __repr__(self) -> str:
        """
        Return a representation of object.

        Returns:
            Object representation
        """
        return f"Project {self['name']}"

    @property
    def members(self) -> Members:
        """
        Return member list.

        Returns:
            Member list
        """
        return Members(self._http, self._url / "members/")

    @property
    def workflows(self) -> Workflows:
        """
        Return project workflow list.

        Returns:
            Project workflow list
        """
        return Workflows(self._http, self._url / "workflows/")


class Projects(List):
    """Project API List."""

    def __init__(self, http, url: URL = None):
        """
        Initialize a new Projects object.

        Args:
            http: A HTTPRequest object to talk with api
            url: Absolute or relative path to Projects
        """
        if url is None:
            url = URL("/v1/projects/")
        super().__init__(http, url, Project)
