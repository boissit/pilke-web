---
title: Terälehdet
lead: Terälehdet ovat Pilkkeen valuutta. Ansaitset niitä käymällä treffeillä ja kulutat niitä lähettämällä treffikutsuja.
order: 30
draft: true
---

{{petals.per_rose}} terälehteä on yksi ruusu, ja yksi ruusu on yhden treffikutsun hinta. Tältä sivulta näet, mistä niitä tulee, mihin ne menevät ja milloin saat ne takaisin.

## Terälehtien ansainta ja kuluminen

| Mitä tapahtuu | Terälehdet |
|---|---|
| Kalenterissasi on {{calendar.petal_week_hours}} tuntia vapaata aikaa viikon ajan | +1 |
| Käyt treffeillä ja annat niistä palautteen | +{{petals.per_date}}, kun lähetät palautteen |
| Lähetät treffikutsun | −{{petals.set_cost}}, kun painat **Lähetä treffikutsu!** |
| Kutsusi hylätään | +{{petals.refund}} takaisin |
| Kutsusi raukeaa, koska siihen ei vastattu {{invitation.answer_hours}} tunnissa | +{{petals.refund}} takaisin |
| Kutsumasi henkilö perui sovitut treffit | +{{petals.refund}} takaisin |
| Sopivia ehdokkaita ei löydy | Mitään ei veloiteta |
| Peruutat kutsusi ennen kuin toinen vastaa | Ei palautusta |
| Et kutsu ketään löytämistäsi ehdokkaista | Ei palautusta |
| Perut sovitut treffit | Ei palautusta |

Palautuksena saat takaisin ne {{petals.refund}} terälehteä, jotka kutsu maksoi.

Treffeistä saa terälehtiä vain palautteesta. Jos et anna palautetta, et saa niitä. Kumpikin saa omansa, kun on itse vastannut.

## Kalenterin terälehdet

Kalenteri maksaa siitä, kuinka kauan vapaa aika pysyy merkittynä. {{calendar.petal_week_hours}} tuntia viikon ajan on yksi terälehti, ja sama määrä kertyy esimerkiksi {{calendar.counted_hours_cap}} tunnista vajaassa kahdessa päivässä. Terälehdet tulevat tilille yksi kerrallaan sitä mukaa kuin niitä kertyy.

- Mukaan lasketaan vain ajat, jotka eivät ole vielä alkaneet, ja niistä se osa, joka on seuraavan {{calendar.earning_horizon_days}} päivän sisällä. Tunti lakkaa kerryttämästä, kun se alkaa.
- Kerrallaan lasketaan enintään {{calendar.counted_hours_cap}} tuntia. Kalenterista voi siis kertyä enintään {{calendar.max_petals_per_week}} terälehteä viikossa.
- Ajan merkitseminen ja poistaminen heti perään ei tuota mitään.

### Esimerkkejä

| Kalenterissasi | Terälehtiä |
| --- | --- |
| Lauantai klo 18–22 (4 tuntia), merkitty viikkoa ennen | noin 0,4 |
| Sama lauantai, merkitty 20 päivää ennen: se alkaa kerryttää, kun lauantaihin on {{calendar.earning_horizon_days}} päivää | noin 0,8 |
| Noin 10 tuntia viikossa, aina kaksi viikkoa eteenpäin merkittynä | noin 2 viikossa |
| Vähintään {{calendar.counted_hours_cap}} tuntia seuraavan {{calendar.earning_horizon_days}} päivän aikana, koko ajan | {{calendar.max_petals_per_week}} viikossa |

## Yläraja

Tilillä voi olla kerrallaan enintään {{petals.cap}} terälehteä, eli {{petals.cap_roses}} ruusua. Kun tili on täynnä, uudet terälehdet jäävät odottamaan. Ne tulevat heti, kun lähetät kutsun ja tilille vapautuu tilaa, joten täyttä tiliä kannattaa käyttää.

Esimerkiksi: tililläsi on {{petals.cap}} terälehteä, ja kalenterisi ansaitsee viikossa 2 lisää. Ne odottavat. Kun lähetät kutsun, tililtä lähtee {{petals.set_cost}}, ja odottaneet 2 tulevat perille. Palautteen {{petals.per_date}} terälehteä tulevat vasta, kun ne mahtuvat tilille kaikki kerralla.

Palautukset tulevat perille rajasta riippumatta, joten saldo voi joskus olla yli {{petals.cap}}.

## Milloin terälehdet kuluvat

![Treffikutsun viimeinen vaihe: terälehtien määrä ja Lähetä treffikutsu! -painike](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Näet terälehtesi (1) ennen kuin lähetät kutsun. Terälehdet kuluvat heti, kun painat **Lähetä treffikutsu!** (2). Sen jälkeen löydät {{candidates.per_set}} ehdokasta ja valitset, kenelle kutsu lähtee.

Jos {{candidates.per_set}} sopivaa ehdokasta ei löydy, mitään ei veloiteta. Jos taas löydät ehdokkaat etkä kutsu ketään heistä, terälehtiä ei palauteta. Ehdokkaat odottavat sinua {{candidates.set_hours}} tuntia: katso [Ketä sinulle näytetään](/ohje/ehdokkaat).
