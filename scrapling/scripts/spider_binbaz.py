# -*- coding: utf-8 -*-
import asyncio
from copy import deepcopy
from urllib.parse import urljoin

from scrapling.spiders import Spider, Request , Response

from scrapling.fetchers import AsyncDynamicSession

import logging

import uvloop

def parse_duration(raw: str) -> str:
    raw = raw.strip()
    raw = raw.lstrip("-")

    parts = raw.split(":")

    if len(parts) == 2:
        minutes, seconds = map(int, parts)

        if minutes >= 60:
            hours = minutes // 60
            minutes = minutes % 60
            return f"{hours}:{minutes:02d}:{seconds:02d}"
        return f"{minutes:02d}:{seconds:02d}"


    if len(parts) == 3:
        hours, minutes, seconds = map(int, parts)
        return f"{hours}:{minutes:02d}:{seconds:02d}"

    return raw


    return f"{hours}:{minutes:02d}:{seconds:02d}"

class BinbazMp3Spider(Spider):
    name = "binbaz_mp3_spider"
    allowed_domains = {"binbaz.org.sa"}
    start_urls = [
"https://binbaz.org.sa/fatwas/kind/2"
    ]
    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 1.0
  #  logging_level = logging.INFO
    log_file = "binbaz_spider.log"

    def configure_sessions(self, manager):
        manager.add("default", AsyncDynamicSession(network_idle=True))

# manager.add("default", AsyncDynamicSession(network_idle=True,max_pages=10))


    async def parse(self, response: Response):
       for episode in response.css(".box__body__element h1 a::attr(href)").getall():
        yield response.follow(episode , sid="default", callback=self.parse_episode)

       next_page = response.css('li a[rel="next"]::attr(href)').get()
       if next_page:
             yield Request(next_page, callback=self.parse)

    async def parse_episode(self, response: Response):

      raw_dur = response.css("div.jp-duration::text").get("").strip()
      duration = parse_duration(raw_dur) if raw_dur else ""

      yield {
        "title": response.css("h1::text").get("").strip(),
        "mp3": response.css('.box__body a[href$=".mp3"]::attr(href)').get(""),
#        "o-duration": response.css("div.jp-duration::text").get("").strip(),
        "duration": duration
    }

if __name__ == "__main__":

    result = BinbazMp3Spider(crawldir="spider", interval=600.0).start(use_uvloop=True)
    result.items.to_jsonl("binbaz_mp3_links.json")
