from typing import List, Dict
from ebooklib import epub
import io
from bs4 import BeautifulSoup
from .base import BaseImporter


class EpubImporter(BaseImporter):
    async def parse_metadata(self, file_content: bytes, filename: str) -> Dict:
        book = epub.read_epub(io.BytesIO(file_content))

        metadata = book.get_metadata('DC', {})
        title_list = metadata.get('title', [])
        creator_list = metadata.get('creator', [])

        title = title_list[0] if title_list else filename.replace('.epub', '')
        author = creator_list[0] if creator_list else None

        return {
            'title': str(title),
            'author': str(author) if author else None,
            'book': book,
        }

    async def parse_chapters(self, file_content: bytes) -> List[Dict]:
        book_data = await self.parse_metadata(file_content, "")
        book = book_data['book']

        chapters = []
        chapter_num = 0

        for item in book.get_items():
            if item.get_type() == epub.ITEM_DOCUMENT:
                content = item.get_content().decode('utf-8', errors='replace')
                title = item.get_name()

                soup = BeautifulSoup(content, 'html.parser')
                text = soup.get_text('\n', strip=True)

                if text.strip():
                    chapter_num += 1
                    chapters.append({
                        'chapter_number': chapter_num,
                        'title': title,
                        'content': text,
                    })

        return chapters
