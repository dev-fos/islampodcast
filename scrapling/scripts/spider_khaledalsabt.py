# -*- coding: utf-8 -*-
import asyncio
from copy import deepcopy
from urllib.parse import urljoin

from scrapling.spiders import Spider, Request , Response

from scrapling.fetchers import AsyncDynamicSession

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

class khaledalsabtMp3Spider(Spider):
    name = "khaledalsabt_mp3_spider"
    allowed_domains = {"khaledalsabt.com"}
    start_urls = [
"https://khaledalsabt.com/interpretations/category/348/%C2%A0%D8%B4%D8%B1%D8%AD-%D9%83%D8%AA%D8%A7%D8%A8-%D8%A7%D9%84%D9%85%D8%B5%D8%A8%D8%A7%D8%AD-%D8%A7%D9%84%D9%85%D9%86%D9%8A%D8%B1-%D9%81%D9%8A-%D8%AA%D9%87%D8%B0%D9%8A%D8%A8-%D8%AA%D9%81%D8%B3%D9%8A%D8%B1-%D8%A7%D8%A8%D9%86-%D9%83%D8%AB%D9%8A%D8%B1"
    ]
    concurrent_requests = 1
    concurrent_requests_per_domain = 1
    download_delay = 1.0
#    development_mode = True
    development_mode = False

    def configure_sessions(self, manager):
        manager.add("default", AsyncDynamicSession(network_idle=True))

    async def parse(self, response: Response):

      for category in response.css("div.row.tafseer_category.list-item"):

       url =  category.css("div.d-flex.align-items-center.utility__padding__left--2em a::attr(href)").get("")
       title = category.css("p.card__title.card__title--no-border.single-line::text").get("").strip()
       absolute = urljoin(response.url , url)

       yield  response.follow(absolute , sid="default", callback=self.parse_episode, meta={"category": f"{title}",},priority=1)

      next_page = response.css('li a[rel="next"]::attr(href)').get()
      if next_page:
         next_url = urljoin(response.url, next_page)
             # نعيد استدعاء parse لمعالجة الصفحة التالية
         yield response.follow(next_url, callback=self.parse,meta=response.meta,priority=1)

    async def parse_episode(self, response: Response):

      for episode in response.css("div.row.tafseer.list-item"):

            url = episode.css("div.d-flex.align-items-center.utility__padding__left--2em a::attr(href)").get("")
            name = episode.css("p.card__title.card__title--no-border.single-line::text").get("").strip()
            category = response.meta.get('category', '')
            mp3 = episode.css('div.col.d-flex.align-items-center a::attr(href)').get("")
            absolute = urljoin(response.url , url)

            yield  response.follow(absolute , sid="default", callback=self.parse_episode_2, meta={"category": f"{category}","url" : f"{url}","mp3":  f"{mp3}", "name": f"{name}"}, priority=1)

#            yield {
#              "url" :  episode.css('div.d-flex.align-items-center.utility__padding__left--2em a::attr(href)').get(""),
#              "title": f'{category} - {name}',
#              "mp3": episode.css('div.col.d-flex.align-items-center a::attr(href)').get(""),
#              "category": f"{response.meta.get('category', '')}",
#              "duration" :  response.css('div.jp-duration::text').get("")
#              }


      next_page = response.css('li a[rel="next"]::attr(href)').get()
      if next_page:
         next_url = urljoin(response.url, next_page)
             # نعيد استدعاء parse لمعالجة الصفحة التالية
         yield response.follow(next_url, callback=self.parse_episode,meta=response.meta,priority=2 )


    async def parse_episode_2(self, response: Response):

          raw_dur = response.css("div.jp-duration::text").get("").strip()
          duration = parse_duration(raw_dur) if raw_dur else ""
          name = response.meta.get('name', '')
          category = response.meta.get('category', '')

          yield {
            "url" : response.meta.get('url', '') ,
            "mp3": response.meta.get('mp3', ''),
            "duration" :  duration ,
            "title": f'{category} - {name}',
           }

if __name__ == "__main__":

    result = khaledalsabtMp3Spider().start()
    result.items.to_jsonl("khaledalsabt_mp3_links.json")
