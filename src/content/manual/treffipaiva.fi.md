---
title: Treffipäivä
lead: Miten löydätte toisenne perillä, mitä turvapainike lähettää, ja mitä teet, jos toinen ei tule.
order: 70
draft: true
---

![Sovitut treffit: ajankohta, paikka ja Löydättekö toisenne? -kartta](shot:date#agreed-time,live-map)

Treffisivulla on sovittu ajankohta (1), paikka ja kartta (2). Muistutus tulee {{date.reminder_hours}} h ennen treffejä, jos se on päällä asetuksissa.

## Toisen löytäminen perillä

Voit näyttää sijaintisi treffikumppanillesi kartalla, jotta löydätte toisenne. Se on vapaaehtoista.

- **Milloin.** {{sharing.lead_minutes}} minuuttia ennen treffien alkua ja {{sharing.trail_minutes}} minuuttia alun jälkeen. Kun aika alkaa, saat ilmoituksen.
- **Missä.** Vain noin {{sharing.radius_m}} metrin päässä treffipaikasta. Kauempaa lähetettyä sijaintia ei hyväksytä, joten sinua ei voi paikantaa kotoa.
- **Kenelle.** Vain treffikumppanillesi. Hän saa ilmoituksen, kun olet paikalla.
- **Kuinka kauan.** Sijainti on palvelimella vain näyttämisen ajan. Se poistetaan heti, kun lopetat näyttämisen tai aika loppuu. Talteen jää vain tieto siitä, että sijaintia näytettiin.

![Treffipaikan kartta ja Näytä sijaintini -painike](shot:date-map#meet-up-reveal)

Näyttäminen alkaa kartan painikkeesta **Näytä sijaintini** (1). Se päivittyy itsestään, vaikka puhelin olisi taskussa, ja päättyy, kun aika loppuu tai kun painat **Lopeta sijainnin näyttäminen**.

![Kysymys Näytetäänkö sijaintisi? ja sen selitys](shot:date-location-consent)

Ennen kuin mitään näytetään, sovellus kertoo vielä, mitä tapahtuu, ja kysyy luvan.

## Turvapainike

**Turvapainike** näkyy treffisivulla, jos olet tallentanut asetusten kohtaan **Turvallisuus** luotettavan henkilön puhelinnumeron. Ilman numeroa painiketta ei ole, joten tallenna se etukäteen ja sovi asiasta hänen kanssaan.

Yksi painallus lähettää hänelle tekstiviestin: *Pilke: [nimesi] painoi turvapainiketta ja pyytää sinua ottamaan yhteyttä.* Viestissä ei ole sijaintiasi, treffipaikkaa, kellonaikaa eikä mitään treffikumppanistasi. Treffikumppanisi ei saa tietää painalluksesta. Pilke kirjaa, että painoit painiketta ja menikö viesti perille.

Näytöllä lukee, lähtikö viesti. Jos ei, soita läheisellesi itse. Hätätilanteessa soita 112.

## Jos toinen ei tule

Sovelluksessa ei ole keskusteluyhteyttä, joten toinen ei voi ilmoittaa myöhästyvänsä. Jos jäät odottamaan yksin, voit kertoa siitä meille, mutta vain treffien aikana ja treffipaikalla:

- **Milloin.** Aikaisintaan {{noshow.grace_minutes}} minuuttia sovitun alkamisajan jälkeen ja viimeistään, kun treffit päättyvät, {{date.length_hours}} tunnin kuluttua alusta. Ensimmäiset minuutit jättävät tilaa pienelle myöhästymiselle.
- **Missä.** Noin {{noshow.venue_radius_m}} metrin päässä treffipaikasta. Ilmoitus maksaa toiselle pitkän tauon yhden ihmisen sanan perusteella, ja paikan päällä tehtynä se kertoo illasta sellaisena kuin se oli. Puhelin tarkistaa sijaintisi sillä hetkellä, kun ilmoitat, eikä sitä tallenneta.

Näin ilmoitat:

1. Pysy treffipaikalla.
2. Treffisivulle ilmestyy kohta **Jäitkö odottamaan yksin?**. Kun alkamisajasta on kulunut {{noshow.grace_minutes}} minuuttia, paina **Kerro, ettei toinen saapunut**.
3. Vahvista painamalla **Kerro meille**.

![Ilmoitusta ei voi tehdä, koska et ole treffipaikalla](shot:date-noshow-not-at-venue#no-show-report)

Jos et ole treffipaikalla, ilmoitusta ei tehdä, ja sovellus kertoo sen (1).

Kerran tehtyä ilmoitusta ei voi perua. Emme kysy sinulta enää palautetta näistä treffeistä. Toinen ei näy muiden ehdokkaissa eikä voi hakea uusia ehdokkaita {{cooldown.noshow_days}} päivään, ja hän näkee Treffit-sivulla, että hänestä on tehty ilmoitus. Jos hänkin kertoo treffien aikana treffipaikalta, ettet sinä saapunut, kumpaakaan ei rangaista ja Pilkkeen työntekijä käy tapauksen läpi.

## Kysyttyä

**Mitä tapahtuu, kun kutsu hyväksytään?** Treffit on sovittu. Valittu aika varataan teiltä molemmilta, muut tarjotut ajat vapautuvat, ja kutsuja saa ilmoituksen. Treffit näkyvät Treffit-sivulla kohdassa **Sovitut treffit**.

**Voiko aikaa tai paikkaa muuttaa jälkikäteen?** Ei. Jos sovittu ei käy, peru treffit, ja siitä seuraa jäähdytys. Katso [Peruminen ja jäähdytys](/ohje/peruminen-ja-jaahdytys).

**Myöhästyn. Voinko kertoa siitä?** Et. Mene paikalle niin pian kuin pääset. Ensimmäiset {{noshow.grace_minutes}} minuuttia jättävät tilaa pienelle myöhästymiselle.

**En löydä toista paikan päältä.** Näytä sijaintisi kartalla. Toinen saa ilmoituksen, kun olet paikalla, ja näkee sinut kartalla.

**Kauanko treffit kestävät?** Pilkkeen kannalta {{date.length_hours}} tunnin alkamisajasta. Sen jälkeen voit antaa palautetta. Katso [Treffien jälkeen](/ohje/treffien-jalkeen). Te päätätte itse, kauanko olette yhdessä.

**Kuka näkee, missä olen?** Vain treffikumppanisi, vain jos itse näytät sijaintisi ja vain {{sharing.window_minutes}} minuutin ajan treffien alun ympärillä. Luotettava läheisesi ei näe sijaintiasi.
