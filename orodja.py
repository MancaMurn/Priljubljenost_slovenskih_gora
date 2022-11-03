import re
import os
import requests
import csv
import json


# Vzorec, ki bo iz prvotne strani s seznamom gorovij in drugih držav zajel samo bolk, s slovenskimi gorovji.
vzorec_slovenska_gorovja = re.compile(
    r'<div class="naslov1"><h1>Gorovja - Slovenija</h1></div>'
    r'.*?'
    r'<div class="naslov2"><h2>Ostale države</h2></div>',
    flags=re.DOTALL
)

# Vzorec, ki bo iz bloka, kjer so samo slovenska gorovja, zajel url naslove strani, 
# ki nam podajo sezname vrhov v določenem gorovju.
vzorec_url_gorovja = re.compile(
    r'<div class="vr\d"><a href="(?P<url_gorovje>.+?)">.+?</a></div>',
    flags=re.DOTALL
)

# Vzorec, ki bo iz strani, kjer je seznam vrhov v nekem gorovju,
# zajel url naslov vrha, ki nas pelje na stran s podatki o tem vrhu.
vzorec_url_vrh = re.compile(
    r'<tr class="vr\d"><td class="vrtd.*?"><a href="(?P<url_vrh>.+?)">.+?</a></td>',
    flags=re.DOTALL
)

# Vzorec, ki pobere podatke o vrhu, na koncu dobimo še blok, 
# iz katerega je potrebno dodatno pobrati podatke o poteh.
vzorec_podatki_gore = re.compile(
    r'</script>.*?'
    r'<div class="naslov1"><div style="float:left;"><h1>(?P<ime>.+?)</h1></div>.*?'
    r'<div class="g2"><b>Država:</b> <a class="moder" href="/gorovja">(?P<drzava>.+?)</a></div>.*?'
    r' <div class="g2"><b>Gorovje:</b> <a class="moder" href=.*?>(?P<gorovje>.+?)</a></div>.*?'
    r'<div class="g2"><b>Višina:</b> (?P<visina>.+?)&nbsp;m</div>.*?'
    r'<div class="g2"><b>Vrsta:</b> (?P<vrsta>.*?)</div>.*?'
    r'<div class="g2"><b>Ogledov:</b> (?P<stevilo_ogledov>.+?)</div>.*?'
    r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost>.+?)%.*?</div>.*?'
    r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<stevilo_poti>.+?)</a></div>.*?'
    r'<div style="padding-top:10px;"><b>Opis gore:</b><br />(?P<opis>.+?)</div>.*?'
    r'<table class="TPoti" id="poti">(?P<blok_poti>.+?)</table>',
    flags=re.DOTALL
)

# Vzorec, ki iz bloka o poteh na nek vrh pobere podatke o posamezni poti. 
vzorec_podatki_pot = re.compile(
    r'<tr class="trG\d"><td class="tdG"><a href=.+?>(?P<ime_poti>.+?)</a></td>.*?'
    r'<td class="tdG"><a href=.+?>(?P<cas_poti>.+?)</a></td>.*?'
    r'<td class="tdG"><a href=.+?>(?P<tezavnost_poti>.+?)</a></td></tr>',
    flags=re.DOTALL
)



#Funkcija, ki preveri obstoj datoteke z danim imenom.
def preveri_obstoj_datoteke(ime_datoteke):
    return os.path.isfile(ime_datoteke)
      

# Funkcija, ki vrne niz z vsebino datoteke z danim imenom.
def vsebina_datoteke(ime_datoteke):
    if preveri_obstoj_datoteke(ime_datoteke) == True:
        with open(ime_datoteke, encoding='utf-8') as datoteka:
            return datoteka.read()
    else:
        print(f'Datoteka z imenom {ime_datoteke} ne obstaja!')


# Funkcija, ki iz dane datoteke pobere samo potreben blok z danim vzorcem in vrne iskan blok, 
# v obliki niza v seznamu.
def poberi_blok(ime_datoteke, vzorec):
    niz = vsebina_datoteke(ime_datoteke)
    blok = vzorec.findall(niz)
    return blok


# Funkcija, ki nam v dani datoteki z danim vzorcem, najde vse pojavitve in jih vrne v seznamu slovarjev, v obliki:
# [{'url_gorovje': '"/gorovje/gorisko_notranjsko_in_sneznisko_hribovje/26"'}, {'url_gorovje': '"/gorovje/julijske_alpe/1"'}]
def najdi_vzorec_v_datoteki(ime_datoteke, vzorec):
    niz = vsebina_datoteke(ime_datoteke)
    seznam = []
    for pojavitev in re.finditer(vzorec, niz):
        ujemanje = pojavitev.groupdict()
        seznam.append(ujemanje)
    return seznam


#Funkcija, ki nam v danem nizu z danim vzocem, najde vse pojavitve in vrne seznam slovarjev.
def najdi_vzorec_v_nizu(niz, vzorec):
    seznam = []
    for pojavitev in re.finditer(vzorec, niz):
        ujemanje = pojavitev.groupdict()
        seznam.append(ujemanje)
    return seznam


#Če še ne obstaja, pripravi prazen imenik za dano datoteko.
def pripravi_imenik(ime_datoteke):
   imenik = os.path.dirname(ime_datoteke)
   if imenik:
        os.makedirs(imenik, exist_ok=True)


# Vsebino strani na danem naslovu shrani v datoteko z danim imenom.
def shrani_spletno_stran(url, ime_datoteke, vsili_prenos=False):
    try:
        print(f'Shranjujem {url} ...', end='')
        if os.path.isfile(ime_datoteke) and not vsili_prenos:
            print('shranjeno že od prej!')
            return
        r = requests.get(url)
    except requests.exceptions.ConnectionError:
        print('stran ne obstaja!')
    else:
        pripravi_imenik(ime_datoteke)
        with open(ime_datoteke, 'w', encoding='utf-8') as datoteka:
            datoteka.write(r.text)
            print('shranjeno!')


def popravi_podatke_vrh(slovar):
    slovar['visina'] = int(slovar['visina'])
    slovar['stevilo_ogledov'] = int(slovar['stevilo_ogledov'].replace('.',''))
    slovar['priljubljenost'] = int(slovar['priljubljenost'])
    slovar['stevilo_poti'] = int(slovar['stevilo_poti'])
    for i in range(len(slovar['blok_poti'])):
        cas = slovar['blok_poti'][i]['cas_poti']
        if 'min' in cas and 'h' in cas:
            cas = cas.replace(' h', '*60')
            cas = cas.replace(' min', '')
            cas = cas.replace(' ', '+')
        else:
            cas = cas.replace(' h', '*60')
            cas = cas.replace(' min', '')
        slovar['blok_poti'][i]['cas_poti'] = eval(cas)
    
     

#Iz seznama slovarjev ustvari CSV datoteko z glavo.
def zapisi_csv(seznam_slovarjev, imena_polj, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in seznam_slovarjev:
            writer.writerow(slovar)


#Iz danega objekta ustvari JSON datoteko.
def zapisi_json(objekt, ime_datoteke):
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as json_datoteka:
        json.dump(objekt, json_datoteka, indent=4, ensure_ascii=False)