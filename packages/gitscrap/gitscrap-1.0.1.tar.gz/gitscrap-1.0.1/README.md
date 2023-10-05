# GitScrap

A CLI tool for scraping email addresses from a Github repo, icluding `STARGAZERS`, `CONTRIBUTORS`, `COMMITERS` & `WATCHERS`.

## Contribute

```bash
./install-dev.sh
```

## Setup

### Get your Github token

Create a personal access token: [https://github.com/settings/tokens](https://github.com/settings/tokens).
Make sure to create a classic token, not a fine-grained token.
Make sure to enable at least those scopes:

```text
repo
read:packages
read:org
read:public_key
read:repo_hook
user
read:discussion
read:enterprise
read:gpg_key
```

### Use

Run `gitscrap`, URL being the Github repo URL to scrap. For multiple repos, just write multiple URLs:

```bash
gitscrap -t TOKEN -u URL1 URL2 URL3 -c
```

This will create a one `owner-repo.csv` file per repo in your current working directory.
