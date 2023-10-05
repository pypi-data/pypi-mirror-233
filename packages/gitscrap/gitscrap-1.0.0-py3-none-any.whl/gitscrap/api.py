"""Github API wrapper."""

import logging

# Configure the logger
import requests

from gitscrap.helpers import get_graphql_data_safe

logger = logging.getLogger(__name__)


class GithubAPI:
    """Manipulate the Github API"""

    token: str
    header: dict
    url: str
    sucess_status: int = 200

    def __init__(self, token: str, url: str = 'https://api.github.com/graphql'):
        """Init."""
        self.token = token
        self.header = {'Authorization': f'bearer {self.token}'}
        self.url = url

        if not self.valid_token():
            raise ValueError('The token given is not valid')

        logger.info('Github API initialized')

    def valid_token(self) -> bool:
        response = requests.post(self.url, headers=self.header, json={'query': '{__typename}'}, timeout=10)
        result = response.json()

        return result.get('data') is not None

    def count_contributors(self, owner: str, repo: str) -> int:
        """Count contributors."""

        query = """query($owner: String!, $repo: String!) {
            repository(name: $repo, owner: $owner){
                defaultBranchRef {
                    name
                    target {
                        ... on Commit {
                            id
                            history {
                                totalCount
                            }
                        }
                    }
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner}

        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        return data['repository']['defaultBranchRef']['target']['history']['totalCount']

    def get_contributors(self, owner: str, repo: str, after: str | None) -> tuple[list, str] | tuple[None, None]:
        """Get contributors."""

        query = """query($owner: String!, $repo: String!, $after: String) {
            repository(name: $repo, owner: $owner){
                defaultBranchRef {
                    name
                    target {
                        ... on Commit {
                            id
                            history (first: 100, after: $after) {
                                edges {
                                    cursor
                                    node {
                                        committer {
                                        user{
                                                name
                                                email
                                                url
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner, 'after': after}

        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        tmp = data['repository']['defaultBranchRef']['target']['history']
        cursor = tmp['edges'][-1]['cursor']
        contributors: list = list(filter(None, [node['node']['committer']['user'] for node in tmp['edges']]))

        return contributors, cursor

    def count_stargazers(self, owner: str, repo: str) -> int:
        query = """query($owner: String!, $repo: String!) {
            repository(name: $repo, owner: $owner) {
                stargazers{
                    totalCount
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner}

        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        return data['repository']['stargazers']['totalCount']

    def get_stargazers(self, owner: str, repo: str, after: str | None = None) -> tuple[list, str] | tuple[None, None]:
        query = """query($owner: String!, $repo: String!, $after: String) {
            repository(name: $repo, owner: $owner){
                stargazers(first:100, after: $after){
                    edges{
                        cursor
                    }
                    nodes{
                        name
                        email
                        url
                    }
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner, 'after': after}

        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        tmp = data['repository']['stargazers']
        stargazers = tmp['nodes']
        cursor = tmp['edges'][-1]['cursor']

        return stargazers, cursor

    def count_watchers(self, owner: str, repo: str) -> int:
        query = """query($owner: String!, $repo: String!) {
            repository(name: $repo, owner: $owner) {
                watchers{
                    totalCount
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner}
        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        return data['repository']['watchers']['totalCount']

    def get_watchers(self, owner: str, repo: str, after: str | None) -> tuple[list, str] | tuple[None, None]:
        query = """query($owner: String!, $repo: String!, $after: String) {
            repository(name: $repo, owner: $owner){
                watchers(first:100, after: $after){
                    edges{
                        cursor
                    }
                    nodes{
                        name
                        email
                        url
                    }
                }
            }
        }"""

        variables = {'repo': repo, 'owner': owner, 'after': after}

        r = requests.post(self.url, json={'query': query, 'variables': variables}, headers=self.header, timeout=10)
        data = get_graphql_data_safe(r)

        tmp = data['repository']['watchers']
        watchers = tmp['nodes']
        cursor = tmp['edges'][-1]['cursor']

        return watchers, cursor
