import argparse
import json

class NewsCollector:
    def __init__(self,sources='sources.json'):
        self.sources = Utils.load_sources(sources)

class Utils:
    def load_sources(file: str):
        try:
            with open(file) as data:
                sources = json.load(data)
            print(f'INFO: File {file} successfully loaded as source file.')
            return sources
        except Exception as err:
            print(f'ERROR: Unexpected {err=}, {type(err)=}')
            raise
    
    def get_api_key():
        with open('config.json') as f:
            config = json.load(f) 
            api_key = config['api_key']
        return api_key

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='News Article Collector')
    parser.add_argument("-s", "--sources", type=str, help='Path of source JSON file with news sources to be scraped.', required=False, default="./ny-times/sources.json")
    
    args = parser.parse_args()

    collector = NewsCollector(args.sources)
    #collector.run()
    print(collector.sources)