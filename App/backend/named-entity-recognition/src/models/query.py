from pydantic import BaseModel

class Query(BaseModel):
    """
    A class used to represent the Query model.

    Attributes:
        content (str): The (article's) content of the query.
    """

    content: str