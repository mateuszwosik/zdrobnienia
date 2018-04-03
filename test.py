from urllib.request import urlopen
import urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup

adjectives_endings = ['eńki', 'enieńki', 'uni', 'usi', 'utki', 'uteczki', 'utechny', 'uty', 'utenieczki', 'ućki', 'uczki', 'uśki', 'uchny']
nouns_ending = ['ek', 'ka', 'ko', 'ik', 'yk', 'czyk', 'ak', 'eńko', 'ułka', 'yczka', 'ina', 'uchna', 'uś', 'usia', 'iś', 'yś', 'unia', 'unio']

with open('examples/dziewczynka.txt','r') as f:
    for line in f:
        for word in line.split():
            word = word.strip(" \".,?!")
            for ending in nouns_ending:
                if word.endswith(ending):
                    quote_page = "https://sjp.pl/" + quote(word)

                    print()
                    print(quote_page)
                    page = urlopen(quote_page)
                    soup = BeautifulSoup(page, 'html.parser')
                    name_box = soup.findAll('p', style="margin: .5em 0; font: medium/1.4 sans-serif; max-width: 32em; ")
                    for n in name_box:
                        if "zdrobnienie" in n.text or "pieszczotliwie" in n.text:
                            print(n.text)
                            
                    print(word, "- rzeczownik, końcówka:", ending)
                    break

            # for ending in adjectives_endings:
            #     if word.endswith(ending):
            #         print(word, "- przymiotnik, końcówka:", ending)
            #         break
