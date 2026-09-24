---
title: Saapumatta jääminen
lead: Jos toinen ei tule treffeille, voit kertoa siitä treffien aikana, treffipaikalla. Näin ilmoitus toimii molemmille.
kind: explainer
order: 40
draft: true
---

Sovelluksessa ei ole keskusteluyhteyttä, joten toinen ei voi ilmoittaa myöhästyvänsä. Hän tulee paikalle ja odottaa. Siksi saapumatta jääminen on ainoa asia treffien kulusta, josta voit kertoa meille jo treffien aikana.

## Milloin ilmoituksen voi tehdä

Ilmoituksen voi tehdä vain treffien aikana:

- aikaisintaan, kun sovitusta alkamisajasta on kulunut {{noshow.grace_minutes}} minuuttia
- viimeistään, kun treffit päättyvät. Pilkkeen kannalta treffit kestävät {{date.length_hours}} tunnin alkamisajasta.

Pieni myöhästyminen ei ole vielä saapumatta jäämistä. Siksi ensimmäiset minuutit on jätetty pois.

Kun treffit ovat päättyneet, ilmoitusta ei voi enää tehdä. Sovellus kertoo silloin: *Aika kertoa näistä treffeistä on mennyt.*

## Missä ilmoituksen voi tehdä

Ilmoituksen voi tehdä vain treffipaikalla. Kun painat **Kerro meille**, puhelin katsoo sijaintisi, ja sitä verrataan treffipaikkaan. Jos olet yli {{noshow.venue_radius_m}} metrin päässä, ilmoitusta ei tehdä, ja sovellus kertoo: *Kertoa voi vain treffipaikalla.*

**Sijaintia ei tallenneta.** Sitä verrataan treffipaikkaan sillä hetkellä, kun painat, eikä sitä kirjoiteta mihinkään talteen.

Tarkistus on eri asia kuin sijainnin näyttäminen kartalla. Sinun ei tarvitse näyttää sijaintiasi toiselle voidaksesi tehdä ilmoituksen, eikä näyttämisestä ole ilmoitukselle apua.

Tarkistus tarvitsee tarkan sijainnin. Jos sovellus ei saa käyttää sijaintia tai saa vain likimääräisen sijainnin, se kertoo sen ja neuvoo muuttamaan puhelimen asetuksia.

## Mitä ilmoituksesta seuraa

Ilmoitus tehdään kerran, eikä sitä voi perua. Emme sen jälkeen kysy sinulta palautetta näistä treffeistä.

Toinen osapuoli ei näy muiden ehdokkaissa eikä voi hakea uusia ehdokkaita {{cooldown.noshow_days}} päivään. Katso [Jäähdytys](/ohje/jaahdytys).

## Jos sinusta on tehty ilmoitus

Niin kauan kuin voit vastata, Treffit-sivulla näkyy ilmoitus: *Toinen osapuoli on kertonut, ettet saapunut sovittuihin treffeihin.* Kun avaat treffit, niissä lukee **Sinusta on tehty ilmoitus**.

Jos olit paikalla etkä löytänyt toista, voit kertoa, ettei hän itse saapunut. Paina treffisivulla **Kerro, ettei toinen saapunut**. Samat säännöt pätevät: ilmoituksen voi tehdä vain treffien aikana ja treffipaikalla.

Kun treffit ovat päättyneet, vastata ei enää voi. Treffisivulla lukee silloin *Aika vastata on jo mennyt.*

## Kun molemmat kertovat saman

Säännöt ovat samat molemmille. Jos kumpikin kertoo, ettei toinen saapunut:

- kumpaakaan ei rangaista
- jo alkanut jäähdytys poistuu
- Pilkkeen työntekijä käy tapauksen läpi.

Molemmat näkevät tekstin: *Kun kertomukset ovat näin ristiriidassa, kumpaakaan ei rangaista, ja ihminen käy tapauksen läpi.*

Ei ole väliä, kumpi kertoi ensin.

## Miksi näin

Ilmoitus maksaa toiselle {{cooldown.noshow_days}} päivän tauon yhden ihmisen sanan perusteella. Kun sen voi tehdä vain treffipaikalla ja treffien aikana, se kertoo illasta sellaisena kuin se oli, eikä sitä voi tehdä kotoa jälkikäteen.
