import re

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
    r'<div class="vr\d"><a href=(?P<url_gorovje>.+?)>.+?</a></div>'
)

# Vzorec, ki bo iz strani, kjer je seznam vrhov v nekem gorovju,
# zajel url naslov vrha, ki nas pelje na stran s podatki o tem vrhu.
vzorec_url_vrh = re.compile(
    r'<tr class="vr\d"><td class="vrtd.*?"><a href=(?P<url_vrh>.+?)>.+?</a></td>'
)

# Vzorec, ki pobere podatke o vrhu, na koncu dobimo še blok, 
# iz katerega je potrebno dodatno pobrati podatke o poteh.
vzorec_podatki_gore = re.compile(
    r'</script>.*?'
    r'<div class="naslov1"><div style="float:left;"><h1>(?P<ime>.+?)</h1></div>.*?'
    r'<div class="g2"><b>Država:</b> <a class="moder" href="/gorovja">(?P<drzava>.+?)</a></div>.*?'
    r' <div class="g2"><b>Gorovje:</b> <a class="moder" href=.*?>(?P<gorovje>.+?)</a></div>.*?'
    r'<div class="g2"><b>Višina:</b> (?P<visina>.+?)&nbsp;m</div>.*?'
    r'<div class="g2"><b>Vrsta:</b> (?P<vrsta>.+?)</div>.*?'
    r'<div class="g2"><b>Ogledov:</b> (?P<stevilo_ogledov>.+?)</div>.*?'
    r'<div class="g2"><b>Priljubljenost:</b> (?P<priljubljenost>.+?)%.*?</div>.*?'
    r'<div class="g2"><b>Število poti:</b> <a class="moder" href="#poti">(?P<stevilo_poti>.+?)</a></div>.*?'
    r'<div style="padding-top:10px;"><b>Opis gore:</b><br />(?P<opis>.+?)</div>.*?'
    r'<table class="TPoti" id="poti">(?P<blok_poti>)</table>'
)

# Vzorec, ki iz bloka o poteh na nek vrh pobere podatke o posamezni poti. 
vzorec_podatki_pot = re.compile(
    r'<tr class="trG\d"><td class="tdG"><a href=.+?>(?P<ime_poti>.+?)</a></td>.*?'
    r'<td class="tdG"><a href=.+?>(?P<cas_poti>.+?)</a></td>.*?'
    r'<td class="tdG"><a href=.+?>(?P<tezavnost_poti>.+?)</a></td></tr>'
)