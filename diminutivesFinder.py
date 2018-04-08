from urllib.request import urlopen
import urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import io
import collections
import re


#TODO:
# [ ] - dodać wszystkie końcówki i ich odmiany przez przypdaki

# [OK] - posortować od najdłuższych końcówek do najkrutszych ("od szczegółu do ogółu")

# [OK] - sprawdzać pierwsze przymiotniki, później rzeczowniki - jak należy do przymiotników,
# to przerwać sprawdzanie i nie sprawdzać dla rzeczowników

# [OK] - sprawdzić czy istnieje hasło w sjp (dopuszczalne w grach / niedopuszczalne w grach)
# i wiki (strona nie istnieje), jeżeli tak i nie należy do zdrobnień, to pominąć
# je i nie dodawać do słownika !!!! Pierwsze sprawdzić czy należy do zdrobnien
# później sprawdzić czy słowo istnieje w sjp

# [OK] - dodac tablice z słowami które określają czy słowo jest zabronione i zastąpić tym tego ififa z orami

# [OK] - dodac do tablicy z słowami zdrobnien dodatkowe słowa, np. Sympatią, młoda, mała

# [OK] - ograniczyc slowa sparwdzane, musza miec przynajmniej 3 litery

# [ ] - optymalizacja (zadanie na przyszłość - opcjonalne)

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
                      'uchny',
                      'uty',
                      'ylki']
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
                'iczek', #dalsza odmiana -ik + -ek ; odmiana -iczek przez przypadki
                'iczka',
                'iczkowi',
                'iczkiem',
                'iczku',
                'iczki',
                'iczków',
                'iczkom',
                'iczkami',
                'iczkach', #koniec
                'yczek', #dalsza odmiana -yk + -ek ; odmiana -yczek przez przypadki
                'yczka',
                'yczkowi',
                'yczkiem',
                'yczku',
                'yczki',
                'yczków',
                'yczkom',
                'yczkami',
                'yczkach', #koniec
                'ak', #odmiana -ak przez przypadki
                'aka',
                'akowi',
                'akiem',
                'aku',
                'aki',
                'aków',
                'akom',
                'akami',
                'akach', #koniec
                'aczek', #dalsza odmiana -ak + -ek ; odmiana -aczek przez przypadki
                'aczka',
                'aczkowi',
                'aczkiem',
                'aczku',
                'aczki',
                'aczków',
                'aczkom',
                'aczkami',
                'aczkach', #koniec
                'aczyk', #dalsza odmiana -ak + -ik ; odmiana -aczyk przez przypadki (jest już w innych) #koniec
                'iszek', #odmiana -iszek przez przypadki
                'iszka',
                'iszkowi',
                'iszkiem',
                'iszku',
                'iszkowie',
                'iszków',
                'iszkom',
                'iszkami',
                'iszkach',
                'iszkowie', #koniec
                'aszek', #odmiana -aszek przez przypadki
                'aszka',
                'aszkiem',
                'aszkowi',
                'aszku',
                'aszków',
                'aszkach',
                'aszkami',
                'aszkom',
                'aszkowie',
                'aszki', #koniec
                'uszek', #odmiana -uszek przez przypadki
                'uszka',
                'uszkowi',
                'uszkiem',
                'uszku',
                'uszki',
                'uszków',
                'uszkom',
                'uszkami',
                'uszkach', #koniec
                'ątko', #odmiana -ątko przez przypadki
                'ątka',
                'ątku',
                'ątko',
                'ątkiem',
                'ątek',
                'ątkom',
                'ątkami',
                'ątkach', #koniec
                'ąteczko', #odmiana -ąteczko przez przypadki
                'ąteczka',
                'ąteczku',
                'ąteczkiem',
                'ąteczek',
                'ąteczkom',
                'ąteczkami',
                'ąteczkach', #koniec
                'eńko', #odmiana -eńko przez przypadki
                'eńka',
                'eńku',
                'eńko',
                'eńkiem',
                'eniek',
                'eńkom',
                'eńkami',
                'eńkach', #koniec
                'ułka', #odmiana -ułka przez przypadki
                'ułki',
                'ułce',
                'ułkę',
                'ułką',
                'ułko',
                'ułek',
                'ułkom',
                'ułkami',
                'ułkach', #koniec
                'yczka', #odmiana -yczka przez przypadki
                'yczki',
                'yczce',
                'yczkę',
                'yczką',
                'yczko',
                'yczek',
                'yczkom',
                'yczkami',
                'yczkach', #koniec
                'ina', #odmiana -ina przez przypadki
                'iny',
                'inie',
                'inę',
                'iną',
                'ino',
                'ini',
                'inów',
                'inom',
                'inami',
                'inach', #koniec
                'uchna', #odmiana -uchna przez przypadki
                'uchny',
                'uchnie',
                'uchnę',
                'uchną',
                'uchno',
                'uchny',
                'uchen',
                'uchnom',
                'uchnami',
                'uchnach', #koniec
                'uś', #odmiana -uś przez przypadki
                'usiowi',
                'usiem',
                'usiu',
                'usiach',
                'usiami',
                'usiom',
                'usiów',
                'usiowie',
                'usie', #koniec
                'usia', #omiana -usia przez przypadki
                'usi',
                'usię',
                'usią',
                'usiom', #koniec
                'iś', #odmiana -iś przez przypadki
                'isia',
                'isiowi',
                'isiem',
                'isiu',
                'isie',
                'isiów',
                'isiom',
                'isiami',
                'isiach', #koniec
                'yś', #odmiana -yś przez przypadki
                'ysia',
                'ysiowi',
                'ysiem',
                'ysiu',
                'ysiach',
                'ysiami',
                'ysiom',
                'ysiów',
                'ysiowie',
                'ysie',
                'ysi',
                'ysią',
                'ysię', #koniec
                'unia', #odmiana -unia przez przypadki
                'uni',
                'unię',
                'unią',
                'uniu',
                'unie',
                'uń',
                'uniom',
                'unie',
                'uniami',
                'uniach', #koniec
                'unio', #odmiana -unio przez przypadki
                'unia',
                'uniowi',
                'uniem',
                'uniowie',
                'uniów', #koniec
                'o', #odmiana -o przez przypadki
                'owi',
                'em',
                'u',
                'ach',
                'ami',
                'om',
                'ów',
                'owie',
                'e', #koniec
                'cio', #odmiana -cio przez przypadki
                'cia',
                'ciowi',
                'ciem',
                'ciu',
                'cie',
                'ciów',
                'ciom',
                'ciami',
                'ciach', #koniec
                'aś', #odmiana -aś przez przypadki
                'asia',
                'asiowi',
                'asiem',
                'asiu',
                'asie',
                'asiowie',
                'asiów',
                'asiom',
                'asiach', #koniec
                'a', #odmiana -a przez przypadki
                'ą',
                'ę' #koniec
                ]

minWordLen = 3

sjpDimunitivesList = ["zdrobnienie", "zdrobn.", "zdrobniale", "pieszczotliwie", "dziecko", "sympatią", "młoda", "mała", "mały", "małe", "niewielkie", "niewiele", "drobnej"]
#wikiDimunitivesList = ["zdrobn.", "pieszczotliwie", "dziecko", "sympatią", "młoda", "mała"]

def findDiminutives(text):
    adjectives_endings.sort(key=len, reverse=True)
    nouns_endings.sort(key=len, reverse=True)

    diminutives = collections.OrderedDict()

    n = 0
    a = 0

    for word in text.split():
        word = word.strip(" \"„”.,?!():;'")
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
                    a += 1
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
                        n += 1
                        break
    stats = {}
    stats["nouns"] = n
    stats["adjectives"] = a
    return {"diminutives": diminutives, "stats": stats}

def getOnlyDiminutives(diminutives):
    d = []
    for k,diminutive in diminutives.items():
        d.append(diminutive["word"])
    return d

def searchInSjp(word, diminutive):
    quote_page = "https://sjp.pl/" + quote(word)
    page = urlopen(quote_page)
    soup = BeautifulSoup(page, 'html.parser')

    if not isSjpWord(soup):
        print("Nie występuje w słowniku")
        return "Nie występuje w słowniku"

    definitions = soup.findAll('p', style="margin: .5em 0; font: medium/1.4 sans-serif; max-width: 32em; ")

    #if not definitions:
    #    return "Jest zdrobnieniem"
    #else:
    for definition in definitions:
        for dim in sjpDimunitivesList:
            if re.findall('\\b' + dim + '\\b', definition.text, flags=re.IGNORECASE): #dim in definition.text:
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
            for dim in sjpDimunitivesList:
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
