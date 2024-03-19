import requests
import json

API_KEY = "cb585bc0-76e2-49fe-a635-277e94cbeba8"

api = f'https://content.guardianapis.com/sections?api-key={API_KEY}'

class FileManager:

    @staticmethod
    def save(file: str, data):
        try:
            with open(file, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"[INFO] Data has been saved into file {file}.")
        except:
            raise Exception(f"[ERROR] in FileManager.save()")

try:    
    response = requests.get(api)
    data = response.json()
    sections = data['response']['results']
    FileManager.save("sections.json", sections)
except requests.exceptions.HTTPError as errh:
    print ("Http Error:",errh)
except requests.exceptions.ConnectionError as errc:
    print ("Error Connecting:",errc)
except requests.exceptions.Timeout as errt:
    print ("Timeout Error:",errt)
except requests.exceptions.RequestException as e: 
    raise SystemExit(e)  

"""
- business
- money
- technology
"""
