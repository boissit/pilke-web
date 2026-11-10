---
title: Kutsut
lead: Kutsussa on valmiina ajat ja paikat. Vastaanottaja valitsee niistä yhden ajan ja yhden paikan, ja treffit on sovittu.
order: 50
draft: true
---

## Mitä kutsuun kuuluu

Valitse kortin yhteisistä ajoista ja paikoista ne, jotka sopivat sinulle. Kutsussa on oltava vähintään {{invitation.min_times_offered}} aika ja vähintään {{invitation.min_venues_offered}} paikka. Lisäksi, jotta kutsun vastaanottajalla on valinnanvaraa, kutsussa on oltava joko vähintään {{invitation.choice_threshold}} paikkaa tai aikaa, esimerkiksi 3 aikaa ja 1 paikka, tai 1 aika ja 2 paikkaa.

Vastaanottaja valitsee tarjoamistasi yhden ajan ja yhden paikan. Treffit alkavat valitun ajan alussa, ja treffien ohjeistettu kesto on {{date.length_hours}} tuntia.

![Saapunut treffikutsu: tarjotut ajat, paikat ja painikkeet Hylkää ja Sovittu!](shot:invitation#timeslot-*,venue-*)

Kun saat kutsun, valitse siitä treffien lopullinen aika (1) ja lopullinen paikka (2). **Takaisin** sulkee näkymän, mutta kutsu jää odottamaan ja vastausaika kuluu.

## Vastausaika

Kutsuun on vastattava {{invitation.answer_hours}} tunnissa sen lähettämisestä. Noin {{invitation.expiry_warning_hours}} tuntia ennen määräajan loppua saat muistutuksen, jos et ole vielä vastannut ja [muistutukset ovat päällä](/ohje/tiedot-ja-tili#ilmoitukset). Vastaamaton kutsu raukeaa itsestään, ja kutsuja saa siitä ilmoituksen.

## Avoin kutsu varaa ajat

Kaikki kutsussa tarjotut ajat ovat varattuja teiltä molemmilta, kunnes kutsu päättyy. Ne eivät näy kummallekaan muiden ehdokkaiden korteissa, eikä kumpikaan voi tarjota niitä toisessa kutsussa. Kalenterissasi ne näkyvät varattuina, etkä voi muuttaa niitä.

Kun kutsu hyväksytään, vain sovittu aika jää varatuksi, ja muut vapautuvat. Kun kutsu hylätään, raukeaa tai peruutetaan, kaikki ajat vapautuvat heti.

![Lähetetty treffikutsu: ehdotetut ajat ja paikat, alhaalla Peruuta kutsu](shot:sent#withdraw-invitation-open)

Lähettämäsi kutsun voit perua painikkeella **Peruuta kutsu** (1).

## Mitä kutsulle käy

| Miten kutsu päättyy | Kutsujalle | Kutsutulle |
|---|---|---|
| **Hyväksytty.** Treffit on sovittu. | Kipinät jäävät käytetyiksi. Saat ilmoituksen. | Ei jäähyä. |
| **Hylätty.** | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.decline_hours}} tuntiin. |
| **Rauennut.** Kutsuun ei vastattu {{invitation.answer_hours}} tunnissa. | {{petals.refund}} kipinää palaa sinulle. Saat ilmoituksen. | Et voi löytää uusia ehdokkaita {{cooldown.no_answer_hours}} tuntiin. |
| **Peruutettu.** Kutsuja peruutti sen ennen vastausta. | Ei palautusta. Et voi löytää uusia ehdokkaita {{cooldown.withdrawal_hours}} tuntiin. | Jos sait jo ilmoituksen kutsusta, saat ilmoituksen myös peruutuksesta. |

Kutsun jälkeen teitä ei enää ehdoteta toisillenne. Poikkeuksena on, jos kävitte treffeillä ja vastasitte molemmat haluavanne tavata uudelleen Pilkkeen kautta.

Sovittujen treffien perumisesta kerromme sivulla [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).
