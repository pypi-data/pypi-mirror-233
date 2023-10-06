from __future__ import annotations
from functools import wraps
import json
from pathlib import Path

from typing import Any
import requests
from toolforge_weld.api_client import ToolforgeClient
from toolforge_weld.kubernetes_config import Kubeconfig
from toolforge_builds_cli.config import Config


ERROR_STRINGS = {
    "SERVICE_DOWN_ERROR": (
        "The build service seems to be down – please retry in a few minutes.\nIf the problem persists, "
        + "please contact us or open a bug:\nsee https://phabricator.wikimedia.org/T324822"
    ),
    "UNKNOWN_ERROR": (
        "An unknown error occured while trying to perform this operation.\nIf the problem persists, "
        + "please contact us or open a bug:\nsee https://phabricator.wikimedia.org/T324822"
    ),
}

USER_AGENT = "toolforge_builds_cli"


class BuildClientError(Exception):
    def to_str(self) -> str:
        err_str = str(self)
        try:
            err_dict = json.loads(err_str)
            return err_dict["message"]
        except json.decoder.JSONDecodeError:
            return err_str


def with_api_error(func):
    @wraps(func)
    def _inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except requests.HTTPError as error:
            raise BuildClientError(error.response.text) from error

        except requests.ConnectionError as error:
            raise BuildClientError(ERROR_STRINGS["SERVICE_DOWN_ERROR"]) from error

        except Exception as error:
            raise BuildClientError(ERROR_STRINGS["UNKNOWN_ERROR"] + f"\nOriginal error: {error}") from error

    return _inner


class BuildClient(ToolforgeClient):
    def __init__(
        self,
        kubeconfig: Kubeconfig,
        server: str,
        endpoint_prefix: str,
        user_agent: str,
    ):
        super().__init__(
            kubeconfig=kubeconfig,
            server=server + endpoint_prefix,
            user_agent=user_agent,
        )

    @classmethod
    def from_config(cls, config: Config, kubeconfig: Path):
        return cls(
            endpoint_prefix=config.builds.builds_endpoint,
            kubeconfig=Kubeconfig.load(kubeconfig.expanduser().resolve()),
            server=config.api_gateway.url,
            user_agent=USER_AGENT,
        )

    @with_api_error
    def get(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().get(url=url, json=json)

    @with_api_error
    def post(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().post(url=url, json=json)

    @with_api_error
    def put(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().put(url=url, json=json)

    @with_api_error
    def delete(self, url: str, json: dict[str, Any] | None = None) -> dict[str, Any]:
        return super().delete(url=url, json=json)
