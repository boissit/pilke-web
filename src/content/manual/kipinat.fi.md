---
title: Kipinät
lead: Deittailu vaatii kipinää. Kipinöitä kertyy ylläpidetystä kalenterista ja käydyistä treffeistä, ja {{petals.set_cost}} kipinällä lähetät treffikutsun.
order: 30
draft: false
---

Kipinäsi näkyvät Treffit-sivun ylälaidassa. Tällä sivulla kerromme, mistä niitä kertyy ja mihin ne kuluvat.

## Mistä kipinöitä saa ja mihin ne kuluvat

| Mitä tapahtuu | Kipinät |
|---|---|
| Vahvistat puhelinnumerosi, kun luot profiilin | +{{petals.signup_bonus}}, kerran |
| Kalenterissasi on {{calendar.petal_week_hours}} tuntia vapaata aikaa viikon ajan | +1 |
| Käyt treffeillä ja kerrot, miten meni | +{{sparks.per_date}}, kun lähetät palautteen |
| Lähetät treffikutsun | −{{petals.set_cost}}, kun painat **Löydä treffit** |
| Kutsusi hylätään | +{{petals.refund}} takaisin |
| Kutsuusi ei vastata {{invitation.answer_hours}} tunnissa, ja se raukeaa | +{{petals.refund}} takaisin |
| Kutsumasi ihminen peruu sovitut treffit | +{{petals.refund}} takaisin |
| Sopivia ehdokkaita on alle {{candidates.per_set}} | Kipinät pysyvät tallessa, ellet jatka silti |
| Peruutat kutsusi ennen kuin toinen vastaa | Ei palautusta |
| Et kutsu ketään löytämistäsi ehdokkaista | Ei palautusta |
| Perut sovitut treffit | Ei palautusta |

Palautuksessa saat takaisin kutsuun kuluneet {{petals.refund}} kipinää.

Treffeistä saat kipinät, kun olet täyttänyt treffipalautteen.

## Kalenterin kipinät

Mitä pidempään vapaa aika on merkittynä, sitä enemmän kipinöitä kertyy. {{calendar.petal_week_hours}} tuntia viikon ajan tuo yhden kipinän. Saman verran tuo esimerkiksi {{calendar.counted_hours_cap}} tuntia vajaassa kahdessa päivässä. Saat kipinöitä yksi kerrallaan sitä mukaa kuin ne kertyvät.

- Mukaan lasketaan tulevat ajat siltä osin kuin ne osuvat seuraavan {{calendar.earning_horizon_days}} päivän sisälle.
- Kerrallaan lasketaan enintään {{calendar.counted_hours_cap}} tuntia, joten viikossa kalenterista kertyy enintään {{calendar.max_petals_per_week}} kipinää.
- Aika, jonka merkitset ja poistat heti perään, ei kerrytä mitään.

### Esimerkkejä

| Kalenterissasi | Kipinöitä |
| --- | --- |
| Lauantai klo 18–22 (4 tuntia), merkitty viikkoa ennen | noin 0,4 |
| Sama lauantai merkittynä 20 päivää ennen nykyhetkeä. Kipinöiden kertyminen alkaa, kun lauantaihin on {{calendar.earning_horizon_days}} päivää | noin 0,8 |
| Noin 10 tuntia viikossa, aina kaksi viikkoa eteenpäin merkittynä | noin 2 viikossa |
| Koko ajan vähintään {{calendar.counted_hours_cap}} tuntia seuraavan {{calendar.earning_horizon_days}} päivän aikana | {{calendar.max_petals_per_week}} viikossa |

## Yläraja

Kipinöitä voi olla kerrallaan enintään {{petals.cap}}, mikä riittää {{petals.cap_roses}} kutsuun. Kun raja täyttyy, uudet kipinät jäävät odottamaan. Voit saada niitä lisää, kun lähetät kutsun ja tilaa vapautuu. Kun kipinät ovat täynnä, lähetä kutsu!

Esimerkiksi: sinulla on {{petals.cap}} kipinää, ja kalenterisi kerryttää viikossa kaksi lisää. Saat ne, kun lähetät kutsun ja tilaa vapautuu.

Palautetut kipinät tulevat perille rajasta riippumatta, joten kipinöitä voi joskus olla yli {{petals.cap}}.

## Milloin kipinät kuluvat

![Treffikutsun viimeinen vaihe: kipinöiden määrä ja Löydä treffit -painike](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Ennen kutsua näet kipinäsi (1). Kun painat **Löydä treffit** (2), {{petals.set_cost}} kipinää kuluu heti. Sitten näet {{candidates.per_set}} ehdokasta ja valitset, kenet kutsut.

Jos sopivia ehdokkaita on alle {{candidates.per_set}}, kipinäsi pysyvät tallessa. Sovellus kertoo, montako löytyi, ja jos painat **Jatka silti**, kipinöitä kuluu tavalliset {{petals.set_cost}}. Jos et kutsu ketään löytämistäsi ehdokkaista, kipinöitä ei palauteta. Ehdokkaat odottavat sinua {{candidates.set_hours}} tuntia. Katso [Ketä sinulle näytetään](/ohje/ehdokkaat).
