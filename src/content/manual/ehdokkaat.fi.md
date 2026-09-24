---
title: Ehdokkaat
lead: Näin avaat ehdokasvalikoiman ja valitset, kenelle lähetät treffikutsun.
kind: guide
order: 40
draft: true
---

Valikoimassa on {{candidates.per_set}} ehdokasta. Valitset heistä yhden ja tarjoat hänelle aikoja ja paikkoja. Valikoiman avaaminen maksaa {{petals.set_cost}} terälehteä.

## Valikoiman avaaminen

Paina Treffit-sivulla **Löydä treffit!**.

![Ensimmäinen vaihe: kalenteri ja Seuraava-painike](shot:date-wizard-kalenteri#date-wizard-next)

Ensin näet kalenterisi. Ehdokkaat haetaan sen perusteella, joten tarkista, että ajat ovat ajan tasalla. Paina sitten **Seuraava** (1).

![Toinen vaihe: terälehtien määrä ja Lähetä treffikutsu! -painike](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Seuraavaksi näet terälehtesi (1). Paina **Lähetä treffikutsu!** (2), niin Pilke hakee sinulle ehdokkaat.

Terälehdet kuluvat tässä vaiheessa. Itse kutsun lähettäminen ei maksa enää mitään. Jos terälehtiä ei ole tarpeeksi, näet tekstin *Tarvitset lisää terälehtiä* ja painikkeen **Takaisin**.

## Ehdokkaiden selaaminen

![Ehdokkaat-näkymä: ehdokkaan kuva, yhteiset ajat ja yhteinen tekeminen](shot:platter#card-map-toggle,timeslot-chip-0,activity-chip-0,propose)

Ehdokkaat ovat kortteina rinnakkain. Pyyhkäise sivulle, niin näet seuraavan. Keskimmäinen kortti on se, jonka Pilke arvioi sinulle sopivimmaksi.

Kortissa on ehdokkaan kuva, nimi ja ikä. **Kartta** (1) näyttää kuvan tilalla yhteiset treffipaikat kartalla. **Kuva** palauttaa kuvan.

Näin kokoat kutsun:

1. Valitse kohdasta **Yhteiset ajat** (2) ajat, jotka sopisivat sinulle. Kortissa on enintään {{candidates.times_per_card}} lähintä aikaa, jolloin olette molemmat vapaita.
2. Valitse kohdasta **Yhteinen tekeminen** (3) paikat, joihin haluaisit mennä. Kortissa on enintään {{candidates.venues_per_card}} paikkaa.
3. Paina **Ehdota!** (4).

Valitse vähintään {{invitation.min_times_offered}} aika ja {{invitation.min_venues_offered}} paikka. Lisäksi kutsussa pitää olla vaihtoehto: joko {{invitation.choice_threshold}} aikaa tai {{invitation.choice_threshold}} paikkaa. Jos jokin puuttuu, kortti kertoo sen, eikä **Ehdota!** toimi.

Kutsu lähtee heti. Valikoiman muut ehdokkaat poistuvat, ja palaat Treffit-sivulle. Toinen valitsee tarjoamistasi yhden ajan ja yhden paikan. Katso [Treffikutsu](/ohje/kutsu).

## Jos et lähetä kutsua heti

Valikoima säilyy {{candidates.set_hours}} tuntia. Sillä välin Treffit-sivun painikkeessa lukee **Viimeistele kutsu**, ja se vie takaisin samaan valikoimaan.

Valikoima vanhenee aiemmin, jos sen ajat ehtivät mennä ohi. Vanhentuneesta valikoimasta ei saa terälehtiä takaisin.

## Jos ehdokkaita ei löydy

Jos Pilke ei löydä {{candidates.per_set}} sopivaa ehdokasta, terälehtiä ei kulu. Näet syyn, esimerkiksi:

- *Kenelläkään sopivalla ei ole yhtään yhteistä aikaa kanssasi.* Merkitse kalenteriin lisää aikoja.
- *Toiveesi eivät juuri nyt osu keneenkään.* Väljennä toiveitasi Asetusten Omissa tiedoissa.
- *Treffialueillasi ei ole ketään sopivaa.* Valitse lisää treffialueita.
- *Sopivia ihmisiä on juuri nyt liian vähän.* Kokeile myöhemmin uudelleen.

Jos et voi juuri nyt hakea ehdokkaita, näet syyn ja päättymisajan. Katso [Jäähdytys](/ohje/jaahdytys). Miten ehdokkaat valitaan, kerrotaan sivulla [Näin ehdokkaat valitaan](/ohje/ehdokkaiden-valinta).
