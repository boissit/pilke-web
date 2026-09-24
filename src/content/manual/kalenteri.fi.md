---
title: Vapaat ajat kalenteriin
lead: Merkitse kalenteriin ajat, jolloin voisit lähteä treffeille. Ehdokkaita löytyy vain yhteisille ajoille.
kind: guide
order: 30
draft: true
---

Kalenteri on alapalkin **Kalenteri**-välilehti. Merkinnät ovat treffivarauksia: aikoja, jolloin olet valmis lähtemään treffeille.

Ehdokas löytyy vain, jos teillä on vähintään {{calendar.min_shared_hours}} tunnin yhteinen aika. Mitä enemmän aikoja merkitset, sitä useampi voi olla sinulle ehdokas.

## Kalenterinäkymä

![Kalenterin viikkonäkymä, jossa on merkittyjä aikoja ja kellertäviä tunteja](shot:kalenteri#calendar-menu,calendar-explainer)

Ruudukossa näkyy muutama päivä kerrallaan. Pyyhkäise sivulle, niin näet muut päivät. Nipistä kahdella sormella, jos haluat suurentaa tunteja.

Otsikon vieressä on kaksi painiketta. **⋮** (1) avaa **Pikatoiminnot**. **i** (2) avaa lyhyen ohjeen.

Voit merkitä aikoja enintään {{calendar.horizon_days}} päivän päähän. Menneitä merkintöjä ei voi muuttaa.

## Uuden ajan merkitseminen

![Uutta aikaa merkitään vetämällä ruudukossa](shot:kalenteri-drag)

1. Paina ruudukkoa pitkään kohdasta, josta aika alkaa.
2. Vedä sormea, niin merkintä kasvaa.
3. Päästä irti. Merkintä tallentuu.

Merkinnän on oltava vähintään {{calendar.min_slot_hours}} tunnin mittainen. Lyhyempää sovellus ei tallenna.

## Merkinnän muuttaminen ja poistaminen

1. Napauta merkintää, niin se valitaan.
2. Siirrä sitä raahaamalla, tai muuta pituutta vetämällä ylä- tai alareunasta.
3. Poista merkintä kulman **✕**-painikkeella.

Jos aika kuuluu treffikutsuun tai sovittuihin treffeihin, sitä ei voi muuttaa. Sovellus kertoo silloin: *Tämä merkintä on treffikutsu, joten sitä ei voi muuttaa.*

## Puhelimen oman kalenterin tapahtumat

Jos olet sallinut sen asetuksissa, puhelimesi kalenterin tapahtumat näkyvät raidoitettuina. Ne näyttävät, milloin olet jo varattu. Niitä ei voi muokata Pilkkeessä. Katso [Asetukset](/ohje/asetukset).

## Kellertävät tunnit

Osa tunneista on sävytetty kellertäviksi. Ne ovat aikoja, jolloin moni sinulle sopiva ihminen on merkinnyt olevansa vapaa. Mitä tummempi sävy, sitä enemmän heitä on.

- Mukana ovat vain ihmiset, jotka voisivat olla sinulle ehdokkaita: toiveenne sopivat yhteen ja teillä on yhteinen treffialue.
- Tunti sävytetään vasta, kun vapaita on vähintään {{calendar.density_min_people}}. Siksi kenenkään kalenteria ei voi päätellä sävyistä.
- Sävyt kattavat seuraavat {{calendar.density_days}} päivää. Kaukana olevat päivät ovat usein tyhjiä, koska harvempi on ehtinyt merkitä niin pitkälle.

Sävy ei ole ihmisten lukumäärä. Se kertoo, mihin aikoihin kannattaa merkitä, jos haluat ehdokkaita.

## Viikon toistaminen

![Pikatoiminnot-valikko ja Kopioi tämä viikko -ehdotus kalenterissa](shot:kalenteri-toistuva#repeat-proposal,repeat-save,repeat-cancel)

1. Paina **⋮** ja valitse **Kopioi tämä viikko**.
2. Sovellus kopioi kuluvan viikon (maanantaista sunnuntaihin) treffivaraukset seuraavalle viikolle. Ehdotetut ajat näkyvät katkoviivoin, ja ruudukon yläpuolella (1) lukee, montako aikaa ja tuntia ehdotus sisältää.
3. Voit muokata ehdotettuja aikoja ennen tallennusta.
4. Paina **Tallenna** (2), tai hylkää ehdotus painamalla **Peruuta** (3).

Ajat, jotka on jo varattu treffeille, jätetään pois. Jos kopioitavaa ei ole, sovellus kertoo: *Tällä viikolla ei ole kopioitavia treffivarauksia.*

## Muut pikatoiminnot

**Ehdota treffivarauksia** ehdottaa vapaita aikoja puhelimesi kalenterin ja aiempien merkintöjesi perusteella. Se tarvitsee luvan lukea kalenteriasi. Ehdotus tallennetaan samalla tavalla kuin kopioitu viikko.

**Tyhjennä kalenteri** poistaa tulevat treffivaraukset. Sovitut treffit ja avoimet kutsut säilyvät. Sovellus kysyy vielä **Tyhjennä?** ennen kuin mitään poistetaan.

## Terälehdet kalenterista

Kalenteri tuottaa terälehtiä sitä mukaa, kun merkityt ajat ovat voimassa. Noin {{calendar.petal_week_hours}} tuntia merkittyä aikaa viikon ajan tuottaa yhden terälehden. Tarkemmin: [Terälehdet](/ohje/teralehdet).

![Kalenterin ohje avattuna](shot:popover-calendar)

Unohtuiko jokin? Kalenterin **i** kertoo eleet lyhyesti.
