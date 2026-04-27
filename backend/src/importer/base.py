from abc import ABC, abstractmethod
from typing import List, Dict, Tuple
import re


class BaseImporter(ABC):
    @abstractmethod
    async def parse_metadata(self, file_content: bytes, filename: str) -> Dict:
        pass

    @abstractmethod
    async def parse_chapters(self, file_content: bytes) -> List[Dict]:
        pass

    async def detect_chapter_pattern(self, text: str) -> List[Tuple[str, int, int]]:
        patterns = [
            r'第[零一二三四五六七八九十百千万0-9]+[章节回卷集篇]',
            r'Chapter\s+\d+',
        ]

        for pattern in patterns:
            regex = re.compile(pattern, re.MULTILINE)
            matches = list(regex.finditer(text))
            if len(matches) > 1:
                chapters = []
                for i, match in enumerate(matches):
                    start = match.start()
                    end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
                    title = match.group(0).strip()
                    chapters.append((title, start, end))
                return chapters

        return [("", 0, len(text))]
