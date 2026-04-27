from typing import List, Dict
import chardet
from .base import BaseImporter


class TxtImporter(BaseImporter):
    async def parse_metadata(self, file_content: bytes, filename: str) -> Dict:
        detected = chardet.detect(file_content)
        encoding = detected['encoding'] or 'utf-8'
        text = file_content.decode(encoding, errors='replace')

        title = filename.replace('.txt', '')
        author = None

        lines = text.split('\n')[:20]
        for line in lines:
            if '作者' in line:
                author = line.split('：')[-1].strip() if '：' in line else line.split(':')[-1].strip()

        return {
            'title': title,
            'author': author,
            'content': text,
        }

    async def parse_chapters(self, file_content: bytes) -> List[Dict]:
        detected = chardet.detect(file_content)
        encoding = detected['encoding'] or 'utf-8'
        text = file_content.decode(encoding, errors='replace')

        chapters_data = await self.detect_chapter_pattern(text)
        chapters = []

        for i, (title, start, end) in enumerate(chapters_data):
            content = text[start:end].strip()
            chapters.append({
                'chapter_number': i + 1,
                'title': title or f'第{i + 1}章',
                'content': content,
            })

        return chapters
