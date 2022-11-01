import orodja


hribi_seznam_gorovij = "https://www.hribi.net/gorovja"


# Shranimo prvo stran, kjer je seznam gorovij. 
orodja.shrani_spletno_stran(hribi_seznam_gorovij, 'shranjene_strani/seznam_gorovij')


# Iz datoteke s prvo stranjo najprej poberemo blok, ki vsebuje samo slovenske gore.
# Iz dobljenega bloka poberemo delne url naslove posameznih gorovij
# in jih postopno dopolnimo ter shranimo spletne strani na teh naslovih. 
blok = orodja.poberi_blok('shranjene_strani/seznam_gorovij', orodja.vzorec_slovenska_gorovja)
if blok == []:
    print('V datoteki nismo našli iskanega bloka!')
else:
    niz = blok[0]
    seznam_slovarjev_url_gorovij = orodja.najdi_vzorec_v_nizu(niz, orodja.vzorec_url_gorovja)
    i = 0
    for url_slovar in seznam_slovarjev_url_gorovij:
        for url_niz in url_slovar.values():
            url_naslov = 'https://www.hribi.net' + url_niz
            orodja.shrani_spletno_stran(url_naslov, f'shranjene_strani/gorovje{i}/gorovje{i}')
            i += 1


# Na vsaki shranjeni strani s posameznim gorovjem, moramo sedaj pobrati url naslove posamezne gore.
# Za vsak tak naslov shranimo spletno stran.
stevec = 0
for j in range(2):
    seznam_slovarjev_url_vrhov = orodja.najdi_vzorec_v_datoteki(f'shranjene_strani/gorovje{j}/gorovje{j}', orodja.vzorec_url_vrh)
    k = 0
    for url_slovar in seznam_slovarjev_url_vrhov:
        for url_niz in url_slovar.values():
            url_naslov = 'https://www.hribi.net' + url_niz
            orodja.shrani_spletno_stran(url_naslov, f'shranjene_strani/gorovje{j}/vrh{j}.{k}')
            k += 1
            stevec+=1
print(stevec)


# Iz vsake spletne strani za posamezen vrh moramo ven pobrati podatke o vrhu in jih zapisati v slovar. 
# Hkrati še iz bloka poti poberem podatke in jih shranimo v podslovar.
seznam_podatki_vrhov = []
for j in range(2):
    k = 0 
    while orodja.preveri_obstoj_datoteke(f'shranjene_strani/gorovje{j}/vrh{j}.{k}') == True:
        podatki = orodja.najdi_vzorec_v_datoteki(f'shranjene_strani/gorovje{j}/vrh{j}.{k}', orodja.vzorec_podatki_gore)
        for slovar_vrh in podatki:
            blok_poti = slovar_vrh.get('blok_poti')
            slovar_poti = orodja.najdi_vzorec_v_nizu(blok_poti, orodja.vzorec_podatki_pot)
            slovar_vrh['blok_poti'] = slovar_poti
            slovar_vrh = orodja.popravi_podatke_vrh(slovar_vrh)
        seznam_podatki_vrhov += podatki
        k += 1

# Posebej naredimo še seznam vseh poti.
seznam_vseh_poti = []
for vrh in seznam_podatki_vrhov:
    seznam_poti = vrh['blok_poti']
    for pot in seznam_poti:
        pot['vrh'] = vrh['ime']
        seznam_vseh_poti.append(pot)


orodja.zapisi_csv(seznam_podatki_vrhov, ['ime', 'drzava', 'gorovje', 
'visina', 'vrsta', 'stevilo_ogledov', 'priljubljenost', 'stevilo_poti', 'opis', 'blok_poti'],
    'obdelani_podatki/hribi.csv')

orodja.zapisi_csv(seznam_vseh_poti, ['ime_poti', 'cas_poti', 'tezavnost_poti', 'vrh'], 
    'obdelani_podatki/poti.csv')