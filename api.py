from newsdataapi import NewsDataApiClient
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.getenv("API_KEY")

api = NewsDataApiClient(apikey=api_key)

#response = api.news_api(q='pizza')
response2= api.latest_api(country='no')
#print(response)
print(response2)