from bs4 import BeautifulSoup
import requests
import html2text

inp = input("Hvilket ord vil du søke opp? ")

# Definerer de cookiene jeg trenger:



url = "https://www.wordreference.com/fren/" + inp
result = requests.get(url)
content = result.content
soup = BeautifulSoup(content, features="lxml")

samples = soup.find(id="centercolumn")
sample = samples.get_text()

print(html2text.html2text(sample))

# s = requests.Session()
# response = s.post(url, cookies=cookies, headers=headers, params=params)

# string = response.text
# html_string = string
# string = html2text.html2text(string)

# print(string)
