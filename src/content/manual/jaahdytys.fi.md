---
title: Jäähdytys
lead: Jos perut sovitut treffit, peruutat kutsun tai et saavu paikalle, Pilke pitää lyhyen tauon. Näin se toimii.
kind: explainer
order: 30
draft: true
---

Jäähdytys on tauko, joka seuraa teosta, joka maksoi toiselle jotain: varatun illan tai odottamisen. Se ei vie terälehtiä, eikä se ole rangaistus vastauksesta. Kutsun hylkääminen ei koskaan aiheuta jäähdytystä.

Jäähdytyksellä on kaksi vaikutusta, ja ne voivat olla voimassa yhdessä tai erikseen:

- **Et näy muiden ehdokkaissa.** Kukaan ei voi saada sinua valikoimaansa.
- **Et voi hakea uusia ehdokkaita.** Et voi avata uutta valikoimaa.

## Mitä näet

Jäähdytyksen aikana Treffit-sivun yläosassa on ilmoitus. Siinä kerrotaan, mikä on voimassa, mihin asti ja miksi. Sama teksti näkyy Ehdokkaat-näkymässä, jos yrität hakea ehdokkaita.

![Ilmoitus: et näy muiden ehdokkaissa etkä voi hakea uusia ehdokkaita](shot:cooldown-blocked#cooldown-notice)

**Molemmat voimassa.** *Et näy juuri nyt muiden treffiehdokkaissa etkä voi hakea uusia ehdokkaita … asti.* Tämä seuraa, kun perut sovitut treffit tai kun toinen kertoo, ettet saapunut.

![Ilmoitus: et voi hakea uusia ehdokkaita](shot:cooldown-nodraw#cooldown-notice)

**Et voi hakea.** *Et voi hakea uusia ehdokkaita … asti.* Tämä seuraa, kun peruutat lähettämäsi kutsun ennen kuin toinen on vastannut. Näyt silti muiden ehdokkaissa.

![Ilmoitus: et näy muiden ehdokkaissa](shot:cooldown-hidden#cooldown-notice)

**Et näy.** *Et näy juuri nyt muiden treffiehdokkaissa … asti.* Sovelluksessa on sääntö, joka voi piilottaa käyttäjän, jonka saamia kutsuja jää toistuvasti hyväksymättä. Sääntö ei ole tällä hetkellä käytössä, joten kutsujen hylkääminen tai vastaamatta jättäminen ei piilota sinua.

Jos voimassa on useampi jäähdytys, ilmoitus kertoo pisimpään kestävän syyn ja päättymisajan.

## Kuinka kauan

| Mitä teit | Kesto |
|---|---|
| Peruutit lähettämäsi kutsun | {{cooldown.withdrawal_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_long_notice_days}} päivää ennen | {{cooldown.cancel_long_notice_hours}} tuntia |
| Peruit sovitut treffit vähintään {{cooldown.cancel_short_notice_hours}} tuntia ennen | {{cooldown.cancel_short_notice_days}} päivää |
| Peruit sovitut treffit myöhemmin | {{cooldown.cancel_late_days}} päivää |
| Toinen kertoi, ettet saapunut | {{cooldown.noshow_days}} päivää |

Jos perut treffejä toistuvasti, kesto kasvaa. Jokainen aiempi jäähdytykseen johtanut peruminen viimeisen {{cooldown.repeat_window_days}} päivän ajalta kertoo seuraavan keston {{cooldown.repeat_multiplier}}:lla. Yksikään jäähdytys ei kuitenkaan kestä yli {{cooldown.ceiling_days}} päivää.

Mitä aikaisemmin perut, sitä lyhyempi tauko on. Peru siis heti, kun tiedät ettet pääse.

## Mitä jäähdytys ei tee

- Se ei vie terälehtiä.
- Sovitut treffisi ja avoimet kutsusi pysyvät ennallaan.
- Voit edelleen vastata saamiisi kutsuihin ja käydä treffeillä.
- Se päättyy itsestään ilmoitetulla hetkellä.

Jos toinen kertoo, ettet saapunut, ja sinä kerrot saman hänestä, kumpaakaan ei rangaista, ja jäähdytyksesi poistuu. Katso [Saapumatta jääminen](/ohje/saapumatta-jaaminen).

## Pysyvä esto

Jäähdytys on aina väliaikainen. Ainoa pysyvä esto syntyy turvallisuusilmoituksesta: jos jompikumpi teistä kertoo treffien jälkeen, että olo oli turvaton, teitä ei enää ehdoteta toisillenne. Se ei vaikuta siihen, näytkö muiden ehdokkaissa.
