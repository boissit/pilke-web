---
title: Kutsut
lead: Kutsussa on valmiina ajat ja paikat. Toinen valitsee niistä yhden kumpaakin, ja treffit on sovittu.
order: 50
draft: true
---

Lähetät kutsun yhdelle ehdokkaistasi. Kutsuun kului {{petals.set_cost}} kipinää jo silloin, kun painoit **Lähetä treffikutsu!** ja löysit ehdokkaat. Katso [Kipinät](/ohje/kipinat).

## Mitä tarjoat

Valitset kortin yhteisistä ajoista ja paikoista ne, jotka sopivat sinulle. Kutsussa on oltava:

- vähintään {{invitation.min_times_offered}} aika ja vähintään {{invitation.min_venues_offered}} paikka, ja
- vaihtoehto: vähintään {{invitation.choice_threshold}} aikaa tai vähintään {{invitation.choice_threshold}} paikkaa.

Toinen valitsee tarjoamistasi täsmälleen yhden ajan ja yhden paikan. Treffit alkavat valitun ajan alussa ja kestävät Pilkkeen kannalta {{date.length_hours}} tunnin.

![Saapunut treffikutsu: tarjotut ajat, paikat ja painikkeet Hylkää ja Sovittu!](shot:invitation#timeslot-0,venue-0)

Saamassasi kutsussa valitset yhden ajan (1) ja, jos paikkoja on useampi, yhden paikan (2). **Päätä myöhemmin** vain sulkee näkymän: kutsu odottaa, mutta aika kuluu.

## Vastausaika

Kutsuun on vastattava {{invitation.answer_hours}} tunnin kuluessa sen lähettämisestä. Jos et ole vastannut, saat muistutuksen noin {{invitation.expiry_warning_hours}} tuntia ennen kuin kutsu raukeaa, jos muistutukset ovat päällä asetuksissa. Vastaamaton kutsu raukeaa itsestään, ja kutsuja saa siitä ilmoituksen.

## Avoin kutsu varaa ajat

Niin kauan kuin kutsu on avoinna, kaikki sen tarjoamat ajat ovat varattuja teiltä molemmilta. Niitä ei näytetä kummallekaan muiden ehdokkaiden korteissa, eikä kumpikaan voi tarjota niitä toisessa kutsussa. Siksi kalenterisi näyttää ne varattuina, eikä niitä voi muuttaa.

Kun kutsu hyväksytään, vain sovittu aika jää varatuksi ja muut vapautuvat. Kun kutsu hylätään, raukeaa tai peruutetaan, kaikki ajat vapautuvat heti.

![Lähetetty treffikutsu: ehdotetut ajat ja paikat, alhaalla Peruuta kutsu](shot:sent#withdraw-invitation-open)

**Peruuta kutsu** (1) peruu lähettämäsi kutsun: katso alta, mitä siitä seuraa.

## Mitä kutsulle käy

| Loppu | Kutsujalle | Vastaajalle |
|---|---|---|
| **Hyväksytty.** Treffit on sovittu. | Kipinät jäävät käytetyiksi. Saat ilmoituksen. | Ei jäähyä. |
| **Hylätty.** | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.decline_hours}} tuntiin. |
| **Rauennut.** Kukaan ei vastannut {{invitation.answer_hours}} tunnissa. | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.no_answer_hours}} tuntiin. |
| **Peruutettu.** Kutsuja perui ennen vastausta. | Ei palautusta. Et voi löytää uusia ehdokkaita {{cooldown.withdrawal_hours}} tuntiin. | Jos hän oli jo saanut ilmoituksen kutsusta, hän saa ilmoituksen myös peruutuksesta. |

Vastaajan kipinät pysyvät ennallaan, päättyipä kutsu miten tahansa. Ilmoitukset tulevat, jos ne ovat päällä asetuksissa.

Päättyipä kutsu miten tahansa, teitä kahta ei sen jälkeen enää ehdoteta toisillenne. Ainoa poikkeus on, jos kävitte treffeillä ja vastasitte molemmat haluavanne tavata uudelleen.

Sovittujen treffien perumisesta kerrotaan sivulla [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).
