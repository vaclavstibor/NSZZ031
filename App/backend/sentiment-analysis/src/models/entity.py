from pydantic import BaseModel

class Entity(BaseModel):
    """
    A class used to represent the Entity model.

    Attributes:
        text (str): The text of the entity.
        ticker (str): The ticker of the entity.
    """

    text: str
    ticker: str

    def __hash__(self):
        """
        Compute a hash value for an Entity instance.

        This is needed because we want to use Entity instances as keys in a dictionary.
        """
        return hash((self.text, self.ticker))

    def __eq__(self, other):
        """
        Check if this Entity instance is equal to the 'other' object.

        In the context of using Entity instances as dictionary keys, 
        this method is used to check if a given key is in the dictionary.
        """
        if isinstance(other, Entity):
            return self.text == other.text and self.ticker == other.ticker
        return False