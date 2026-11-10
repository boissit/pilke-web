---
title: Kutsut
lead: Kutsussa on valmiina ajat ja paikat. Toinen valitsee niistä yhden ajan ja yhden paikan, ja treffit on sovittu.
order: 50
draft: true
---

Kutsu lähtee yhdelle ehdokkaistasi. Sen {{petals.set_cost}} kipinää kului jo, kun painoit **Löydä treffit**. Katso [Kipinät](/ohje/kipinat).

## Mitä tarjoat

Valitse kortin yhteisistä ajoista ja paikoista ne, jotka sopivat sinulle. Kutsussa on oltava vähintään {{invitation.min_times_offered}} aika ja vähintään {{invitation.min_venues_offered}} paikka. Lisäksi siinä on oltava vähintään {{invitation.choice_threshold}} aikaa tai {{invitation.choice_threshold}} paikkaa, jotta toinen voi valita.

Toinen valitsee tarjoamistasi yhden ajan ja yhden paikan. Treffit alkavat valitun ajan alussa, ja sovelluksessa ne kestävät {{date.length_hours}} tuntia.

![Saapunut treffikutsu: tarjotut ajat, paikat ja painikkeet Hylkää ja Sovittu!](shot:invitation#timeslot-*,venue-*)

Kun saat kutsun, valitse siitä yksi aika (1) ja, jos paikkoja on useampi, yksi paikka (2). **Takaisin** sulkee näkymän. Kutsu jää odottamaan, mutta vastausaika kuluu.

## Vastausaika

Kutsuun on vastattava {{invitation.answer_hours}} tunnissa sen lähettämisestä. Noin {{invitation.expiry_warning_hours}} tuntia ennen määräajan loppua saat muistutuksen, jos et ole vielä vastannut ja muistutukset ovat päällä. Vastaamaton kutsu raukeaa itsestään, ja kutsuja saa siitä ilmoituksen.

## Avoin kutsu varaa ajat

Kaikki kutsussa tarjotut ajat ovat varattuja teiltä molemmilta, kunnes kutsu päättyy. Ne eivät näy kummallekaan muiden ehdokkaiden korteissa, eikä kumpikaan voi tarjota niitä toisessa kutsussa. Kalenterissasi ne näkyvät varattuina, etkä voi muuttaa niitä.

Kun kutsu hyväksytään, vain sovittu aika jää varatuksi, ja muut vapautuvat. Kun kutsu hylätään, raukeaa tai peruutetaan, kaikki ajat vapautuvat heti.

![Lähetetty treffikutsu: ehdotetut ajat ja paikat, alhaalla Peruuta kutsu](shot:sent#withdraw-invitation-open)

Lähettämäsi kutsun voit perua painikkeella **Peruuta kutsu** (1). Mitä siitä seuraa, näet alta.

## Mitä kutsulle käy

| Miten kutsu päättyy | Kutsujalle | Kutsutulle |
|---|---|---|
| **Hyväksytty.** Treffit on sovittu. | Kipinät jäävät käytetyiksi. Saat ilmoituksen. | Ei jäähyä. |
| **Hylätty.** | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.decline_hours}} tuntiin. |
| **Rauennut.** Kutsuun ei vastattu {{invitation.answer_hours}} tunnissa. | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.no_answer_hours}} tuntiin. |
| **Peruutettu.** Kutsuja peruutti sen ennen vastausta. | Ei palautusta. Et voi löytää uusia ehdokkaita {{cooldown.withdrawal_hours}} tuntiin. | Jos sait jo ilmoituksen kutsusta, saat ilmoituksen myös peruutuksesta. |

Kutsutun kipinät pysyvät ennallaan, päättyipä kutsu miten tahansa. Ilmoitukset tulevat, jos ne ovat päällä asetuksissa.

Kutsun jälkeen teitä ei enää ehdoteta toisillenne. Poikkeus on, jos kävitte treffeillä ja vastasitte molemmat haluavanne tavata uudelleen.

Sovittujen treffien perumisesta kerromme sivulla [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).
