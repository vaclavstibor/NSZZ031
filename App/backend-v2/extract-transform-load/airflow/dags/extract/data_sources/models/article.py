from dataclasses import dataclass


@dataclass
class Article:
    """
    A class to represent an article.
    """

    id: str  # Unique identifier for the article
    type: str  # Type of the article
    section: str  # Section where the article belongs
    url: str  # URL of the article
    title: str  # Title of the article
    content: str  # Content of the article
    author: str  # Author of the article
    published_date: str  # Date when the article was published

    def to_dict(self) -> dict:
        """
        Convert the Article instance into a dictionary for JSON serialization.
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
