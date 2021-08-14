from bs4 import BeautifulSoup
import requests
import html2text
import re
from jmd_imagescraper.core import * # dont't worry, it's designed to work with import *
from pathlib import Path
from PIL import Image
import glob
import psutil
import os

inp = input("Hvilket ord vil du søke opp? ")
url = "https://www.wordreference.com/fren/" + inp
result = requests.get(url)
content = result.content
soup = BeautifulSoup(content, features="lxml")
samples = soup.find(id="articleWRD")
sample = samples.get_text()
# print(html2text.html2text(sample))
# This is our string:
string = html2text.html2text(sample)
originalstring = string
# String cleaning:
# Clear linebreaks
while string.find("\n") != -1:
    string = string.replace("\n", " ")
print(string+"\n\n")

phrases_to_remove = []
phrases_to_remove.append("traductionsFrançaisAnglais")
phrases_to_remove.append("verbe transitif: verbe qui sSINGLE1utilise avec un complément dSINGLE1objet direct (COD). Ex : DOUBLE2JSINGLE1écris une lettreDOUBLE2. DOUBLE2Elle a retrouvé son chatDOUBLE2.")
phrases_to_remove.append("vtrtransitive verb: Verb taking a direct object--for example, DOUBLE2Say something.DOUBLE2 DOUBLE2She found the cat.DOUBLE2")
phrases_to_remove.append("verbal expression: Phrase with special meaning functioning as verb--for example, DOUBLE2put their heads together,DOUBLE2 DOUBLE2come to an end.DOUBLE2")
phrases_to_remove.append("verbe pronominal: verbe qui sSINGLE1utilise avec le pronom réfléchi DOUBLE2seDOUBLE2, qui sSINGLE1accorde avec le sujet. Ex : se regarder : DOUBLE2Je me regarde dans le miroir. Tu te regardes dans le miroir.DOUBLE2. Les verbes pronominaux se conjuguent toujours avec lSINGLE1auxiliaire DOUBLE2êtreDOUBLE2. Ex : DOUBLE2Elle a lavé la voitureDOUBLE2 mais DOUBLE2Elle sSINGLE1est lavée.DOUBLE2")
phrases_to_remove.append(": Verb with adverb(s) or preposition(s), having special meaning, divisible--for example, DOUBLE2call offDOUBLE2 [=cancel], DOUBLE2call the game off,DOUBLE2 DOUBLE2call off the game.DOUBLE2")
phrases_to_remove.append("nmnom masculin: sSINGLE1utilise avec les articles DOUBLE2leDOUBLE2, DOUBLE2lSINGLE1DOUBLE2 (devant une voyelle ou un h muet), DOUBLE2unDOUBLE2. Ex : garçon - nm > On dira DOUBLE2le garçonDOUBLE2 ou DOUBLE2un garçonDOUBLE2. ")
phrases_to_remove.append("nnoun: Refers to person, place, thing, quality, etc. ")
phrases_to_remove.append("adjadjectif: modifie un nom. Il est généralement placé après le nom et sSINGLE1accorde avec le nom (ex : un ballon bleu, une balle bleue). En général, seule la forme au masculin singulier est donnée. Pour former le féminin, on ajoute DOUBLE2eDOUBLE2 (ex : petit > petite) et pour former le pluriel, on ajoute DOUBLE2sDOUBLE2 (ex : petit > petits). Pour les formes qui sont DOUBLE2irrégulièresDOUBLE2 au féminin, celles-ci sont données (ex : irrégulier, irrégulière > irrégulier = forme masculine, irrégulière = forme féminine)")
phrases_to_remove.append("adjadjectif: modifie un nom. Il est généralement placé après le nom et sSINGLE1accorde avec le nom (ex : un ballon bleu, une balle bleue). En général, seule la forme au masculin singulier est donnée. Pour former le féminin, on ajoute DOUBLE2eDOUBLE2 (ex : petit > petite) et pour former le pluriel, on ajoute DOUBLE2sDOUBLE2 (ex : petit > petits). Pour les formes qui sont DOUBLE2irrégulièresDOUBLE2 au féminin, celles- ci sont données (ex : irrégulier, irrégulière > irrégulier = forme masculine, irrégulière = forme féminine)")
phrases_to_remove.append("adjadjective: Describes a noun or pronoun--for example, DOUBLE2a tall girl,DOUBLE2 DOUBLE2an interesting book,DOUBLE2 DOUBLE2a big house.DOUBLE2 ")
phrases_to_remove.append("adjadjective: Describes a noun or pronoun-- for example, DOUBLE2a tall girl,DOUBLE2 DOUBLE2an interesting book,DOUBLE2 DOUBLE2a big house.DOUBLE2 ")
phrases_to_remove.append("nfnom féminin: sSINGLE1utilise avec les articles DOUBLE2laDOUBLE2, DOUBLE2lSINGLE1DOUBLE2 (devant une voyelle ou un h muet), DOUBLE2uneDOUBLE2. Ex : fille - nf > On dira DOUBLE2la filleDOUBLE2 ou DOUBLE2une filleDOUBLE2. Avec un nom féminin, lSINGLE1adjectif sSINGLE1accorde. En général, on ajoute un DOUBLE2eDOUBLE2 à lSINGLE1adjectif. Par exemple, on dira DOUBLE2une petite filleDOUBLE2. ")
phrases_to_remove.append("nfnom féminin: sSINGLE1utilise avec les articles DOUBLE2laDOUBLE2, DOUBLE2lSINGLE1DOUBLE2 (devant une voyelle ou un h muet), DOUBLE2uneDOUBLE2. Ex : fille - nf > On dira DOUBLE2la filleDOUBLE2 ou DOUBLE2une filleDOUBLE2. Avec un nom féminin, lSINGLE1adjectif sSINGLE1accorde. En général, on ajoute un DOUBLE2eDOUBLE2 à lSINGLE1adjectif. Par exemple, on dira DOUBLE2une petite filleDOUBLE2. ")
phrases_to_remove.append("conjconjunction: Connects words, clauses, and sentences--for example, DOUBLE2and,DOUBLE2 DOUBLE2but,DOUBLE2 DOUBLE2because,DOUBLE2 DOUBLE2in order that.DOUBLE2 in the manner of, following the example of ")
phrases_to_remove.append("exprexpression: Prepositional phrase, adverbial phrase, or other phrase or expression--for example, DOUBLE2behind the times,DOUBLE2 DOUBLE2on your own.DOUBLE2 ")
phrases_to_remove.append("advadverbe: modifie un adjectif ou un verbe. Est toujours invariable ! Ex : DOUBLE2Elle est très grande.DOUBLE2 DOUBLE2Je marche lentement.DOUBLE2 ")
phrases_to_remove.append("advadverb: Describes a verb, adjective, adverb, or clause--for example, DOUBLE2come quickly,DOUBLE2 DOUBLE2very rare,DOUBLE2 DOUBLE2happening now,DOUBLE2 DOUBLE2fall down.DOUBLE2 ")

for i in phrases_to_remove:
    while string.find(i) != -1:
        string = string.replace(i, "ENDPART")
    # Managing quotation marks again:
while string.find("DOUBLE2") != -1:
    string = string.replace("DOUBLE2", '"')
while string.find("SINGLE1") != -1:
    string = string.replace("SINGLE1", "'")

    # Other things to remove:
phrases_to_remove = []
phrases_to_remove.append("ⓘCette phrase n'est pas une traduction de la phrase originale.")
phrases_to_remove.append("Un oubli important ? Signalez une erreur ou suggérez une amélioration. Traductions supplémentairesFrançaisAnglais")


# for i in phrases_to_remove:
#     while string.find(i) != -1:
#         string = string.replace(i, "")
print(string)

print("\n\n\n")
example_string = "hei dette er en liten Test av regex"
result = re.search('([A-Z]\w+)', example_string)
print(result)
