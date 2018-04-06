from urllib.request import urlopen
import urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import io
import collections


#TODO:
# - dodać odmiany przez przypdaki

# [OK] - posortować od najdłuższych końcówek do najkrutszych ("od szczegółu do ogółu")

# [OK] - sprawdzać pierwsze przymiotniki, później rzeczowniki - jak należy do przymiotników,
# to przerwać sprawdzanie i nie sprawdzać dla rzeczowników

# [Częśćiowo] - sprawdzić czy istnieje hasło w sjp (dopuszczalne w grach / niedopuszczalne w grach)
# i wiki (strona nie istnieje), jeżeli tak i nie należy do zdrobnień, to pominąć
# je i nie dodawać do słownika !!!! Pierwsze sprawdzić czy należy do zdrobnien
# później sprawdzić czy słowo istnieje w sjp

# [OK] - dodac tablice z słowami które określają czy słowo jest zabronione i zastąpić tym tego ififa z orami

# [OK] - dodac do tablicy z słowami zdrobnien dodatkowe słowa, np. Sympatią, młoda, mała

# [OK] - ograniczyc slowa sparwdzane, musza miec przynajmniej 3 litery

# - optymalizacja

# [OK] - wyświetlanie słów w poprawnej kolejności


adjectives_endings = ['eńki', #odmiana -eńki przez przypadki
                      'eńka',
                      'eńkie',
                      'eńkiego',
                      'eńkiej',
                      'eńkiemu',
                      'eńką',
                      'eńkim',
                      'eńcy',
                      'eńkich',
                      'eńcy', #koniec
                      'enieńki', #odmiana -enieńki przez przypadki (CHECK)
                      'enieńką',
                      'enieńka',
                      'enieńkiemu',
                      'enieńkim', #koniec
                      'uni', 'usi',
                      'utki', #odmiana -utki przez przypadki
                      'utka',
                      'utkie',
                      'utkiego',
                      'utkiej',
                      'utkiemu',
                      'utką',
                      'utkim',
                      'utcy',
                      'utkich',
                      'utkimi', #koniec
                      'uteczki', 'utechny', 'uty', 'utenieczki', 'ućki',
                      'uczki', #odmiana -uczki przez przypadki
                      'uczka',
                      'uczkie',
                      'uczkiego',
                      'uczkiej',
                      'uczkiemu',
                      'uczką',
                      'uczkim',
                      'uczcy',
                      'uczkich', #koniec
                      'uśki', #odmiana -uśki przez przypadki
                      'uśka',
                      'uśkie',
                      'uśkiego',
                      'uśkiej',
                      'uśkiemu',
                      'uśką',
                      'uśkim',
                      'uścy',
                      'uśkich',
                      'uśkimi', #koniec
                      'uchny']
nouns_endings = ['ek', #odmiana -ek przez przypadki
                'kowi',
                'kiem',
                'ku',
                'ki',
                'ków',
                'kom',
                'kami',
                'kach', #koniec
                'eczek', #kumulacja -ek ; odmiana -eczek przez przypadki
                'eczka',
                'eczkowi',
                'eczkiem',
                'eczku',
                'eczki',
                'eczków',
                'eczkom',
                'eczkami',
                'eczkach', #koniec
                'ka', #odmiana -ka przez przypadki
                'ce',
                'kę',
                'ką', #koniec
                'eczka', #kumulacja -ka ; odmiana -eczka przez przypadki
                'eczki',
                'eczce',
                'eczkę',
                'eczką',
                'eczko',
                'eczkom',
                'eczkami',
                'eczkach', #koniec
                'ko', #odmiana -ko przez przypadki (juz jest w innych) #koniec
                'eczko', #kumulacja -ko ; odmiana -eczko przez przypadki (jest juz w innych) #koniec
                'ik', #odmiana -ik przez przypadki
                'ika',
                'ikowi',
                'ikiem',
                'iku',
                'iki',
                'icy',
                'ikowie',
                'ików',
                'ikom',
                'ikami',
                'ikach', #koniec
                'yk', #odmiana -yk przez przypadki
                'yka',
                'ykowi',
                'ykiem',
                'yku',
                'yki',
                'yków',
                'ykom',
                'ykami',
                'ykach', #koniec
                'czyk', #odmiana -czyk przez przypadki
                'czyka',
                'czykowi',
                'czyk',
                'czykiem',
                'czyku',
                'czyki',
                'czyków',
                'czykom',
                'czykami',
                'czykach', #koniec
                'iczek', #dalsza odmiana -ik + -ek
                'yczek', #dalsza odmiana -yk + -ek
                'ak',
                'aczek', #dalsza odmiana -ak + -ek
                'aczyk', #dalsza odmiana -ak + -ik
                'iszek',
                'aszek',
                'uszek',
                'ątko',
                'ąteczko',
                'eńko', 'ułka', 'yczka', 'ina', 'uchna',
                'uś', 'usia',
                'iś', 'yś',
                'unia', 'unio']

minWordLen = 3

sjpDimunitivesList = ["zdrobnienie", "pieszczotliwie", "dziecko", "sympatią", "młoda", "mała"]
wikiDimunitivesList = ["zdrobn.", "pieszczotliwie", "dziecko", "sympatią", "młoda", "mała"]

def findDiminutives(text):
    adjectives_endings.sort(key=len, reverse=True)
    nouns_endings.sort(key=len, reverse=True)

    diminutives = collections.OrderedDict()

    for word in text.split():
        word = word.strip(" \".,?!")
        isAdjective = False
        if(len(word) >= minWordLen):
            for ending in adjectives_endings:
                if word.endswith(ending):
                    isAdjective = True
                    diminutive = {}
                    diminutive["word"] = word
                    diminutive["type"] = "przymiotnik"
                    diminutive["ending"] = ending
                    print(word, "- przymiotnik, końcówka:", ending)
                    diminutives[word] = diminutive
                    break

            if not isAdjective:
                for ending in nouns_endings:
                    if word.endswith(ending):
                        diminutive = {}
                        diminutive["word"] = word
                        diminutive["type"] = "rzeczownik"
                        diminutive["ending"] = ending
                        print(word, "- rzeczownik, końcówka:", ending)

                        sjp = searchInSjp(word, diminutive)

                        if sjp == "Nie jest zdrobnieniem":
                            continue

                        if sjp == "Nie występuje w słowniku":
                            searchInWiki(word, diminutive)

                        diminutives[word] = diminutive
                        break
    return diminutives

def getOnlyDiminutives(diminutives):
    d = []
    for k,diminutive in diminutives.items():
        d.append(diminutive["word"])
    return d

def getStats(diminutives):
    n = 0
    a = 0
    for k,diminutive in diminutives.items():
        if diminutive.get("type") == "rzeczownik":
            n += 1
        else:
            a += 1
    stats = {}
    stats["nouns"] = n
    stats["adjectives"] = a
    return stats

def searchInSjp(word, diminutive):
    quote_page = "https://sjp.pl/" + quote(word)
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')

    if not isSjpWord(soup):
        print("Nie występuje w słowniku")
        return "Nie występuje w słowniku"

    definitions = soup.findAll('p', style="margin: .5em 0; font: medium/1.4 sans-serif; max-width: 32em; ")

    for definition in definitions:
        for dim in sjpDimunitivesList:
            if dim in definition.text:
                diminutive["explenation"] = definition.text
                diminutive["sjp"] = quote_page
                return "Jest zdrobnieniem"

    return "Nie jest zdrobnieniem"

def searchInWiki(word, diminutive):
    quote_page = "https://pl.wiktionary.org/wiki/" + quote(word)
    try:
        page = urlopen(quote_page)
        soup = BeautifulSoup(page, 'html.parser')
        definitions = soup.findAll('dd')
        for definition in definitions:
            for dim in wikiDimunitivesList:
                if dim in definition.text:
                    diminutive["explenation"] = definition.text
                    diminutive["wiki"] = quote_page
                    print(definition.text)
    except:
        pass

def isSjpWord(soup):
    content = soup.findAll('p')
    for c in content:
        if "nie występuje w słowniku" in c.text:
            return False
    return True
