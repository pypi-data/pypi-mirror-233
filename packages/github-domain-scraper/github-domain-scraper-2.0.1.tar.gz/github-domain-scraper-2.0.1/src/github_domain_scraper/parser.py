import contextlib
import re
import time
import urllib.parse
from abc import ABC, abstractmethod
from typing import List

from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from github_domain_scraper.exceptions import InvalidSearchType
from github_domain_scraper.logger import get_logger
from github_domain_scraper.driver import SeleniumWebDriver

logger = get_logger(__file__)


class Backend(ABC):

    @abstractmethod
    def process(self, *args, **kwargs):
        pass


class Link(ABC):

    @abstractmethod
    def is_url_matched(self):
        pass

    @property
    @abstractmethod
    def meta(self):
        pass


class UserRepositoriesLink(Link):
    pattern = r'^(https:\/\/github.com\/[a-zA-Z\d](?:[a-zA-Z\d]|-(?=[a-zA-Z\d])){0,38})\/?(\?tab=[\w-]+(.*)?)?$'

    def __init__(self, url: str):
        self.url = url

    def is_url_matched(self) -> bool:
        return bool(re.match(self.pattern, self.url))

    @property
    def meta(self) -> dict:
        url = re.match(self.pattern, self.url).group(1)
        return {
            'url': f"{url}?tab=repositories",
            'xpath': '//div[@id="user-repositories-list"]/ul/li/div/div/h3/a[@href]',
            'next_xpath': '//a[@class="next_page"]'
        }


class SearchRepositoryLink(Link):
    pattern = r'^https:\/\/github.com\/search\?'
    x_paths = {
        'repositories': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'issues': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'pullrequests': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'discussions': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'users': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'commits': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'registrypackages': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'wikis': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'topics': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
        'marketplace': '//div[@data-testid="results-list"]//div[contains(@class, "search-title")]//a[1]',
    }

    def __init__(self, url: str):
        self.url = url

    def is_url_matched(self) -> bool:
        return bool(re.match(self.pattern, self.url))

    @property
    def xpath(self):
        try:
            parsed_url = urllib.parse.urlparse(self.url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            search_type = query_params['type'][0].lower()
            return self.x_paths[search_type]
        except (KeyError, IndexError):
            raise InvalidSearchType(
                'Provided link does not support extraction yet. Please contact package owner to add feature.'
            )

    @property
    def meta(self) -> dict:
        return {
            'url': self.url,
            'xpath': self.xpath,
            'next_xpath': '//a[text()="Next"]'
        }


class BackendUtility:
    webdriver_waiting_time = 10

    def __init__(self, banned_waiting_time: int = 30):
        self.wd = SeleniumWebDriver().webdriver
        self.banned_waiting_time = banned_waiting_time

    @property
    def _is_banned(self):
        return (
                bool(self.wd.find_elements(By.XPATH, "//title[contains(text(),'Rate limit')]")) or
                bool(self.wd.find_elements(By.XPATH, "//title[contains(text(),'Error 429')]"))
        )


class ListBackend(Backend, BackendUtility):
    link_classes = [
        UserRepositoriesLink,
        SearchRepositoryLink
    ]

    def __init__(self, total_links_to_download: int, **kwargs):
        super().__init__(**kwargs)
        self.total_links_to_download = total_links_to_download
        self.links = []

    def process(self, url: str) -> list:
        for link_class in self.link_classes:
            link_object = link_class(url=url)
            if link_object.is_url_matched():
                logger.debug(f'URL matched for {link_object.__class__.__name__} class')
                try:
                    self._start(link_object)
                except (NotImplementedError, InvalidSearchType) as e:
                    logger.error(e)
                break
        else:
            logger.error('Provided link does not support extraction yet. Please contact package owner to add feature.')

        return self.links

    def _start(self, link_object: Link):
        link = link_object.meta.get('url')
        if not link:
            raise NotImplementedError(
                f"meta property method of {link_object.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'url' key."
            )

        try:
            self.wd.get(link)
            self.wd.switch_to.window(self.wd.window_handles[-1])
            while link and len(self.links) < self.total_links_to_download:
                logger.info(f'Crawling url {link}')
                next_link = self._parse(link_object=link_object)
                if self._is_banned:
                    logger.info(f'Banned!! Script will retry after {self.banned_waiting_time} seconds')
                    time.sleep(self.banned_waiting_time)
                    self.wd.get(link)
                else:
                    link = next_link
                    time.sleep(1)
        except KeyboardInterrupt:
            logger.error('Stopping crawler...')
        finally:
            self.wd.quit()
            logger.info('Crawler Stopped')

    def _parse(self, link_object: Link):
        element = link_object.meta.get('xpath')
        if not element:
            raise NotImplementedError(
                f"meta property method of {link_object.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'xpath' key."
            )

        try:
            WebDriverWait(self.wd, self.webdriver_waiting_time).until(
                expected_conditions.presence_of_all_elements_located((By.XPATH, element))
            )
        except TimeoutException:
            logger.debug(f'Error in detecting links using xpath - {element}')
            return None

        repositories = [elem.get_attribute("href") for elem in self.wd.find_elements(By.XPATH, element)]
        self.links.extend(repositories)

        next_page_element = self.get_next_page_element(link_object=link_object)
        if next_page_element:
            next_page_element.click()
            time.sleep(1)
            return self.wd.current_url

    def get_next_page_element(self, link_object: Link):
        next_xpath = link_object.meta.get('next_xpath')
        if not next_xpath:
            raise NotImplementedError(
                f"meta property method of {self.__class__.__name__} class "
                f"have not implemented correctly. It must return a dict with 'next_xpath' key."
            )

        with contextlib.suppress(NoSuchElementException):
            return self.wd.find_element(By.XPATH, next_xpath)


class UserProfileBackend(Backend, BackendUtility):
    user_profile_url = "https://github.com/%s"
    fields = [
        'avatar', 'fullname', 'username', 'bio', 'followers', 'following', 'works_for', 'home_location',
        'email', 'profile_website_url', 'social', 'achievements', 'organizations', 'number_of_repositories',
        'number_of_stars', 'pinned_repositories'
    ]

    @property
    def _avatar(self):
        if elements := self.wd.find_elements(By.XPATH, '//a[@itemprop="image"]'):
            return elements[0].get_attribute('href')

    @property
    def _fullname(self):
        if elements := self.wd.find_elements(By.XPATH, '//h1[@class="vcard-names "]/span[1]'):
            return elements[0].text

    @property
    def _username(self):
        if elements := self.wd.find_elements(By.XPATH, '//h1[@class="vcard-names "]/span[2]'):
            return elements[0].text

    @property
    def _bio(self):
        if elements := self.wd.find_elements(By.XPATH, '//div[contains(@class, "user-profile-bio")]/div'):
            return elements[0].text

    @property
    def _followers(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//div[contains(@class, "js-profile-editable-area")]/div[2]//a[1]/span'
        ):
            return elements[0].text

    @property
    def _following(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//div[contains(@class, "js-profile-editable-area")]/div[2]//a[2]/span'
        ):
            return elements[0].text

    @property
    def _works_for(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//ul[@class="vcard-details"]/li[@itemprop="worksFor"]/span/div'
        ):
            return elements[0].text

    @property
    def _home_location(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//ul[@class="vcard-details"]/li[@itemprop="homeLocation"]/span'
        ):
            return elements[0].text

    @property
    def _email(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//ul[@class="vcard-details"]/li[@itemprop="email"]/a'
        ):
            return elements[0].text

    @property
    def _profile_website_url(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//ul[@class="vcard-details"]/li[@itemprop="url"]/a'
        ):
            return elements[0].text

    @property
    def _social(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//ul[@class="vcard-details"]/li[@itemprop="social"]/a'
        ):
            return [element.get_attribute('href') for element in elements]

    @property
    def _achievements(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//img[@data-hovercard-type="achievement"]'
        ):
            return list({element.get_attribute('alt').replace('Achievement: ', "") for element in elements})

    @property
    def _organizations(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//a[@data-hovercard-type="organization" and @itemprop="follows"]'
        ):
            return [element.get_attribute('href') for element in elements]

    @property
    def _number_of_repositories(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//a[@data-tab-item="repositories"]/span'
        ):
            return elements[0].text

    @property
    def _number_of_stars(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//a[@data-tab-item="stars"]/span'
        ):
            return elements[0].text

    @property
    def _pinned_repositories(self):
        if elements := self.wd.find_elements(
                By.XPATH, '//div[@class="pinned-item-list-item-content"]/div/div/a'
        ):
            return [element.get_attribute('href') for element in elements]

    def process(self, usernames: List[str]) -> dict:
        users_information = {}
        try:
            # self.wd.execute_script("window.open()")
            self.wd.switch_to.window(self.wd.window_handles[-1])
            for username in usernames:
                logger.info(f'Crawling for user {username}')
                users_information[username] = self._start(url=self.user_profile_url % username)
        except KeyboardInterrupt:
            logger.error('Stopping crawler...')
        finally:
            self.wd.quit()
            logger.info('Crawler Stopped')

        return users_information

    def _start(self, url):
        if self._is_banned:
            logger.info(f'Banned!! Script will retry after {self.banned_waiting_time} seconds')
            time.sleep(self.banned_waiting_time)
            return self._start(url)

        self.wd.get(url)
        return self.extract_fields()

    def extract_fields(self):
        return {
            field: getattr(self, f"_{field}")
            for field in self.fields
        }
