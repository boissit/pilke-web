---
title: Treffipäivä
lead: Miten löydätte toisenne treffipaikalla ja mitä tehdä, jos toinen ei saavu paikalle.
order: 70
draft: false
---

![Sovitut treffit: ajankohta, paikka ja Löydättekö toisenne? -kartta](shot:date#agreed-time,live-map..date-map-directions)

Treffisivulla näet sovitun ajan (1), paikan ja kartan (2). Saat muistutuksen {{date.reminder_hours}} tuntia ennen treffejä, jos muistutukset ovat päällä.

## Toisen löytäminen perillä

Kartalla voit jakaa sijaintisi treffikumppanillesi, niin löydätte toisenne helpommin. Jakaminen on vapaaehtoista.

- **Milloin.** {{sharing.lead_minutes}} minuuttia ennen treffien alkua ja {{sharing.trail_minutes}} minuuttia alun jälkeen. Saat ilmoituksen, kun jakaminen on mahdollista.
- **Missä.** Enintään noin {{sharing.radius_m}} metrin päässä treffipaikasta.
- **Kenelle.** Vain treffikumppanillesi. Hän saa ilmoituksen, kun olet paikalla.
- **Kuinka kauan.** Sijaintisi näkyy toiselle korkeintaan {{sharing.trail_minutes}} minuuttia treffien alkamisen jälkeen, tai kunnes päätät itse lopettaa jakamisen.

![Treffipaikan kartta ja Jaa sijaintini -painike](shot:date-map#meet-up-reveal)

Aloita jakaminen kartan painikkeesta **Jaa sijaintini** (1).

![Kysymys Jaetaanko sijaintisi? ja sen selitys](shot:date-location-consent)

Ennen jakamista sovellus kysyy lupaasi.

![Kartta, kun jaatte molemmat sijaintianne: molempien nastat, treffikumppanin sijainnin päivitysaika ja Lopeta sijainnin jakaminen -painike](shot:date-map-sharing#meet-up-stop)

Kun jaat sijaintiasi, näet kartalla itsesi ja treffipaikan. Jos treffikumppanisikin jakaa sijaintinsa, näet myös hänet, ja kartan alla lukee, milloin hänen sijaintinsa päivittyi viimeksi. Sinun sijaintisi päivittyy automaattisesti, vaikka puhelin olisi taskussa. Jakaminen päättyy, kun aika loppuu tai painat **Lopeta sijainnin jakaminen** (1).

## Jos toinen ei tule paikalle

Jos treffiparisi ei saavu paikalle, voit kertoa siitä meille. Ilmoituksen voi tehdä vain treffien aikana ja treffipaikalla:

- **Milloin.** Aikaisintaan {{noshow.grace_minutes}} minuuttia sovitun alkamisajan jälkeen ja viimeistään, kun treffit päättyvät {{date.length_hours}} tunnin kuluttua alusta. Odotusaika jättää tilaa pienelle myöhästymiselle.
- **Missä.** Enintään noin {{noshow.venue_radius_m}} metrin päässä treffipaikasta. Puhelin tarkistaa sijaintisi ilmoitushetkellä, eikä sijaintia tallenneta.

Näin ilmoitat:

1. Pysy treffipaikalla.
2. Treffisivulla on kohta **Jäitkö odottamaan yksin?** Kun alkamisajasta on kulunut {{noshow.grace_minutes}} minuuttia, paina siinä **Kerro, ettei toinen saapunut**.
3. Vahvista painamalla **Kerro meille**.

![Ilmoitusta ei voi tehdä, koska et ole treffipaikalla](shot:date-noshow-not-at-venue#no-show-report)

Jos et ole treffipaikalla, sovellus kertoo sen (1), eikä ilmoitusta tehdä.

Ilmoitusta ei voi perua. Toinen saa {{cooldown.noshow_days}} päivän jäähyn, jonka aikana hän ei näy muiden ehdokkaissa eikä voi hakea uusia ehdokkaita. Jos hänkin tekee ilmoituksen treffipaikalta treffien aikana, Pilkkeen ylläpito pyrkii selvittämään tapauksen.

Jos et jättänyt ilmoitusta treffipaikalla, kerro asiasta treffien jälkeen palautteessa. Valitse kysymyksessä *Miten treffit sujuivat?* vaihtoehto *Treffit eivät toteutuneet* ja sitten *Treffipari ei tullut paikalle*. Tästä ilmoitetaan Pilkkeen ylläpitäjille, mutta toinen ei saa siitä jäähyä. Palautteesta saat {{sparks.per_date}} kipinää. Katso [Treffien jälkeen](/ohje/treffien-jalkeen#jos-treffit-eivät-toteutuneet).

## Kysyttyä

**Mitä tapahtuu, kun kutsu hyväksytään?** Treffit on sovittu. Valittu aika varataan teiltä molemmilta, ja muut tarjotut ajat vapautuvat. Kutsuja saa ilmoituksen, ja treffit näkyvät Treffit-sivulla kohdassa **Sovitut treffit**.

**Voiko aikaa tai paikkaa muuttaa jälkikäteen?** Ei. Jos sovittu aika tai paikka ei käy, peru treffit. Perumisesta seuraa jäähy. Katso [Peruminen ja jäähy](/ohje/peruminen-ja-jaahy).

**Myöhästyn. Voinko kertoa siitä?** Et. Mene paikalle niin pian kuin pääset. Toinen voi ilmoittaa saapumatta jäämisestä aikaisintaan {{noshow.grace_minutes}} minuuttia alkamisajan jälkeen.

**En löydä toista paikan päältä.** Jaa sijaintisi kartalla. Toinen saa ilmoituksen, kun olet paikalla, ja näkee sinut kartalla.

**Kauanko treffit kestävät?** Niin kauan kuin haluatte. Treffien ohjeistettu kesto on noin {{date.length_hours}} tuntia.

**Kuka näkee, missä olen?** Vain treffikumppanisi ja vain silloin, kun jaat sijaintisi. Jakaminen on mahdollista {{sharing.window_minutes}} minuutin ajan treffien alkamisen aikoihin ja vain treffipaikan läheisyydessä.
