# pylint: disable=no-name-in-module, too-few-public-methods

"""This file contains that type that will be used as the output of the CSV file."""

from dataclasses import dataclass
from enum import Enum


class UserType(Enum):

    """The type of the user found."""

    WATCHER = 'Watcher'
    STARGAZER = 'Stargazer'
    CONTRIBUTOR = 'Contributor'
    COMMITER = 'Commiter'


@dataclass
class User:

    """The output type that will be used for the CSV file."""

    timestamp: str
    name: str
    email: str
    url: str
    user_type: set[UserType]
