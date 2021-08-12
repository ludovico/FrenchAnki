from bs4 import BeautifulSoup
import requests
import html2text
import re

inp = input("Hvilket ord vil du søke opp? ")

# Definerer de cookiene jeg trenger:



url = "https://www.wordreference.com/fren/" + inp
result = requests.get(url)
content = result.content
soup = BeautifulSoup(content, features="lxml")

samples = soup.find(id="articleWRD")
sample = samples.get_text()

# print(html2text.html2text(sample))

# This is our string:
string = html2text.html2text(sample)

# String cleaning:
# Clear linebreaks
while string.find("\n") != -1:
    string = string.replace("\n", " ")
# Managing quotation marks:
while string.find('"') != -1:
    string = string.replace('"', "DOUBLE2")
while string.find("'") != -1:
    string = string.replace("'", "SINGLE1")

phrases_to_remove = []
phrases_to_remove.append("traductionsFrançaisAnglais")
phrases_to_remove.append("verbe transitif: verbe qui sSINGLE1utilise avec un complément dSINGLE1objet direct (COD). Ex : DOUBLE2JSINGLE1écris une lettreDOUBLE2. DOUBLE2Elle a retrouvé son chatDOUBLE2.")
phrases_to_remove.append("transitive verb: Verb taking a direct object--for example, DOUBLE2Say something.DOUBLE2 DOUBLE2She found the cat.DOUBLE2")
phrases_to_remove.append("verbal expression: Phrase with special meaning functioning as verb--for example, DOUBLE2put their heads together,DOUBLE2 DOUBLE2come to an end.DOUBLE2")
phrases_to_remove.append("verbe pronominal: verbe qui sSINGLE1utilise avec le pronom réfléchi DOUBLE2seDOUBLE2, qui sSINGLE1accorde avec le sujet. Ex : se regarder : DOUBLE2Je me regarde dans le miroir. Tu te regardes dans le miroir.DOUBLE2. Les verbes pronominaux se conjuguent toujours avec lSINGLE1auxiliaire DOUBLE2êtreDOUBLE2. Ex : DOUBLE2Elle a lavé la voitureDOUBLE2 mais DOUBLE2Elle sSINGLE1est lavée.DOUBLE2")
phrases_to_remove.append(": Verb with adverb(s) or preposition(s), having special meaning, divisible--for example, DOUBLE2call offDOUBLE2 [=cancel], DOUBLE2call the game off,DOUBLE2 DOUBLE2call off the game.DOUBLE2")

for i in phrases_to_remove:
    while string.find(i) != -1:
        string = string.replace(i, "")

# Managing quotation marks again:
while string.find("DOUBLE2") != -1:
    string = string.replace("DOUBLE2", '"')
while string.find("SINGLE1") != -1:
    string = string.replace("SINGLE1", "'")

# Finding definitions:
next = "y"
while next == "y":
    # French Definition
    definition_start = string.find("(")
    definition_end = string.find(")", definition_start)
    definition = string[(definition_start +1):(definition_end)]
    print("French Definition: " + definition + "\n")
    # English Definition:
    eng_def_end = string.find("⇒", definition_end)
    eng_def_start = definition_end +1
    eng_def = string[eng_def_start:eng_def_end]
    print("English Definition: " + eng_def + "\n")
    # French Sentence:
    string = string[eng_def_end:(len(string))] # Kutter strengen for å gjøre det enklere med regex
    capital = re.search('[A-ZÀ-Ÿ]', string).span()
    sentence_start = capital[0]
    symbol = re.search('[.!?]', string).span()
    sentence_end = symbol[0] +1
    sentence = string[sentence_start:sentence_end]
    print("French Sentence: " + sentence + "\n")
    #English sentence
    string = string[(symbol[0]+1):len(string)]
    symbol = re.search('[.!?]', string).span()
    english_sentence_end = symbol[0]
    english_sentence = string[1:(english_sentence_end+1)]
    print("English Sentence: " + english_sentence + "\n")
    # French Sentence: Remove keyword:
    keyword = inp[0:(len(inp)-2)]
    if sentence.find(keyword) != 1:
        remove_word_start = sentence.find(keyword)
        remove_word_end = sentence.find(" ", remove_word_start)
        remove_word = sentence[remove_word_start:remove_word_end]
        sentence_keyword_removed = sentence.replace(remove_word, "___")
        print("Sentence with keyword removed: " +  sentence_keyword_removed + "\n")
    else: print("Keyword not found")
    string = string[(string.find(".", sentence_end+1)+1):len(string)]
    next = input("Do you want to scroll to the next definition? Press y to scroll or any key to continue")
