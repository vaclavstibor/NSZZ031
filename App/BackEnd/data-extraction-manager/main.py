from typing import List
from src.data_sources.the_guardian import TheGuardian
from src.data_sources.nytimes import NYTimes
from src.data_sources.models.base_source import BaseSource


class Processor:
    """ """

    def __init__(self, source: BaseSource):
        self.source = source

    def process(self, sections: List[str], from_date: str):
        self.source.fetch_data(sections, from_date)
        return True


if __name__ == "__main__":
    the_guardian_processor = Processor(TheGuardian())
    the_guardian_processor.process(["politics"], "2024-01-01")

