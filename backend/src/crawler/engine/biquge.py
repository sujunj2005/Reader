from typing import List, Dict
from bs4 import BeautifulSoup
from .base import BaseCrawler


class BiqugeCrawler(BaseCrawler):
    async def parse_novel_list(self, html: str) -> List[Dict]:
        soup = await self.parse_html(html)
        novels = []

        title_elem = soup.select_one(".booktitle h1") or soup.select_one("h1")
        author_elem = soup.select_one(".bookinfo .author")
        desc_elem = soup.select_one(".bookinfo .intro")
        cover_elem = soup.select_one(".bookimg img")

        if title_elem:
            novels.append({
                "title": title_elem.get_text(strip=True),
                "author": author_elem.get_text(strip=True) if author_elem else None,
                "description": desc_elem.get_text(strip=True) if desc_elem else None,
                "cover_image": cover_elem.get("src") if cover_elem else None,
            })

        return novels

    async def parse_chapter_list(self, html: str) -> List[Dict]:
        soup = await self.parse_html(html)
        chapters = []

        chapter_elems = soup.select(".listmain dd a")
        for idx, elem in enumerate(chapter_elems):
            title = elem.get_text(strip=True)
            href = elem.get("href")
            if href:
                url = href if href.startswith("http") else f"{self.source.base_url}{href}"
                chapters.append({
                    "chapter_number": idx + 1,
                    "title": title,
                    "url": url,
                })

        return chapters

    async def parse_chapter_content(self, html: str) -> str:
        soup = await self.parse_html(html)
        content_elem = soup.select_one("#content")

        if content_elem:
            text = content_elem.get_text("\n", strip=True)
            text = text.replace("请记住本书首发域名", "")
            return text.strip()

        return ""
