---
title: Ketä sinulle näytetään
lead: Miksi ehdokkaasi ovat juuri nämä ihmiset, missä järjestyksessä heidät näytetään ja miksi joku ei tule enää vastaan.
order: 40
draft: true
---

Löydät kerralla {{candidates.per_set}} ehdokasta. Pilke käy läpi kaikki, joiden kanssa treffit olisivat mahdollisia, ja valitsee heistä sinulle sopivimmat. Jos sopivia on alle {{candidates.per_set}}, ehdokkaiden haku peruuntuu, eivätkä kipinät kulu.

![Ehdokkaat-näkymä: keskimmäisen ehdokkaan kortti, yhteiset ajat ja paikat](shot:platter#timeslot-chip-*,activity-chip-*)

Ehdokkaan kortissa on hänen kuvansa, nimensä ja ikänsä. Lisäksi siinä on enintään {{candidates.times_per_card}} lähintä yhteistä aikaanne (1) ja enintään {{candidates.venues_per_card}} teille molemmille sopivaa treffipaikkaa (2). Niistä kokoat kutsun. Katso [Kutsut](/ohje/kutsut).

## Suosikkipaikat

Voit valita enintään {{candidates.favourite_venues_max}} suosikkipaikkaa Omien tietojen Paikat-sivulla. Kun suosikki sopii teille molemmille, se näkyy ehdokkaan kortilla ensimmäisenä. Ehdokkaasi valitaan samoin kuin aina; suosikit päättävät vain, mitkä paikat kortilla näkyvät ensin.

Kortilla tähti kertoo, kenen suosikki paikka on: {star:mine} on suosikkisi, {star:theirs} hänen suosikkinsa ja {star:both} molempien suosikki. Samat tähdet näet kutsussa ja treffien sivulla.

Suosikki pysyy tallessa, vaikka poistaisit sen treffialueen tai treffiaktiviteetin valinnoistasi, ja toimii taas, kun valitset ne uudelleen.

## Miksi juuri nämä ihmiset

Ehdokkaan pitää täyttää kaikki nämä ehdot. Ne tarkistetaan molempiin suuntiin, joten myös sinun pitää sopia hänen toiveisiinsa.

- **Yhteinen aika.** Kalentereissanne on vähintään {{calendar.min_shared_hours}} tunnin yhteinen vapaa aika. Ajat, jotka ovat jo toisessa avoimessa kutsussa tai sovituilla treffeillä, eivät kuulu mukaan.
- **Treffialue.** Alueella, jonka olette molemmat valinneet, on treffipaikka, joka sopii teidän molempien toivomaan tekemiseen.
- **Kieli.** Teillä on vähintään yksi yhteinen kieli.
- **Tekeminen.** Molemmat ovat toivoneet ainakin jotain samaa tekemistä.
- **Toiveet.** Sukupuolenne, ikänne ja muut mieltymykset sopivat toistenne toiveisiin.
- **Valinnanvara.** Teillä on vähintään {{invitation.choice_threshold}} yhteistä aikaa tai {{invitation.choice_threshold}} yhteistä paikkaa, jotta kutsun vastaanottajalla on varaa valita.

Myös **treffitahti** vaikuttaa. Sen valitset Omien tietojen Ajat-sivulla kohdassa *Kuinka usein haluaisit käydä treffeillä?* Jos ehdokas on valinnut *Kerran viikossa*, hänelle ehdotetaan aikoja ennen hänen viimeisimpiä sovittuja treffejään tai aikaisintaan {{matching.pace_weekly_days}} päivää niiden jälkeen. Valinnalla *Kerran kahdessa viikossa* väli on {{matching.pace_fortnightly_days}} päivää. Kun itse etsit ehdokkaita, omaan tahtiisi sopivat ajat näytetään ensin.

Persoonallisuuskyselyn vastaukset toimivat pohjana treffiehdokkaiden löytämiseen. Myöhemmin treffien jälkeinen treffipalaute ohjaa sopivimpien ehdokkaiden löytämistä.

## Miksi joku ei tule enää vastaan

- **Olette jo käyneet treffeillä.** Kun kaksi ihmistä on käynyt treffeillä, heitä ei enää ehdoteta toisilleen. Poikkeuksena tilanne, jossa molemmat valitsivat treffipalautteessa haluavansa tavata uudelleen Pilkkeen välityksellä. Katso [Treffien jälkeen](/ohje/treffien-jalkeen).
- **Hänet on näytetty sinulle äskettäin.** Äskettäin näytetty ehdokas laskee järjestyksessä, ja vaikutus puolittuu {{candidates.exposure_half_life_days}} päivässä. Kun sama ihminen on ollut ehdokkaanasi {{candidates.max_appearances}} kertaa, et näe häntä enää.

## Kuinka kauan ehdokkaat odottavat

Ehdokkaasi odottavat sinua {{candidates.set_hours}} tuntia. Jos kutsu jää kesken, Treffit-sivun painikkeessa lukee **Viimeistele kutsu**. Se vie sinut takaisin samojen ehdokkaiden luo, eikä uusia kipinöitä kulu. Uudet ehdokkaat löydät, kun olet lähettänyt kutsun tai nämä ehdokkaat ovat vanhentuneet.

Ehdokkaat vanhenevat jo aiemmin, jos yhdellekin heistä ei voi enää lähettää kutsua. Näin käy, kun kortin ajat ovat menneet ohi tai varautuneet toiseen kutsuun. Silloin kaikki ehdokkaat vanhenevat, eikä kipinöitä palauteta.

Kun lähetät kutsun, muut ehdokkaat poistuvat.

![Ilmoitus Treffit-sivulla: et voi hakea uusia ehdokkaita tiettyyn aikaan asti](shot:cooldown-nodraw#cooldown-notice)

Jos et juuri nyt voi löytää ehdokkaita, Treffit-sivun ilmoitus (1) kertoo syyn ja sen, milloin jäähy päättyy. Katso [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).

## Kysyttyä

**Miksi ehdokkaita ei löytynyt?** Sopivia ehdokkaita oli alle {{candidates.per_set}}. Sovellus pyrkii kertomaan, jos tähän voi vaikuttaa valinnoillasi. Tähän vaikuttavat toiveet, tekeminen, treffialueet, yhteinen aika tai se, että sopivia ihmisiä on rekisteröityneenä toistaiseksi vähän. Painikkeesta pääset suoraan kalenteriin tai siihen Omien tietojen sivuun, jolla voit muuttaa ehtoa. Samat askeleet näet Treffit-sivun kohdassa **Seuraavaksi**. Useimmiten auttaa, kun merkitset kalenteriin lisää aikaa, varsinkin [korostetuille tunneille](/ohje/vapaat-ajat#kellertävät-tunnit). Jos ehdokkaita ei löytynyt, kipinät eivät kulu.

**Näkeekö joku, että hän oli ehdokkaani?** Ei. Ehdokas saa tietää sinusta vasta, kun lähetät hänelle kutsun.

**Miten näyn useammin muiden ehdokkaissa?** Merkitse enemmän aikaa, varsinkin [korostetuille tunneille](/ohje/vapaat-ajat#kellertävät-tunnit), ja valitse useampia treffialueita ja tekemisiä.
