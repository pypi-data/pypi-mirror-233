"""Main.

You can directly import the main function in your code.
"""
import argparse
import csv
import logging
import time
from dataclasses import fields

from gitscrap.api import GithubAPI
from gitscrap.helpers import deduplicate_results, extract_name_owner
from gitscrap.scrapers import scrape_commiters, scrape_contributors, scrape_stargazers, scrape_watchers
from gitscrap.type import User

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# pylint: disable=too-many-branches, too-many-statements
def main() -> None:
    """Entrypoint."""

    # First we have to add the two commands that will be used
    # 1- The command to add the token to the script
    # 2- The command to add the URL to the script
    parser = argparse.ArgumentParser(
        description='This script takes a GitHub URL and scrapes the emails of the stargazers, watchers, and contributors of the repository.',
    )
    parser.add_argument('-t', '--token', required=True, help='The GitHub token to use for the API calls.')
    parser.add_argument('-u', '--url', required=True, help='The GitHub URL to scrape.')
    parser.add_argument(
        '-c', '--clean', action=argparse.BooleanOptionalAction, help='Clean dev related info from the emails'
    )
    args = parser.parse_args()

    # Find the owner and the name of the repository
    name, owner = extract_name_owner(args.url)
    clean = args.clean

    # Now that we have everything to start the scraping
    # First we must make sure that the token given is authentic
    # To do that just send typename to the API
    github_api = GithubAPI(args.token)

    # Now since we made sure that the token is valid. It is time to start scrapping
    results: list[User] = []

    results = scrape_stargazers(owner, name, github_api)
    time.sleep(0.5)
    results += scrape_watchers(owner, name, github_api)
    time.sleep(0.5)
    results += scrape_contributors(owner, name, github_api)
    time.sleep(0.5)
    results += scrape_commiters(args.url, name)

    users = deduplicate_results(results, clean)

    logger.info(f'Found a total of {len(users)} users')

    with open(f'{owner}-{name}.csv', 'w', newline='') as csvfile:
        # Extract field names from the dataclass
        fieldnames = [field.name for field in fields(User)]

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        # Write rows to CSV
        for person in users.values():
            writer.writerow({field: getattr(person, field) for field in fieldnames})
