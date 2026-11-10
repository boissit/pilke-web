---
title: Peruminen ja jäähy
lead: Saat jäähyn, jos perut sovitut treffit tai lähettämäsi kutsun. Samoin käy, jos hylkäät saamasi kutsun, jätät sen vastaamatta tai et saavu treffeille. Tältä sivulta näet, kuinka kauan jäähy kestää ja mitä voit sen aikana tehdä.
order: 60
draft: true
---

Sovitut treffit ovat teidän yhteinen päätöksenne. Toinen on varannut ajan sinulle, eikä hän voi kysyä sinulta mitään, koska sovelluksessa ei ole viestejä. Peruminen on siksi epäkohteliasta, ja siitä saa jäähyn. Jäähy päättyy itsestään, ja kipinäsi pysyvät ennallaan.

## Kaksi jäähyä

| Jäähy | Mitä jäähy estää | Ilmoituksessa lukee |
|---|---|---|
| Molemmat | Et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita. | *Sillä aikaa et näy muiden ehdokkaissa etkä voi löytää uusia ehdokkaita.* |
| Ei hakua | Et voi hakea uusia ehdokkaita, mutta näyt muiden ehdokkaissa. | *Sillä aikaa et voi löytää uusia ehdokkaita.* |

Jäähyn aikana voit vastata saamiisi kutsuihin ja käydä sovituilla treffeillä. Avoimet kutsusi ja sovitut treffisi pysyvät ennallaan. Jos olit jo löytänyt ehdokkaat, voit vielä kutsua jonkun heistä.

![Ilmoitus Treffit-sivulla: et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita](shot:cooldown-blocked#cooldown-notice)

Treffit-sivun yläosan ilmoitus (1) kertoo, mitä jäähy estää, mihin asti ja miksi. Sama teksti tulee näkyviin, jos yrität hakea ehdokkaita. Jos jäähyjä on useampi, ilmoitus kertoo viimeisenä päättyvän syyn ja päättymisajan.

## Mistä jäähy alkaa

| Mitä teit | Jäähy | Kesto |
|---|---|---|
| Peruutit lähettämäsi kutsun ennen vastausta | Ei hakua | {{cooldown.withdrawal_hours}} tuntia |
| Hylkäsit saamasi kutsun | Ei hakua | {{cooldown.decline_hours}} tuntia |
| Jätit saamasi kutsun vastaamatta | Ei hakua | {{cooldown.no_answer_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_long_notice_days}} päivää ennen | Molemmat | {{cooldown.cancel_long_notice_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_short_notice_hours}} tuntia ennen | Molemmat | {{cooldown.cancel_short_notice_days}} päivää |
| Peruit sovitut treffit myöhemmin | Molemmat | {{cooldown.cancel_late_days}} päivää |
| Toinen kertoi treffipaikalta, ettet saapunut | Molemmat | {{cooldown.noshow_days}} päivää |

Jos perut usein, jäähy pitenee. Jokainen sovittujen treffien peruminen viimeisen {{cooldown.repeat_window_days}} päivän ajalta kertoo seuraavan perumisen jäähyn {{cooldown.repeat_multiplier}}:lla. Pisin jäähy on {{cooldown.ceiling_days}} päivää. Kerrointa kasvattavat vain sovittujen treffien perumiset, eivät kutsuihin liittyvät jäähyt eivätkä saapumatta jäämiset.

![Ilmoitus Treffit-sivulla: et voi hakea uusia ehdokkaita, koska hylkäsit saamasi treffikutsun](shot:cooldown-decline#cooldown-notice)

Kutsun voi hylätä perustelematta, ja kutsujalle hylkäys on parempi vastaus kuin hiljaisuus. Hylkäämisestä ja vastaamatta jättämisestä saa lyhyen jäähyn (1), koska toinen käytti kutsuun kipinöitä ja odotti vastaustasi. Jäähyn aikana näyt edelleen muiden ehdokkaissa ja voit vastata saamiisi kutsuihin.

## Mitä perumisesta seuraa toiselle

Toinen saa perumisesta heti ilmoituksen. Sitä ei voi kytkeä pois, koska muuten hän lähtisi odottamaan ihmistä, joka ei tule. Sovittu aika vapautuu teiltä molemmilta. Jos kutsuit hänet, kipinäsi jäävät käytetyiksi. Jos hän kutsui sinut, {{petals.refund}} kipinää palaa hänelle.

Treffit perut treffisivun painikkeella **Peru treffit**. Ennen vahvistusta näet, milloin jäähysi päättyisi. Kun treffien alkamisaika on ohi, painike katoaa.

Peru heti, kun tiedät, ettet pääse. Mitä aikaisemmin perut, sitä lyhyempi jäähy.
