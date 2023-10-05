"""Main.

You can directly import the main function in your code.
"""
import logging
import math
import os
import re
import shutil
import subprocess
from datetime import datetime

from gitscrap.api import GithubAPI
from gitscrap.type import User, UserType

logger = logging.getLogger(__name__)

MAX_RESULTS_PER_API_CALL = 100


def scrape_stargazers(owner: str, repo: str, github_api: GithubAPI) -> list[User]:
    """Scrap all Stargazers using Github GraphQL API."""

    results: list[User] = []

    total_count = github_api.count_stargazers(owner, repo)
    logger.info(f'Total Count Stargazers: {total_count}')

    number_of_loops = math.ceil(total_count / MAX_RESULTS_PER_API_CALL)
    cursor: str | None = None

    for i in range(number_of_loops):
        stargazers, cursor = github_api.get_stargazers(owner, repo, cursor)

        if stargazers is not None:
            for node in stargazers:
                if node['email']:
                    results.append(
                        User(
                            timestamp=f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                            name=node['name'],
                            email=node['email'],
                            url=node['url'],
                            user_type={UserType.STARGAZER},
                        ),
                    )

        logger.debug(f'Stargazers: Loop: {i} | Cursor: {cursor}')

    logger.info(f'Found Stargazers: {len(results)}')

    return results


def scrape_watchers(owner: str, repo: str, github_api: GithubAPI) -> list[User]:
    """Scrap all Watchers using Github GraphQL API."""

    results: list[User] = []

    total_count = github_api.count_watchers(owner, repo)
    logger.info(f'Total Count Watchers: {total_count}')

    number_of_loops = math.ceil(total_count / MAX_RESULTS_PER_API_CALL)
    cursor: str | None = None

    for i in range(number_of_loops):
        watchers, cursor = github_api.get_watchers(owner, repo, cursor)

        if watchers is not None:
            for node in watchers:
                if node['email']:
                    results.append(
                        User(
                            timestamp=f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                            name=node['name'],
                            email=node['email'],
                            url=node['url'],
                            user_type={UserType.WATCHER},
                        ),
                    )

        logger.debug(f'Watchers: Loop: {i} | Cursor: {cursor}')

    logger.info(f'Found Watchers: {len(results)}')

    return results


def scrape_contributors(owner: str, repo: str, github_api: GithubAPI) -> list[User]:
    """Scrap all Contributors using Github GraphQL API."""

    results: list[User] = []

    total_count = github_api.count_contributors(owner, repo)
    logger.info(f'Total Count Contributors: {total_count}')

    number_of_loops = math.ceil(total_count / MAX_RESULTS_PER_API_CALL)
    cursor: str | None = None

    for i in range(number_of_loops):
        contributors, cursor = github_api.get_contributors(owner, repo, cursor)

        if contributors is not None:
            for node in contributors:
                if node['email']:
                    results.append(
                        User(
                            timestamp=f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                            name=node['name'],
                            email=node['email'],
                            url=node['url'],
                            user_type={UserType.CONTRIBUTOR},
                        ),
                    )

        logger.debug(f'Contributors: Loop: {i} | Cursor: {cursor}')

    logger.info(f'Found Contributors: {len(results)}')

    return results


def scrape_commiters(url: str, repo: str) -> list[User]:
    """Scrap commiters from a Git repository by cloning it."""

    try:
        subprocess.run(['git', 'clone', url], check=True)  # noqa: S603, S607
    except subprocess.CalledProcessError:
        logger.error('Error: Failed to clone the repository.')
        return []

    # Change directory to the cloned repository
    os.chdir(repo)

    # Extract commit emails using git log
    try:
        log_output = subprocess.check_output(
            ['git', 'log', '--pretty=format:%ae'],  # noqa: S603, S607
            universal_newlines=True,
        )
    except subprocess.CalledProcessError:
        logger.error('Error: Failed to retrieve the git log.')
        return []

    # Use a regex to extract email addresses
    email_regex = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = set(re.findall(email_regex, log_output))

    # Change back to the original directory
    os.chdir('..')
    shutil.rmtree(repo)

    results: list[User] = []
    for email in emails:
        results.append(
            User(
                timestamp=f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}',
                name=email,
                email=email,
                url=email,
                user_type={UserType.COMMITER},
            ),
        )

    logger.info(f'Found Commiters: {len(results)}')
    return results
