"""Helpers."""

import logging
import re
from typing import Any

import requests

from gitscrap.type import User

logger = logging.getLogger(__name__)


def extract_name_owner(url: str) -> tuple[str, str]:
    """Extract the name and the owner from the url."""
    if url[-1] == '/':
        url = url[:-1]

    name = url.split('/')[-1]
    owner = url.split('/')[-2]

    return name, owner


def __clean_email(mail: Any) -> str | None:
    """Replace antoine+gh@test.com by antoine@test.com."""
    if isinstance(mail, str) and mail:
        return re.sub(r'\+.*@', '@', mail)
    return None


def __keep_email(mail: Any) -> bool:
    """Remove dev specific emails."""
    if isinstance(mail, str):
        prefix, suffix = mail.split('@')
        if 'git' in prefix or 'dev' in prefix or 'code' in prefix:
            return False
        if 'users.noreply.github.com' in suffix:
            return False
    return True


def deduplicate_results(users: list[User], clean: bool = False) -> dict[str, User]:
    """Clean the results."""
    results: dict[str, User] = {}

    for user in users:
        email = __clean_email(user.email) if clean else user.email
        if user.email and email != user.email:
            logger.info(f'Clean the email `{user.email}` to `{email}`')

        if email is not None:
            if not clean or (clean and __keep_email(email)):
                user.email = email
                if user.email not in results:
                    results[user.email] = user
                else:
                    results[user.email].user_type |= user.user_type
            else:
                logger.info(f'Removing email `{email}`')

    return results


def get_graphql_data_safe(response: requests.Response) -> dict:
    """Get the data from the response."""
    try:
        result = response.json()
        if result.get('data') is not None:
            return result['data']
        logger.error('Error in get_graphql_data_safe: %s', result.get('errors', {}))
    except ValueError:
        logger.error('Error in get_graphql_data_safe: %s', response.text)
    return {}
