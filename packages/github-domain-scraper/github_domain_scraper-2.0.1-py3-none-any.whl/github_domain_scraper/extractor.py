import os
import sys
from typing import Optional, Union, List

from github_domain_scraper.logger import get_logger
from github_domain_scraper.parser import ListBackend, UserProfileBackend

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
logger = get_logger(__file__)


class LinkExtractor:
    def __init__(self, initial_link: str, total_links_to_download: Optional[int] = None):
        self.initial_link = initial_link
        self.total_links_to_download = total_links_to_download or sys.maxsize

    def extract(self):
        logger.info('Extracting...')
        parser = ListBackend(total_links_to_download=self.total_links_to_download)
        return parser.process(url=self.initial_link)[:self.total_links_to_download]


class UserProfileInformationExtractor:
    def __init__(self, github_username: Union[str, List[str]]):
        self.github_usernames = github_username if isinstance(github_username, list) else [github_username]

    def extract(self):
        logger.info('Extracting...')
        parser = UserProfileBackend()
        return parser.process(usernames=self.github_usernames)