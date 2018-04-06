from urllib.request import urlopen
import urllib
from urllib.parse   import quote
from bs4 import BeautifulSoup
import io

#TODO:
#-dodać odmiany przez przypdaki
#-posortować od najdłuższych końcówek do najkrutszych ("od szczegółu do ogółu")
#-sprawdzać pierwsze przymiotniki, później rzeczowniki - jak należy do przymiotników, to przerwać sprawdzanie i nie sprawdzać dla rzeczowników
#-sprawdzić czy istnieje hasło w sjp (dopuszczalne w grach / niedopuszczalne w grach) i wiki (strona nie istnieje), jeżeli tak i nie należy do zdrobnień, to pominąć je i nie dodawać do słownika !!!! Pierwsze sprawdzić czy należy do zdrobnien później sprawdzić czy słowo istnieje w sjp
#-dodac tablice z słowami które określają czy słowo jest zabronione i zastąpić tym tego ififa z orami 
#-dodac do tablicy z słowami zdrobnien dodatkowe słowa, np. Sympatią, młoda, mała 
#-ograniczyc slowa sparwdzane, musza miec przynajmniej 3 litery
#-optymalizacja

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

nouns_ending = ['ek', #odmiana -ek przez przypadki
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
