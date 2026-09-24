---
title: Terälehdet
lead: Terälehdillä avaat ehdokasvalikoiman. Niitä kertyy sovellusta käyttämällä, eikä niitä voi ostaa.
kind: explainer
order: 10
draft: true
---

Terälehti on Pilkkeen ainoa valuutta. {{petals.per_rose}} terälehteä tekee ruusun, ja ruusu avaa valikoiman. Muuta hintaa ei ole.

## Mihin terälehdet kuluvat

Valikoiman avaaminen maksaa {{petals.set_cost}} terälehteä. Ne kuluvat sillä hetkellä, kun painat **Lähetä treffikutsu!** ja ehdokkaat haetaan. Itse kutsun lähettäminen ei maksa mitään.

Kutsuun vastaaminen ei maksa mitään, hyväksytpä sen tai hylkäät sen.

## Mistä terälehtiä kertyy

| Mistä | Paljonko |
|---|---|
| Rekisteröinnin viimeistely, kun vahvistuskoodi on hyväksytty | {{petals.signup_bonus}}, kerran |
| Käydyt treffit, kun olet antanut niistä palautteen | {{petals.per_date}} |
| Toinen perui sovitut treffit | {{petals.consolation}} |
| Kalenteriin merkityt ajat | noin yksi viikossa jokaista {{calendar.petal_week_hours}} tuntia kohden |

Treffeistä molemmat saavat omansa erikseen, kun ovat vastanneet palautteeseen. Jos palautetta ei anna, terälehtiä ei tule.

## Kalenterin terälehdet

Kalenteri tuottaa terälehtiä sitä mukaa, kun merkityt ajat ovat voimassa. {{calendar.petal_week_hours}} tuntia vapaata aikaa, joka on merkittynä viikon ajan, tuottaa yhden terälehden.

- Mukaan lasketaan vain ajat, jotka eivät ole vielä alkaneet, ja niistä se osa, joka osuu seuraavan {{calendar.earning_horizon_days}} päivän sisään.
- Jokaisen ajan on oltava vähintään {{calendar.min_slot_hours}} tunnin mittainen.
- Kerrallaan lasketaan enintään {{calendar.counted_hours_cap}} tuntia. Siksi kalenterista voi kertyä enintään {{calendar.max_petals_per_week}} terälehteä viikossa.

Ajan merkitseminen ja poistaminen heti perään ei tuota mitään. Terälehtiä kertyy siitä, kuinka kauan aika on merkittynä.

## Terälehtien yläraja

Terälehtiä voi ansaita enintään {{petals.cap}}, eli {{petals.cap_roses}} ruusua. Kun raja tulee vastaan, uudet ansiot odottavat. Ne tulevat tilillesi, kun käytät terälehtiä ja rajan alle jää tilaa. Mitään ei menetetä.

Palautukset eivät ole ansioita, joten ne tulevat perille rajasta riippumatta. Siksi saldo voi joskus olla rajaa suurempi. Hyvitys toisen perumista treffeistä on ansio, ja se odottaa rajan alle mahtumista kuten muutkin.

## Milloin terälehdet palautetaan

| Mitä tapahtui | Mitä saat |
|---|---|
| Kutsusi hylättiin | {{petals.refund}} takaisin |
| Kutsuusi ei vastattu {{invitation.answer_hours}} tunnissa | {{petals.refund}} takaisin |
| Toinen perui sovitut treffit, ja sinä olit kutsuja | {{petals.refund}} takaisin ja lisäksi {{petals.consolation}} hyvityksenä |
| Pilke ei löytänyt tarpeeksi ehdokkaita | Mitään ei veloitettu |

Terälehtiä ei palauteta, jos peruutat oman kutsusi ennen vastausta tai jos avattu valikoima vanhenee käyttämättä. Molemmat olivat oma valintasi.

## Mitä terälehdillä ei voi tehdä

Terälehtiä ei myydä. Näkyvyyttä, korostusta tai parempaa sijaa ehdotuksissa ei voi ostaa.
