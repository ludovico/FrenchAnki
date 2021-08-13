from bs4 import BeautifulSoup
import requests

url = 'https://fr.wiktionary.org/wiki/attraper'


res = requests.get(url).content

soup = BeautifulSoup(res,'html.parser')

data = soup.find_all('a')


for link in data:
    song_link = link['href']
    songs = link.text

    if '.mp3' in song_link:
        print(song_link)
        with open(songs,'wb') as f:
            print('#------------------ ',songs,' downloading----------#')
            res = requests.get(song_link)
            f.write(res.content)

print('\n Completed.....!')
print('\n Completed.....!')
