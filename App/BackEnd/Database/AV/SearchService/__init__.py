import requests
import json

TICKER = 'AMZN'
LIMIT = 1000 # max 1000
API_KEY = '' #'0JV1305HSHHJ3MNH'


url = f'https://www.alphavantage.co/query?function=NEWS_SENTIMENT&tickers={TICKER}&limit={LIMIT}&apikey={API_KEY}'

class FileManager:

    @staticmethod
    def save(ticker: str, data):
        file_name = f'{ticker}.json'
        try:
            with open(f'/Users/stiborv/Documents/ZS2324/NPRG045/App/BackEnd/AV/data/search/{file_name}', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"[INFO] Data has been saved into file {file_name}.")
        except:
            raise Exception(f"[ERROR] in FileManager.save()")

if __name__ == '__main__':

    try:
        r = requests.get(url)
        data = r.json()
        print(data)
        FileManager.save(TICKER, data)
    except Exception as e:
        print(e)