"""Usage:
--------

    $ github_domain_scraper [--link=<github_link> | --github-username=<github_username>]
                            [--json=filename] [--max-repositories=<max_repositories>]

    where:
    - github_link is the URL of GitHub domain to scrape.
    - github_username is a GitHub username or a list of usernames to extract.
    - filename is the JSON file name to save results (e.g., username.json).
    - max_repositories is an optional argument to limit the number of repositories to scrape (only used with --link).

Version:
--------

- github-domain-scraper v2.0.1
"""
import argparse
import json

from github_domain_scraper.extractor import LinkExtractor, UserProfileInformationExtractor
from github_domain_scraper.logger import get_logger

logger = get_logger(__file__)


def parse():
    parser = argparse.ArgumentParser(description="GitHub Domain Scraper")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--link", type=str, help="GitHub link to scrape")
    group.add_argument("--github-username", nargs='+', type=str, help="GitHub username(s) to scrape")

    parser.add_argument("--json", type=str, help="JSON file to save results")
    parser.add_argument("--max-repositories", type=int, help="Maximum number of repositories to scrape")

    return parser.parse_args()


def extract_user_profiles(usernames, jsonfile):
    extractor = UserProfileInformationExtractor(github_username=usernames)
    result = extractor.extract()

    if jsonfile:
        with open(jsonfile, "w") as file:
            json.dump(result, file, indent=4)
        logger.info(f"Saved user's information to {jsonfile}")
    else:
        logger.info(f"Extracted user's information are {result}")


def extract_links(link, jsonfile, max_repositories):
    extractor = LinkExtractor(initial_link=link, total_links_to_download=max_repositories)
    result = extractor.extract()

    if jsonfile:
        with open(jsonfile, "w") as file:
            json.dump(result, file, indent=4)
        logger.info(f'Saved links to {jsonfile}')
    else:
        logger.info(f"Extracted domains are {result}")


def main():
    args = parse()

    if args.link:
        extract_links(args.link, args.json, args.max_repositories)

    if args.github_username:
        extract_user_profiles(args.github_username, args.json)


if __name__ == "__main__":
    main()
