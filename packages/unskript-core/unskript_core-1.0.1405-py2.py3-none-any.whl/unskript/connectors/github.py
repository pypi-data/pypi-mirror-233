from typing import Any
from github import Github
from pydantic import ValidationError

from unskript.connectors.interface import ConnectorInterface
from unskript.connectors.schema.github import GithubSchema


class GithubConnector(ConnectorInterface):
    def get_handle(self, data) -> Any:
        try:
            githubCredential = GithubSchema(**data)
        except ValidationError as e:
            raise e
        try:
            if githubCredential.hostname=='':
                githubClient = Github(githubCredential.token.get_secret_value())
            else:
                base_url = "https://"+ githubCredential.hostname +"/api/v3"
                githubClient = Github(base_url=base_url, login_or_token=githubCredential.token.get_secret_value())
        except Exception as e:
            raise e

        return githubClient
