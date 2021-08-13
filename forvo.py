from bs4 import BeautifulSoup
import requests
import html2text
import re
from urllib.request import Request, urlopen

url = "https://fr.forvo.com/word/attraper/#fr"
req = Request(url , headers={'User-Agent': 'Mozilla/5.0'})
webpage = urlopen(req).read()
soup = BeautifulSoup(webpage, "html.parser")
print(soup.prettify())


# Create the session object
# s = requests.Session()
#
# # Example request
# response = s.get("https://fr.forvo.com/word/attraper/#fr")
# print(response)

# Finner Forvo-fil:
# url = 'https://fr.forvo.com/word/attraper/#fr'
# result = requests.get(url)
# content = result.content
# soup = BeautifulSoup(content, features="lxml")
# print(soup.prettify())
