from dataclasses import dataclass
from typing import List

import bs4
from bs4 import BeautifulSoup


@dataclass
class SearchResultItem:
    cover_url: str
    href: str
    title: str  # no product Id
    product_id: str
    # TODO score
    release_date: str  # yyyy-mm-dd


# https://javdb.com/search?q=stars-931
def parse_search(html: str) -> List[SearchResultItem]:
    def trasform(item: bs4.Tag) -> SearchResultItem:
        a = item.find("a")
        href = a["href"]
        cover_url = a.find("div", class_="cover").find("img")["src"]
        product_id = a.find(class_="video-title").find("strong").text.strip()
        title = a.find(class_="video-title").text.strip().lstrip(product_id).strip()
        release_date = a.find(class_="meta").text.strip()
        return SearchResultItem(
            cover_url=cover_url, href=href, title=title, product_id=product_id, release_date=release_date
        )

    soup = BeautifulSoup(html, "lxml")
    return [trasform(o) for o in soup.find(class_="movie-list").find_all(class_="item")]
