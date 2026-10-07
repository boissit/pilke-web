---
title: Kipinät
lead: Pilke pyörii kipinöiden ympärillä. Niitä kertyy ylläpidetystä kalenterista ja käydyistä treffeistä, ja {{petals.set_cost}} kipinällä lähetät treffikutsun.
order: 30
draft: true
---

Kipinäsi näkyvät Treffit-sivun ylälaidassa. Tältä sivulta näet, mistä niitä kertyy, mihin ne kuluvat ja milloin ne palaavat sinulle.

## Mistä kipinät tulevat ja minne ne menevät

| Mitä tapahtuu | Kipinät |
|---|---|
| Vahvistat puhelinnumerosi, kun luot profiilin | +{{petals.signup_bonus}}, kerran |
| Kalenterissasi on {{calendar.petal_week_hours}} tuntia vapaata aikaa viikon ajan | +1 |
| Käyt treffeillä ja kerrot, miten meni | +{{petals.per_date}}, kun lähetät palautteen |
| Lähetät treffikutsun | −{{petals.set_cost}}, kun painat **Lähetä treffikutsu!** |
| Kutsusi hylätään | +{{petals.refund}} takaisin |
| Kutsusi raukeaa, koska siihen ei vastattu {{invitation.answer_hours}} tunnissa | +{{petals.refund}} takaisin |
| Kutsumasi henkilö peruu sovitut treffit | +{{petals.refund}} takaisin |
| Sopivia ehdokkaita ei löydy | Kipinät pysyvät tallessa |
| Peruutat kutsusi ennen kuin toinen vastaa | Ei palautusta |
| Et kutsu ketään löytämistäsi ehdokkaista | Ei palautusta |
| Perut sovitut treffit | Ei palautusta |

Palautuksena saat takaisin ne {{petals.refund}} kipinää, jotka kutsuun kuluivat.

Treffeistä kipinät tulevat palautteen mukana. Kumpikin saa omansa, kun on itse vastannut.

## Kalenterin kipinät

Kalenterista kertyy kipinöitä sen mukaan, kuinka kauan vapaa aika pysyy merkittynä. {{calendar.petal_week_hours}} tuntia viikon ajan tuo yhden kipinän, ja saman verran kertyy esimerkiksi {{calendar.counted_hours_cap}} tunnista vajaassa kahdessa päivässä. Kipinät tulevat yksi kerrallaan sitä mukaa kuin niitä kertyy.

- Mukaan lasketaan tulevat ajat ja niistä se osa, joka osuu seuraavan {{calendar.earning_horizon_days}} päivän sisälle. Tunti lakkaa kerryttämästä, kun se alkaa.
- Kerrallaan lasketaan enintään {{calendar.counted_hours_cap}} tuntia, joten kalenterista voi kertyä enintään {{calendar.max_petals_per_week}} kipinää viikossa.
- Aika, jonka merkitset ja poistat heti perään, ei kerrytä mitään.

### Esimerkkejä

| Kalenterissasi | Kipinöitä |
| --- | --- |
| Lauantai klo 18–22 (4 tuntia), merkitty viikkoa ennen | noin 0,4 |
| Sama lauantai, merkitty 20 päivää ennen: se alkaa kerryttää, kun lauantaihin on {{calendar.earning_horizon_days}} päivää | noin 0,8 |
| Noin 10 tuntia viikossa, aina kaksi viikkoa eteenpäin merkittynä | noin 2 viikossa |
| Vähintään {{calendar.counted_hours_cap}} tuntia seuraavan {{calendar.earning_horizon_days}} päivän aikana, koko ajan | {{calendar.max_petals_per_week}} viikossa |

## Yläraja

Kipinöitä voi olla kerrallaan enintään {{petals.cap}}, eli {{petals.cap_roses}} kutsun verran. Kun niitä on {{petals.cap}}, uudet kipinät jäävät odottamaan. Ne tulevat heti, kun lähetät kutsun ja tilaa vapautuu, joten kun kipinöitä on täysi määrä, ne kannattaa laittaa lentoon.

Esimerkiksi: sinulla on {{petals.cap}} kipinää, ja kalenterisi kerryttää viikossa 2 lisää. Ne odottavat. Kun lähetät kutsun, {{petals.set_cost}} kipinää lähtee, ja kaksi odottanutta tulee perille. Palautteen kipinät tulevat vasta, kun ne mahtuvat kaikki kerralla.

Palautetut kipinät tulevat perille rajasta riippumatta, joten kipinöitä voi joskus olla yli {{petals.cap}}.

## Milloin kipinät kuluvat

![Treffikutsun viimeinen vaihe: kipinöiden määrä ja Lähetä treffikutsu! -painike](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Näet kipinäsi (1) ennen kuin lähetät kutsun. {{petals.set_cost}} kipinää lähtee heti, kun painat **Lähetä treffikutsu!** (2). Sen jälkeen löydät {{candidates.per_set}} ehdokasta ja valitset, kenelle kutsu lähtee.

Jos {{candidates.per_set}} sopivaa ehdokasta ei löydy, kipinäsi pysyvät tallessa. Jos taas löydät ehdokkaat etkä kutsu ketään heistä, kipinöitä ei palauteta. Ehdokkaat odottavat sinua {{candidates.set_hours}} tuntia: katso [Ketä sinulle näytetään](/ohje/ehdokkaat).
