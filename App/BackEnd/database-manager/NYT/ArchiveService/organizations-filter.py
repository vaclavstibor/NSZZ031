import json

def main():
    for i in range (1,13):
        SOURCE = f"/Users/stiborv/Documents/ZS2324/NPRG045/App/BackEnd/Database/data/archive/2022/business/2022-{i}.json"
        TARGET = f"/Users/stiborv/Documents/ZS2324/NPRG045/App/BackEnd/Database/data/archive/2022/business/filtered/2022-{i}.json"
        source_data = FileManager.load(SOURCE)
        filtered_data = Filter(source_data).organizations()
        FileManager.save(TARGET, filtered_data)

class FileManager:

    @staticmethod
    def load(file: str):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                print(f"[INFO] File {file} has been loaded.")
                return data
        except Exception as e:
            print(e)

    @staticmethod
    def save(file: str, data):
        try:
            with open(file, "w", encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
                print(f"[INFO] Data has been saved into file {file}.")
        except:
            raise Exception(f"[ERROR] in FileManager.save()")
            
class Filter:

    def __init__(self, data):
        self.data = data

    def organizations(self):
        try:
            # Keep only articles with keyword "organizations"
            self.data = [article for article in self.data if any(keyword["name"] == "organizations" for keyword in article["keywords"])]
            print(f"[INFO] Data filtered by organizations.")
            return self.data
        except:
            raise Exception(f"[ERROR] in Filter.organizations()")

if __name__ == "__main__":
    main()