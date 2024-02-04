import requests 
   
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
r = requests.get("https://query1.finance.yahoo.com/v1/finance/search?q=aapl", headers=headers)
 
# check status code for response received 
# success code - 200 
print(r) 
  
# print content of request 
print(r.content.news)