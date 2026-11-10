---
title: Peruminen ja jäähy
lead: Saat jäähyn, jos perut sovitut treffit tai lähettämäsi kutsun. Samoin käy, jos hylkäät saamasi kutsun, jätät sen vastaamatta tai et saavu treffeille. Tältä sivulta näet, miten jäähy toimii.
order: 60
draft: true
---

Sovitut treffit ovat sovitut, ja niihin on varattu aikaa. Peruminen on epäkohteliasta, ja siitä saa jäähyn.

## Jäähyn tyypit

| Jäähyn tyyppi | Mitä jäähy estää | Treffit-sivulla lukee |
|---|---|---|
| Ei hakua eikä kutsuja | Et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita. | *Sillä aikaa et näy muiden ehdokkaissa etkä voi löytää uusia ehdokkaita.* |
| Ei hakua | Et voi hakea uusia ehdokkaita, mutta näyt muiden ehdokkaissa. | *Sillä aikaa et voi löytää uusia ehdokkaita.* |

Jäähyn aikana voit vastata saamiisi kutsuihin ja käydä sovituilla treffeillä. Avoimet kutsusi ja sovitut treffisi pysyvät ennallaan.

![Ilmoitus Treffit-sivulla: et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita](shot:cooldown-blocked#cooldown-notice)

Treffit-sivun yläosan ilmoitus (1) kertoo, mitä jäähy estää, mihin asti ja miksi.

## Mistä jäähy alkaa

| Mitä teit | Jäähyn tyyppi | Kesto |
|---|---|---|
| Peruutit lähettämäsi kutsun ennen vastausta | Ei hakua | {{cooldown.withdrawal_hours}} tuntia |
| Hylkäsit saamasi kutsun | Ei hakua | {{cooldown.decline_hours}} tuntia |
| Jätit saamasi kutsun vastaamatta | Ei hakua | {{cooldown.no_answer_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_long_notice_days}} päivää ennen | Ei hakua eikä kutsuja | {{cooldown.cancel_long_notice_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_short_notice_hours}} tuntia ennen | Ei hakua eikä kutsuja | {{cooldown.cancel_short_notice_days}} päivää |
| Peruit sovitut treffit myöhemmin | Ei hakua eikä kutsuja | {{cooldown.cancel_late_days}} päivää |
| Toinen kertoi treffipaikalta, ettet saapunut | Ei hakua eikä kutsuja | {{cooldown.noshow_days}} päivää |

Jos perut usein, jäähy pitenee. Jokainen sovittujen treffien peruminen viimeisen {{cooldown.repeat_window_days}} päivän ajalta kertoo seuraavan perumisen jäähyn keston {{cooldown.repeat_multiplier}}:lla. Pisin jäähy on {{cooldown.ceiling_days}} päivää.

![Ilmoitus Treffit-sivulla: et voi hakea uusia ehdokkaita, koska hylkäsit saamasi treffikutsun](shot:cooldown-decline#cooldown-notice)

Kutsun voi aina hylätä perustelematta, ja se on parempi hylätä kuin jättää roikkumaan. Sovellus ei kuitenkaan toimi, jos kaikki hylkäävät kutsuja, joten siitä saa lyhyen jäähyn (1). Tämän jäähyn aikana näyt edelleen muiden ehdokkaissa ja voit vastata saamiisi kutsuihin.

## Miten peruminen näkyy toiselle

Toinen saa perumisesta heti ilmoituksen. Sovittu aika vapautuu teiltä molemmilta. Jos kutsuit hänet, kipinöitäsi ei palauteta. Jos hän kutsui sinut, hänen kipinänsä palautetaan.

Treffit perut treffisivun painikkeella **Peru treffit**.

Peru heti, kun tiedät, ettet pääse treffeille. Mitä aikaisemmin perut, sitä lyhyempi jäähy.
