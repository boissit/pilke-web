---
title: Ketä sinulle näytetään
lead: Miksi ehdokkaasi ovat juuri nämä ihmiset, missä järjestyksessä heidät näytetään ja miksi joku ei tule enää vastaan.
order: 40
draft: true
---

Löydät kerralla {{candidates.per_set}} ehdokasta. Pilke käy läpi kaikki, joiden kanssa treffit olisivat mahdollisia, ja valitsee heistä {{candidates.per_set}} sinulle sopivinta. Jos heitä ei löydy {{candidates.per_set}}, terälehtiä ei veloiteta.

![Ehdokkaat-näkymä: keskimmäisen ehdokkaan kortti, yhteiset ajat ja yhteinen tekeminen](shot:platter#timeslot-chip-0,activity-chip-0)

Jokaisessa kortissa on ehdokkaan kuva, nimi ja ikä, enintään {{candidates.times_per_card}} lähintä yhteistä aikaanne (1) ja enintään {{candidates.venues_per_card}} treffipaikkaa, jotka sopivat teille molemmille (2). Niistä kokoat kutsun. Katso [Kutsut](/ohje/kutsut).

## Miksi juuri nämä ihmiset

Ehdokkaan on täytettävä kaikki nämä ehdot, ja ne tarkistetaan molempiin suuntiin: sinunkin pitää sopia hänen toiveisiinsa.

- **Yhteinen aika.** Kalentereissanne on vähintään {{calendar.min_shared_hours}} tunnin yhteinen aika. Toisen avoimen kutsun tai sovittujen treffien ajat eivät ole yhteistä aikaa.
- **Treffialue.** Alueella, jonka olette molemmat valinneet, on treffipaikka, joka sopii teidän molempien toivomaan tekemiseen.
- **Kieli.** Teillä on vähintään yksi yhteinen kieli.
- **Tekeminen.** Haluatte ainakin osittain samanlaisille treffeille.
- **Toiveet.** Sukupuoli ja ikä sopivat kummankin toiveisiin, ja teillä on yhteinen vastaus siihen, mitä odotatte treffeiltä.
- **Vaihtoehto.** Teillä on vähintään {{invitation.choice_threshold}} yhteistä aikaa tai {{invitation.choice_threshold}} yhteistä paikkaa, jotta kutsussa voi tarjota valinnan.

Lisäksi vaikuttaa **treffitahti**, Omien tietojen kohta *Kuinka usein haluaisit käydä treffeillä?* Jos ehdokas on valinnut *Kerran viikossa*, häntä ei näytetä muille, kun hänellä on sovitut treffit {{matching.pace_weekly_days}} päivän sisällä kumpaan tahansa suuntaan. *Kerran kahdessa viikossa* toimii samoin {{matching.pace_fortnightly_days}} päivän sisällä. Sama koskee sinua, kun olet muiden ehdokas. Omien ehdokkaidesi löytämiseen tahti ei vaikuta.

## Miksi joku ei tule enää vastaan

- **Toinen on lähettänyt toiselle kutsun.** Kun kahden ihmisen välillä on ollut kutsu, kumpaan suuntaan tahansa ja miten tahansa se päättyi, heitä ei enää ehdoteta toisilleen. Poikkeus on, jos te molemmat vastasitte treffien jälkeen haluavanne tavata uudelleen. Katso [Treffien jälkeen](/ohje/treffien-jalkeen).
- **Hänet on näytetty sinulle äskettäin.** Äskettäin näytetty ehdokas laskee järjestyksessä. Vaikutus puolittuu {{candidates.exposure_half_life_days}} päivässä. Kun sama ihminen on ollut ehdokkaanasi {{candidates.max_appearances}} kertaa, häntä ei näytetä sinulle enää.
- **Toinen teistä on tehnyt turvallisuusilmoituksen.** Silloin teitä ei ehdoteta toisillenne koskaan.

## Missä järjestyksessä

Järjestykseen vaikuttaa persoonallisuuskysely: mitä useampaan sen kysymykseen olette vastanneet samoin, sitä korkeammalle ehdokas nousee. Äskettäin näytetyt laskevat, kuten yllä. Terälehdillä ei voi vaikuttaa järjestykseen.

## Kuinka kauan ehdokkaat odottavat

Ehdokkaasi odottavat sinua {{candidates.set_hours}} tuntia. Jos poistut, Treffit-sivun painikkeessa lukee **Viimeistele kutsu**, ja se vie sinut maksutta takaisin samojen ehdokkaiden luo. Uusia ehdokkaita löydät vasta, kun olet lähettänyt kutsun tai nämä ehdokkaat ovat vanhentuneet.

Ehdokkaat vanhenevat jo aiemmin, jos yhdellekin heistä ei voi enää lähettää kutsua: kortin ajat ovat menneet ohi tai varautuneet toiseen kutsuun. Silloin vanhenevat kaikki, eikä terälehtiä palauteta.

Kun lähetät kutsun, kaksi muuta ehdokasta poistuvat. He eivät saa tietää olleensa ehdokkainasi.

![Ilmoitus Treffit-sivulla: et voi hakea uusia ehdokkaita tiettyyn aikaan asti](shot:cooldown-nodraw#cooldown-notice)

Jos et pääse juuri nyt löytämään ehdokkaita, Treffit-sivulla on ilmoitus (1), jossa kerrotaan syy ja päättymisaika. Katso [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).

## Kysyttyä

**Miksi ehdokkaita ei löytynyt?** Sopivia ehdokkaita oli alle {{candidates.per_set}}. Sovellus kertoo, mikä ehto karsi viimeisetkin: toiveet, tekeminen, treffialueet, yhteinen aika tai se, että sopivia ihmisiä on juuri nyt vähän. Useimmiten apu on merkitä kalenteriin lisää aikaa, erityisesti kellertäville tunneille. Terälehtiä ei veloiteta.

**Näkeekö joku, että hän oli ehdokkaani?** Ei. Ehdokas saa tietää sinusta vasta, kun lähetät hänelle kutsun.

**Miten tulen itse useammin ehdotetuksi?** Merkitse enemmän aikaa, erityisesti kellertäville tunneille, ja valitse useampia treffialueita ja tekemisiä. Jäähyn aikana sinua ei ehdoteta.
