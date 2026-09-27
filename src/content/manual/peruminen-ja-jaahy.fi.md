---
title: Peruminen ja jäähy
lead: Jos perut sovitut treffit, peruutat kutsun tai et saavu paikalle, Pilke pitää tauon. Tässä, mistä tauko alkaa, kuinka kauan se kestää ja mitä se estää.
order: 60
draft: true
---

Sovitut treffit ovat kahden ihmisen yhteinen päätös. Toinen on varannut illan sinulle, eikä hän voi kysyä sinulta mitään, koska sovelluksessa ei ole keskusteluyhteyttä. Peruminen on siksi epäkohteliasta häntä kohtaan, ja jäähy on tauko, joka seuraa siitä. Se ei vie terälehtiä, ja se päättyy itsestään.

## Kolme jäähyä

| Jäähy | Mitä et voi tehdä | Ilmoitus alkaa |
|---|---|---|
| Molemmat | Et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita. | *Et näy juuri nyt muiden treffiehdokkaissa etkä voi hakea uusia ehdokkaita …* |
| Ei hakua | Et voi hakea uusia ehdokkaita. Näyt muille. | *Et voi hakea uusia ehdokkaita …* |
| Et näy | Et näy muiden ehdokkaissa. Voit hakea ehdokkaita. | *Et näy juuri nyt muiden treffiehdokkaissa …* |

Jäähyn aikana voit silti vastata saamiisi kutsuihin ja käydä sovituilla treffeillä. Avoimet kutsusi ja sovitut treffisi pysyvät ennallaan. Jos olit jo löytänyt ehdokkaat, voit silti lähettää kutsun jollekulle heistä.

![Ilmoitus Treffit-sivulla: et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita](shot:cooldown-blocked#cooldown-notice)

Jäähyn aikana Treffit-sivun yläosassa on ilmoitus (1): mitä se estää, mihin asti ja miksi. Sama teksti näkyy, jos yrität hakea ehdokkaita. Jos voimassa on useampi jäähy, ilmoitus kertoo viimeisenä päättyvän syyn ja päättymisajan.

![Ilmoitus Treffit-sivulla: et voi hakea uusia ehdokkaita](shot:cooldown-nodraw#cooldown-notice)

Kun et voi hakea ehdokkaita, mutta näyt muille, ilmoitus (1) on lyhyempi. Tämä seuraa kutsun peruuttamisesta.

<!-- hidden-cooldown: pending owner decision -->

![Ilmoitus Treffit-sivulla: et näy muiden ehdokkaissa](shot:cooldown-hidden#cooldown-notice)

Kolmas jäähy (1) piilottaisi sinut muiden ehdokkaista, jos saamiasi kutsuja jäisi toistuvasti hyväksymättä. Sääntö ei ole tällä hetkellä käytössä, joten kutsujen hylkääminen tai vastaamatta jättäminen ei piilota sinua.

## Mistä jäähy alkaa

| Mitä teit | Jäähy | Kesto |
|---|---|---|
| Peruutit lähettämäsi kutsun ennen vastausta | Ei hakua | {{cooldown.withdrawal_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_long_notice_days}} päivää ennen | Molemmat | {{cooldown.cancel_long_notice_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_short_notice_hours}} tuntia ennen | Molemmat | {{cooldown.cancel_short_notice_days}} päivää |
| Peruit sovitut treffit myöhemmin | Molemmat | {{cooldown.cancel_late_days}} päivää |
| Toinen kertoi, ettet saapunut | Molemmat | {{cooldown.noshow_days}} päivää |

Toistuva peruminen pidentää taukoa. Jokainen aiempi sovittujen treffien peruminen viimeisen {{cooldown.repeat_window_days}} päivän ajalta kertoo seuraavan perumisen keston {{cooldown.repeat_multiplier}}:lla. Jäähy kestää kuitenkin enintään {{cooldown.ceiling_days}} päivää. Kutsujen peruutukset ja saapumatta jäämiset eivät kasvata kerrointa.

## Mitä perumisesta seuraa toiselle

Kun perut sovitut treffit, toinen saa siitä heti ilmoituksen. Ilmoitusta ei voi kytkeä pois, koska ilman sitä hän lähtisi odottamaan ihmistä, joka ei tule. Sovittu aika vapautuu teiltä molemmilta. Jos kutsuit hänet itse, käyttämiäsi terälehtiä ei palauteta. Jos hän kutsui sinut, hän saa takaisin {{petals.refund}} terälehteä, jotka hän käytti kutsuun.

Sovitut treffit perutaan treffisivun **Peru treffit** -painikkeella. Kun treffien alkamisaika on ohi, painiketta ei enää ole.

Peru siis heti, kun tiedät, ettet pääse: mitä aikaisemmin perut, sitä lyhyempi tauko on.
