# -*- coding: utf-8 -*-
import asyncio
from urllib.parse import urljoin

from scrapling.spiders import Spider, Request , Response

from scrapling.fetchers import AsyncDynamicSession

import logging

class OthmanalkhameesM4aSpider(Spider):
    name = "Othmanalkhamees_m4a_spider"
    allowed_domains = {"othmanalkhamees.com"}
    start_urls = [
"https://www.othmanalkhamees.com/lesson/562"
    ]
    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 1.0
  #  logging_level = logging.INFO
    log_file = "Alkhamees_spider.log"

    def configure_sessions(self, manager):
        manager.add("default", AsyncDynamicSession(network_idle=True))

    async def parse(self, response: Response):
       pages = response.css('a[href*="part="]')
       if not pages:
          new_url = urljoin(response.url, "?part=1")
          yield{"url": new_url}
          yield response.follow(new_url, callback=self.parse_episode)

       for page in pages:
        url = page.css('::attr(href)').get()
        if pages:
           next_url = urljoin(response.url, url)
           yield{"url2": next_url}
           yield response.follow(next_url, callback=self.parse_episode)


    async def parse_episode(self, response: Response):
        for episode in response.css("div.grid div.bg-white"):
            yield {
             "title": episode.css("h3::text").get("").strip(),
             "mp3": episode.css('div.flex a::attr(href)').get(""),
             "duration": episode.css('div.absolute.bottom-1 ::text').get("").strip(),
             }

if __name__ == "__main__":

    result = OthmanalkhameesM4aSpider().start()
    result.items.to_jsonl("Alkhamees_m4a_links.json")
