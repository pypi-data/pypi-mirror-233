# coding: utf-8

import logging
from dataclasses import dataclass
from typing import List
import requests
from urllib.parse import urljoin
import asyncio

from bs4 import BeautifulSoup
import aiohttp
from unidecode import unidecode

from lefaso_net_scraper import settings


logger = logging.getLogger(__name__)


__all__ = [
    'Article',
    'LefasoNetUrlError',
    'LefasoNetScraper',
]


@dataclass
class Article:

    article_topic: str
    article_title: str
    article_published_date: str
    article_origin: str
    article_url: str
    article_content: str
    article_comments: List[str]

    @staticmethod
    def to_dict(**kwargs) -> dict:
        return Article(**kwargs).__dict__


class LefasoNetUrlError(Exception):

    def __str__(self) -> str:
        return "Exception LefasoNetUrlError, lefaso.net url is expected"


class LefasoNetScraper:

    _topic_url: str
    _pagination_range: range

    def __init__(self, topic_url: str) -> None:
        self._topic_url = topic_url
        self._pagination_range = self._get_topic_pagination_range()

    def run(self):
        data = asyncio.run(self._get_articles_data())
        return data

    async def _get_articles_data(self) -> List[dict]:
        articles = []
        for pagination in self._pagination_range:
            url = self._topic_url + settings.LEFASO_PAGINATION_TEMPLATE
            page_url = url.format(pagination)
            logger.info(f"Page url: {page_url}")
            articles_urls_and_date = self._get_articles_urls_and_date(page_url)  # noqa: E501
            async with aiohttp.ClientSession() as session:
                for article_url, article_date in articles_urls_and_date:
                    async with session.get(article_url) as response:
                        html = await response.text()
                        soup = BeautifulSoup(html, 'html.parser')
                        article_topic = soup.select('#hierarchie > a')[-1].text
                        article_title = soup.select('.entry-title')[-1].text
                        article_origin = settings.LAFASO_URL.geturl()
                        article_summary = soup.select('div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > h3')[0].text  # noqa: E501
                        article_content = article_summary
                        try:
                            for p in soup.select('div.col-xs-12.col-sm-12.col-md-8.col-lg-8 > div.article_content > p'):  # noqa: E501
                                article_content += p.text
                        except Exception:
                            logger.warning(f"Unable to find content at {article_url}")  # noqa: E501
                        article_comments = []
                        comments_div = soup.select('.comment-texte')
                        for comment in comments_div:
                            if comment is not None or comment != '':
                                comment_text = unidecode(comment.text)
                                article_comments.append(comment_text)

                        article = Article.to_dict(
                            article_topic=unidecode(article_topic),
                            article_title=unidecode(article_title),
                            article_published_date=article_date,
                            article_origin=article_origin,
                            article_url=article_url,
                            article_content=unidecode(article_content),
                            article_comments=article_comments,
                        )
                        articles.append(article)
        return articles

    def _get_articles_urls_and_date(self, page_url: str) -> List[tuple]:
        articles_urls_and_date: list = []
        response = requests.get(page_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        articls_container = soup.find_all('div', settings.LEFASO_ARTICLES_CONTAINER)  # noqa: E501
        articles_divs = articls_container[0].find_all('div', 'col-xs-12 col-sm-12 col-md-8 col-lg-8')  # noqa: E501
        for article_div in articles_divs:
            article_path = article_div.select('h3 > a')[0]['href']
            article_published_date = article_div.select('abbr.published')
            article_published_date = article_published_date[0]['title']
            article_url = urljoin(settings.LAFASO_URL.geturl(), article_path)
            articles_urls_and_date.append((article_url, article_published_date))  # noqa: E501
        return articles_urls_and_date

    def _get_topic_pagination_range(self) -> range:
        if not self._topic_url.startswith(settings.LAFASO_URL):
            raise LefasoNetUrlError
        response = requests.get(self._topic_url)
        soup = BeautifulSoup(response.content, 'html.parser')
        start_of_pagination = 0
        end_of_pagination = int(soup.select('.pagination > .pages > a')[-1].text)  # noqa: E501
        pagination_range = range(
            start_of_pagination,
            end_of_pagination + settings.LEFASO_PAGINATION_STEP,
            settings.LEFASO_PAGINATION_STEP
        )
        logger.info(f"Pagination from {start_of_pagination} to {end_of_pagination}")  # noqa: E501
        return pagination_range

    def set_pagination_range(self, start: int, stop: int) -> None:
        if start < 0 or stop < 0:
            logger.error("Invalid start or stop value")
            raise ValueError
        new_range = range(start, stop, settings.LEFASO_PAGINATION_STEP)
        logger.info(f"Settings pagination range from {start} to {stop}")
        self._pagination_range = new_range
