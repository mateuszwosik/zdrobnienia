from urllib.request import urlopen
import urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import io

adjectives_endings = ['eńki', 'enieńki', 'uni', 'usi', 'utki', 'uteczki', 'utechny', 'uty', 'utenieczki', 'ućki', 'uczki', 'uśki', 'uchny']
nouns_ending = ['ek', 'ka', 'ko', 'ik', 'yk', 'czyk', 'ak', 'eńko', 'ułka', 'yczka', 'ina', 'uchna', 'uś', 'usia', 'iś', 'yś', 'unia', 'unio']

def findDiminutives(text):
    diminutives = {}
    for word in text.split():
        word = word.strip(" \".,?!")
        for ending in nouns_ending:
            if word.endswith(ending):
                diminutive = {}
                diminutive["word"] = word
                diminutive["type"] = "rzeczownik"
                diminutive["ending"] = ending

                quote_page = "https://sjp.pl/" + quote(word)

                print()
                print(quote_page)
                page = urlopen(quote_page)
                soup = BeautifulSoup(page, 'html.parser')
                name_box = soup.findAll('p', style="margin: .5em 0; font: medium/1.4 sans-serif; max-width: 32em; ")
                for n in name_box:
                    if "zdrobnienie" in n.text or "pieszczotliwie" in n.text or "dziecko" in n.text:
                        diminutive["explenation"] = n.text
                        diminutive["sjp"] = quote_page
                        print(n.text)

                if not "sjp" in diminutive:
                    quote_page = "https://pl.wiktionary.org/wiki/" + quote(word)
                    print()
                    print(quote_page)
                    try:
                        page = urlopen(quote_page)
                        soup = BeautifulSoup(page, 'html.parser')
                        name_box = soup.findAll('dd')
                        for n in name_box:
                            if "zdrobn." in n.text or "pieszczotliwie" in n.text or "dziecko" in n.text:
                                diminutive["explenation"] = n.text
                                diminutive["wiki"] = quote_page

                    except:
                        pass
                diminutives[word] = diminutive
                break

        for ending in adjectives_endings:
            if word.endswith(ending):
                diminutive = {}
                diminutive["word"] = word
                diminutive["type"] = "przymiotnik"
                diminutive["ending"] = ending
                print(word, "- przymiotnik, końcówka:", ending)
                diminutives[word] = diminutive
                break
    return diminutives
