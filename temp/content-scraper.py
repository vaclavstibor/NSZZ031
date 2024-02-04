# Add to archive business data body content 

from newspaper import Article
import json

class Scraper:

    def __init__(self, file: str):
        self.file = file

    def run(self):
        try:
            with open(self.file, "r+") as f:
                data = json.load(f)
                for article in data:
                    url = article["web_url"]
                    print(url)
                    try:
                        content = Article(url)
                        content.download()
                        content.parse()
                        content.nlp()
                        print("------")
                        print("TEXT")
                        print(content.text)
                        print("------")
                        print("SUMMARY")
                        
                        print(content.summary)
                        print("------")
                    except Exception as e:
                        print(e)                
        except:
            raise Exception(f"[ERROR] in Scraper.run() while try to modify the file {self.filename}.")

"""
Problem s tím, že NYT vrací pouze začátek článků - pravděpodobně způsoveno tím, že ne mám zaplacené 
členství pro kompletní přístup - jediná cesta jak získat 
"""

if __name__ == "__main__":
    FILEPATH = "/Users/stiborv/Documents/ZS2324/NPRG045/App/BackEnd/Database/data/archive/2022/business/"
    FILENAME = "2022-1.json"
    FILE = FILEPATH + FILENAME
    
    scraper = Scraper(FILE)
    scraper.run()



"""
---
"""

class Utils:

    @staticmethod
    def load_file(file_name: str):
        try:
            with open(file_name, "r") as f:
                data_json = json.load(f)
            return data_json
        except:
            raise Exception(f"[ERROR] in load_file() while loading {file_name}.")
