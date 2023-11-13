import argparse
import json
import newspaper
import os
import requests
import datetime

class NewsCollector:
    
    def __init__(self):
        print("NewsCollector")

    def execute(self):
        try:
            print("execute")
        except Exception as err:
            print(f'ERROR: Unexpected {err=}, {type(err)=}')
            raise
            
class Scraper:

    def __init__(self,sources):
        self.sources = sources
        self.count = 0

    @classmethod
    def print_scrape_status(self):
        self.count += 1
        print(f"Scraped {self.count} articles",end="\r")

    @classmethod
    def execute(self, data):
        for article in data['results']:            
            url = article['url']
            try:
                content = newspaper.Article(url)
                content.download()
                content.parse()
                content.nlp()
                try:
                    article['body'] = content.text
                    article['summary'] = content.summary
                    self.print_scrape_status()
                except Exception as err:
                    print(f'ERROR: Unexpected {err=}, {type(err)=}')
                    #raise
            except Exception as err:
                print(f'ERROR: Unexpected {err=}, {type(err)=}')
                #raise
        return data

class DataManager:

    def __init__(self, sources_file: str):
        self.load_sources(sources_file)
        self.api = self.get_api()
        self.data = self.call_api()

    @classmethod
    def load_sources(cls, file: str):
        try:
            with open(file) as data:
                cls.sources = json.load(data)
            print(f"INFO: Sources successfully loaded from file {file}.")
        except Exception as err:
            print(f"ERROR: Unexpected {err=}, {type(err)=}")
            raise

    @classmethod
    def get_api(cls):
        with open('config.json') as f:
            config = json.load(f)
            api_dict = {}
            for source_name, url in cls.sources.items():
                if source_name in config['sources']:
                    api_key = config['sources'][source_name]['api key']
                    api_dict[url['api']] = api_key
                else:
                    print(f"API key not found for source: {source_name}")
            return api_dict

    def call_api(self):
        for url, key in self.api.items():
            try:
                r = requests.get(f'{url}{key}')
                print(f"INFO: Request status code {r.status_code}")
                try:
                    current_time = datetime.datetime.now()
                    content_response = json.loads(r.content)
                    with open(f'./data/all/business-{current_time.day}-{current_time.month}-{current_time.year}.json', 'w', encoding='utf-8') as f:
                        json.dump(content_response, f, ensure_ascii=False, indent=4)
                        print(f"INFO: Response content was successfully written into file {f.name}")
                except Exception as err:
                    print(f"ERROR: Unexpected {err=}, {type(err)=}")
            except Exception as err:
                print(f"ERROR: Unexpected {err=}, {type(err)=}")
                

#class Utils:



if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='News Article Collector')
    parser.add_argument("-s", "--sources", type=str, help='Path of source JSON file with news sources to be scraped.', required=False, default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "sources.json"))
    
    args = parser.parse_args()

    #dm = DataManager(args.sources)

    #collector = NewsCollector(args.sources)
    #collector.run()
    

