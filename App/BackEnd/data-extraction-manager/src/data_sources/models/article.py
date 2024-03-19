from dataclasses import dataclass


@dataclass
class Article:
    id: str
    type: str
    section: str
    url: str
    title: str
    content: str
    author: str
    published_date: str

    def to_dict(self) -> dict:
        """
        Convert the Article instance into a dictionary due to JSON sotring.
        """
        return {
            "id": self.id,
            "type": self.type,
            "section": self.section,
            "url": self.url,
            "title": self.title,
            "author": self.author,
            "published_date": self.published_date,
            "content": self.content,
        }
