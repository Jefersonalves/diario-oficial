import re
import datetime
from urllib.parse import urljoin

import scrapy
import dateparser

from gazette.items import Gazette
from gazette.spiders.base import BaseGazetteSpider


class RjPetropolis(BaseGazetteSpider):
    TERRITORY_ID = "3303906"
    BASE_URL = "https://www.petropolis.rj.gov.br"

    name = "rj_petropolis"
    allowed_domains = ["petropolis.rj.gov.br"]
    start_urls = [
        f"{BASE_URL}/pmp/index.php/servicos-na-web/informacoes/diario-oficial/viewcategory/3-diario-oficial.html"
    ]
    start_date = datetime.date(2001, 10, 2)

    month_name_to_number = {
        "janeiro": 1,
        "fevereiro": 2,
        "marco": 3,
        "março": 3,
        "abril": 4,
        "maio": 5,
        "junho": 6,
        "julho": 7,
        "agosto": 8,
        "setembro": 9,
        "outubro": 10,
        "novembro": 11,
        "dezembro": 12,
    }

    def parse(self, response):
        for document in response.css("#col1 div table tr td b a"):
            year = int(document.css("::text").get())
            if year >= self.start_date.year:
                year_url_sufix = document.css("::attr(href)").get()
                year_url = urljoin(self.BASE_URL, year_url_sufix)
                yield scrapy.Request(
                    url=year_url, callback=self.parse_month_page, meta={"year": year}
                )

    def parse_month_page(self, response):
        for document in response.css("#col1 div table tr td b a"):
            month_name = document.css("::text").get().lower()
            month = self.month_name_to_number[month_name]
            year = response.meta["year"]

            if datetime.date(year, month, 1) >= datetime.date(
                self.start_date.year, self.start_date.month, 1
            ):
                month_url_sufix = document.css("::attr(href)").get()
                month_url = urljoin(self.BASE_URL, month_url_sufix)
                yield scrapy.Request(url=month_url, callback=self.parse_items_page)

    def parse_items_page(self, response):
        for document in response.css(".jd_download_url"):
            document_url = document.css("a::attr(href)").get()
            url = urljoin(self.BASE_URL, document_url)
            file_url = url.replace(".html", ".pdf")

            title = document.css("::text").get().strip()
            date_match = re.search(
                r"(\d+ de \w+ de \d+)|(\d+\/\d+\/\d+)", title, re.IGNORECASE
            )
            is_extra_edition = bool(re.search(r"Suplemento", title, re.IGNORECASE))
            edition_number = re.search(r"^\d+", title).group(0)

            if date_match is not None:
                date = dateparser.parse(date_match.group(0), languages=["pt"]).date()
                yield Gazette(
                    date=date,
                    file_urls=[file_url],
                    is_extra_edition=is_extra_edition,
                    territory_id=self.TERRITORY_ID,
                    power="executive_legislative",
                    scraped_at=datetime.datetime.utcnow(),
                    edition_number=edition_number,
                )
