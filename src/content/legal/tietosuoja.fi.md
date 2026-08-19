---
title: Tietosuojaseloste
lead: Mitä tietoja Pilke kerää, mihin niitä käytetään ja mitä voit vaatia.
version: 2026-09-01
effective: 2026-09-01
draft: true
---

> **Ohje kirjoittajalle.** Tämä on luonnos. Rakenne ja kieliasu seuraavat suomalaista
> käytäntöä (Wolt Oy:n tietosuojaseloste) ja deittipalvelun omat kohdat Tinderin
> suomenkielistä selostetta; **sisältö on kirjoitettu Pilkkeen omasta koodista**
> `docs/legal/privacy-policy.md`-auditin kautta, ei kopioitu kummastakaan. Jokainen
> `TODO(legal)` on omistajan tai lakimiehen päätös, jota ei voi lukea koodista — älä
> täytä niitä sillä, mitä deittisovellus tavallisesti sanoo. Kun lakimies on lukenut
> valmiin tekstin, poista `draft: true` ja tämä huomautus.

## 1. Rekisterinpitäjä ja yhteystiedot

Henkilötietojesi rekisterinpitäjä on **[TODO(legal): yhtiön virallinen nimi, y-tunnus ja
osoite]**, joka tarjoaa Pilke-sovelluksen.

Tietosuojaa koskevissa asioissa voit ottaa meihin yhteyttä osoitteessa
**[TODO(legal): sähköpostiosoite — ilman tätä selostetta ei voi julkaista, ks. tietosuoja-asetuksen 13 artikla]**.

**[TODO(legal): onko tietosuojavastaava nimetty? Jos on, nimi ja yhteystiedot tähän.]**

## 2. Keitä tämä seloste koskee

Tämä seloste koskee sinua, jos käytät Pilkettä. Se koskee myös kahta ihmistä, jotka
eivät itse käytä sovellusta:

- **Luotettava henkilö**, jonka puhelinnumeron olet tallentanut turvatoimintoa varten.
  Numero on hänen tietonsa, ei sinun, ja siksi se ei näy kenellekään muulle.
- **Ihminen, josta joku muu kirjoittaa turvallisuusilmoituksen.** Ilmoituksen kohde ei
  ole kirjoittanut sitä eikä ole voinut estää sitä.

## 3. Mitä tietoja käsittelemme

### 3.1 Tili ja profiili

| Tieto | Tarkemmin |
| --- | --- |
| Puhelinnumero | Tunnistat itsesi sillä. Tilillä ei ole salasanaa. |
| Sähköpostiosoite | Kysytään rekisteröityessä. |
| Nimimerkki | Näkyy muille käyttäjille. |
| Syntymäaika | Tallennamme päivän, mutta muille näytetään vain ikä. |
| Sukupuoli | Näkyy muille käyttäjille. |
| Valokuva | Näkyy muille käyttäjille. |
| Kieli | Suomi tai englanti. Ratkaisee, millä kielellä ilmoitukset ja tekstiviestit tulevat. |
| Luotettavan henkilön puhelinnumero | Vapaaehtoinen. Ei näy kenellekään muulle kuin sinulle. |
| Treffitoiveet | Kenestä olet kiinnostunut, minkälaisia treffejä haet, ikähaarukka ja kielet. |
| Treffialue | Kartalta valitsemasi piste ja säde kilometreinä. Et kerro meille, missä asut. |
| Rekisteröitymisen ajankohta ja tilin tila | |

Treffitoiveisiin kuuluu myös se, haetko seksiä. **[TODO(legal): lakimiehen arvio siitä,
onko tämä yhdessä sukupuolen ja toivottujen sukupuolten kanssa tietosuoja-asetuksen 9
artiklan erityinen henkilötietoryhmä, ja mitä siitä seuraa tälle selosteelle.]**

### 3.2 Kirjautuminen

Kirjautumiskoodi on kuusi numeroa, se on voimassa viisi minuuttia ja se lakkaa
toimimasta viidennen väärän arvauksen jälkeen. Jokaisesta kirjautuneesta laitteesta
jää oma rivi, ja siitä tallennetaan vain istuntotunnuksen tiiviste — ei tunnusta
itseään. Istunto vanhenee, kun sitä ei ole käytetty 90 päivään. Rajoitamme myös sitä,
kuinka usein samaan numeroon voi pyytää koodin.

### 3.3 Kalenteri, treffit ja kipinät

| Tieto | Tarkemmin |
| --- | --- |
| Kalenteri | Ajat, jotka olet merkinnyt vapaiksi. |
| Hyvitetyt ajat | Mistä merkitsemistäsi ajoista olet saanut kipinöitä, myös peruuttamistasi. |
| Ehdokkaat | Kenet järjestelmä on laskenut sinulle mahdolliseksi treffikumppaniksi. |
| Ehdokasnostot | Ketkä sinulle on tarjottu ja kenet valitsit. |
| Treffit ja kutsut | Osapuolet, ehdotettu ja sovittu aika, paikka, tila, sekä kuka perui ja millä syyllä. |
| Kipinätilikirja | Jokainen kipinöiden liike syineen. |
| Hidastukset | Seuraukset, joita parhaillaan kannat, ja niiden syy. |
| Estot | Parit, joita ei enää koskaan ehdoteta toisilleen. |

### 3.4 Kysymyssarjat ja palautteet

Vastaat kysymyssarjoihin valitsemalla vaihtoehdon; vapaata tekstiä ei voi kirjoittaa.
Sama koskee treffien jälkeistä palautetta: vastaus on valinta, ei teksti.

⚠️ **Kysymyssarjojen vastaukset eivät tällä hetkellä vaikuta siihen, keitä sinulle
ehdotetaan.** Keräämme ne, mutta ehdokkaita rajaavat sukupuoli, ikä, treffityyppi,
alue, kalenteri, hidastukset ja estot.

### 3.5 Ilmoitukset ja laitteet

Jokaisesta laitteesta tallennetaan push-tunniste, alusta ja se, milloin tunniste on
viimeksi rekisteröity. Tunniste päivitetään jokaisella sovelluksen käynnistyksellä.
Tallennamme myös jonon jokaisesta lähetetystä ilmoituksesta: mistä se kertoo, mihin
treffeihin se liittyy, ja lähetyksen lopputuloksen laitekohtaisesti. **Ilmoituksen
sisällössä on usein toisen osapuolen nimimerkki.**

### 3.6 Turvallisuustiedot

- **Turvallisuusilmoitus** ja sen vapaa teksti. Tämä on ainoa paikka koko palvelussa,
  johon voi kirjoittaa vapaata tekstiä toisesta ihmisestä.
- **Ilmoitus saapumatta jättämisestä**, molempiin suuntiin.
- **Merkintä turvapainikkeen painamisesta**, ja kenelle viesti lähti.
- **Esto**, joka syntyy kun joku peruu treffit siksi, ettei kokenut oloaan
  turvalliseksi. Syytä ei kerrota toiselle osapuolelle.

### 3.7 Mitä emme kerää

Tämä kannattaa sanoa ääneen, koska se on poikkeuksellista:

- Ei analytiikkaa eikä mainostunnisteita.
- Ei evästeitä. Pilke ei ole verkkosivu, ja tämä sivusto ei aseta evästeitä.
- Ei kaatumisraportointia.
- Ei chattia. Käyttäjät eivät voi lähettää toisilleen viestejä lainkaan.
- Emme kysy kotiosoitettasi emmekä lue laitteesi sijaintia muulloin kuin luvussa 4.2
  kuvatulla tavalla.

**[TODO(legal): mitä palvelinten ja verkkoinfrastruktuurin lokit tallentavat, esimerkiksi
IP-osoitteet ja kuinka kauan. Sovellus itse ei kirjoita niitä, mutta konesali kirjoittaa.]**

## 4. Sijainti

Sanalla sijainti on Pilkkeessä kaksi täysin eri merkitystä, eikä niitä voi kuvata
yhdessä.

### 4.1 Treffialue — ei laitteen sijainti

Valitset kartalta pisteen ja säteen: kuinka kauas voisit lähteä treffeille. Se on sinun
itse asettamasi, se ei tule mistään anturista, ja sen perusteella päätämme mitkä
treffipaikat ovat ulottuvillasi ja kenet voimme ehdottaa sinulle. **Se ei näy muille
käyttäjille.** Voit muuttaa sitä asetuksissa milloin tahansa, ja se poistetaan kun
poistat tilisi.

### 4.2 Sijainnin näyttäminen treffipaikalla

Kun treffit ovat alkamassa, voit näyttää sijaintisi sille, jonka kanssa olet menossa
treffeille. Tarkoitus on yksi: kaksi toisilleen tuntematonta ihmistä löytävät toisensa
baarin edestä.

**Sijainti on tarkka.** Se ei ole sumennettu, karkeistettu eikä likiarvo, vaan noin
metrin tarkkuudella se, missä puhelimesi on. Emme kerro tarkkuutta suojana, koska se ei
ole suoja. Suojia on viisi, ja ne ovat tässä:

1. **Treffien pitää olla sovittu ja niillä pitää olla paikka.** Muuten toimintoa ei ole.
2. **Aikaikkuna on kaksikymmentä minuuttia** — kymmenen minuuttia sovitun alun
   molemmin puolin. Se ei liity siihen, milloin treffit loppuvat. Ikkunan ulkopuolella
   sijaintia ei voi näyttää eikä katsoa.
3. **Enintään 300 metriä treffipaikasta.** Puhelimesi tarkistaa tämän ennen kuin lähettää
   mitään, ja palvelin tarkistaa sen uudelleen. Sohvalta yritetty sijainti ei siis lähde
   laitteeltasi lainkaan.
4. **Yksi vastaanottaja:** se, jonka kanssa olet menossa treffeille. Kukaan muu käyttäjä
   ei näe sitä, ja sitä ei ole viety ylläpidon näkymiin.
5. **Poistaminen.** Rivi poistetaan, kun ikkuna sulkeutuu; tätä tekee minuutin välein
   ajettava työ, joten todellinen elinikä on enintään noin 21 minuuttia. Kun lopetat
   näyttämisen itse, rivi poistetaan heti — eikä siitä jää merkintää. Puuttuvaa sijaintia
   ei voi erottaa siitä, ettet olisi koskaan näyttänyt sitä.

Sijaintia ei käytetä mihinkään muuhun. Mikään seuraus, ilmoitus tai hyvitys ei lue sitä.

Näyttäminen jatkuu, vaikka poistut näkymästä tai laitat puhelimen taskuun — se on
tarkoitus, ja siksi kerromme sen etukäteen sovelluksessa. Emme pyydä lupaa sijaintiin
taustalla muuten kuin tämän kahdenkymmenen minuutin ajan.

⚠️ **Yksi tarkennus, joka on rehellistä sanoa.** Kun näytät sijaintisi ensimmäisen
kerran, toiselle osapuolelle lähtee ilmoitus, jonka otsikossa on nimimerkkisi. Itse
sijaintia ei ole ilmoituksessa, mutta tieto siitä, että saavuit paikalle, kulkee
push-palvelun ja Googlen kautta (luku 8).

## 5. Mitä muut käyttäjät näkevät sinusta

Toinen käyttäjä näkee **nimimerkkisi, ikäsi, sukupuolesi ja valokuvasi** — ei muuta.
Lisäksi hän näkee valitun treffipaikan ja ajan, tarjoamasi ajat, ja aikaikkunan
sisällä treffipaikalla sijaintisi, jos näytät sen.

Toinen käyttäjä **ei koskaan näe** puhelinnumeroasi, sähköpostiosoitettasi,
syntymäaikaasi, luotettavan henkilön numeroa, treffialuettasi, toiveitasi,
kipinäsaldoasi, hidastuksiasi, palautteitasi eikä ilmoituksia.

## 6. Miksi käsittelemme tietojasi

1. Tilin luonti ja kirjautuminen.
2. Treffiehdokkaiden etsiminen: sukupuoli, ikä, toiveet, alue, kalenteri, hidastukset ja
   estot.
3. Treffien sopiminen ja kulku: kutsut, ajan ja paikan valinta, peruminen.
4. Sen auttaminen, että löydätte toisenne treffipaikalla (luku 4.2).
5. Ilmoitukset kutsuista, saapumisesta ja palautepyynnöistä.
6. Turvallisuus: estot, ilmoitukset, turvapainike ja niistä seuraavat hidastukset.
7. Palvelun reilu käyttö: hidastukset perumisista ja saapumatta jättämisistä, ja
   kipinätalous, joka rajaa kutsujen tahtia.
8. Kysymyssarjat. Keräämme ne nyt; ehdokkaisiin ne eivät vielä vaikuta (luku 3.4).
9. Käyttäjätuki ja väärinkäytösten selvittäminen.

## 7. Käsittelyn oikeusperuste

**[TODO(legal): oikeusperuste jokaiselle luvun 6 tarkoitukselle. Tätä ei voi lukea
koodista, ja väärä arvaus on kallis. Erikseen ratkaistavat kohdat:**

- **ydinpalvelu (1–5): sopimus vai suostumus;**
- **sijainnin näyttäminen (4): erillinen suostumus vai sopimuksen välttämättömyys, jonka
  päällä on vahvistus;**
- **se, mitä yksi käyttäjä kirjoittaa toisesta: kohde ei ole suostunut eikä voi. Oikeutettu
  etu on ilmeinen ehdokas ja vaatii dokumentoidun tasapainotestin;**
- **luotettavan henkilön numero: koodin oletus on, että numeron tallentajalla on lupa
  siihen. Oletus ei ole oikeusperuste;**
- **treffityyppi ja sukupuolitoiveet, jos ne ovat 9 artiklan tietoja (luku 3.1);**
- **turvallisuusilmoituksen vapaa teksti, ja 10 artikla jos se kuvaa rikosta.]**

## 8. Kenelle luovutamme tietoja

**Toisille käyttäjille** luvussa 5 kuvatun verran.

**Luotettavalle henkilöllesi** yksi tekstiviesti, jossa on nimimerkkisi, jos painat
turvapainiketta. Viestissä ei ole sijaintia, treffipaikkaa eikä treffikumppaniasi.

**Push-palvelulle (Expo, 650 Industries, Inc., Yhdysvallat)** laitteesi push-tunniste
sekä ilmoituksen otsikko, teksti ja sisältö. Kolmessa ilmoituslajissa neljästä
sisällössä on toisen osapuolen nimimerkki. Expo välittää ilmoituksen edelleen
**Googlen FCM-palveluun**, joka on siten myös vastaanottaja.
**[TODO(legal): sopimuskumppani, onko käsittelysopimus allekirjoitettu, ja siirron
peruste.]**

**Tekstiviestien välittäjälle (GatewayAPI, Tanska)** vastaanottajan puhelinnumero ja
viestin sisältö. Kaksi lajia: kirjautumiskoodi omaan numeroosi, ja turvaviesti
luotettavan henkilön numeroon. Palvelu on EU:ssa. ⚠️ **Tekstiviestejä ei tällä hetkellä
lähetetä lainkaan mistään ympäristöstä**, koska välittäjää ei ole vielä kytketty.
**[TODO(legal): onko käsittelysopimus allekirjoitettu.]**

**Karttapalvelulle (OpenFreeMap)** laitteesi IP-osoite ja ne karttaruudut, joita se
pyytää — eli mitä aluetta katsot kartalla. Pyyntö lähtee laitteeltasi, ei
palvelimeltamme. Tämä koskee treffialueen valintaa, kutsun karttaa ja treffipaikan
karttaa. **[TODO(legal): palvelun ylläpitäjä, sijaintimaa ja se, onko käsittelysopimus
mahdollinen ilmaisen palvelun kanssa. Jos ei, karttapalvelu on vaihdettava.]**

**Konesalille [TODO(legal): palveluntarjoaja, maa ja käsittelysopimus]**. Kaikki tämän
palvelun henkilötiedot ovat yhdessä tietokannassa, ja valokuvat sen vieressä.

**Pilkkeen työntekijöille** ylläpitonäkymän kautta. Sijaintirivit eivät näy siellä
lainkaan. Ilmoitukset saapumatta jättämisestä ovat vain luettavia, myös meille.
**[TODO(legal): kuinka monella henkilöllä on ylläpito-oikeus.]**

**Google Playlle** se, mitä se sovelluksen jakelijana saa.

Emme myy tietojasi emmekä luovuta niitä markkinointiin.

## 9. Siirto EU:n ulkopuolelle

Push-ilmoitukset kulkevat **Yhdysvaltoihin** (Expo) ja sieltä Googlelle. Tämä on ainoa
siirto, joka varmasti tapahtuu tänään. **[TODO(legal): siirron peruste.]**

Tekstiviestien välittäjä on Tanskassa, eli EU:ssa. Konesalin ja karttapalvelun maat ovat
**[TODO(legal)]**.

## 10. Kuinka kauan säilytämme tietoja

Nämä poistuvat itsestään:

| Tieto | Sääntö |
| --- | --- |
| Näytetty sijainti | Kun aikaikkuna sulkeutuu; poistotyö ajetaan minuutin välein. Myös heti, kun lopetat näyttämisen. |
| Ilmoitus siitä, että olet paikalla | Samalla poistotyöllä, myös jo perille menneet. |
| Kirjautumiskoodi | Korvautuu uudella; lakkaa toimimasta viidessä minuutissa. |
| Taustatöiden tulokset | 7 vuorokautta, epäonnistuneet 30. |

⚠️ **Kaikkea muuta säilytetään tällä hetkellä ilman määräaikaa.** Treffit, kipinöiden
liikkeet, kalenterihyvitykset, hidastukset, estot, ilmoitukset saapumatta jättämisestä,
turvallisuusilmoitukset vapaine teksteineen, turvaviestit, ehdokasnostot ja palautteet
jäävät. Mikään ajastettu työ ei poista niitä.

**[TODO(legal): säilytysaika jokaiselle yllä olevalle ryhmälle. Tietosuoja-asetuksen 5
artiklan 1 kohdan e alakohta vaatii sen, eikä koodissa ole yhtäkään. Kaksi kiireellisintä
ovat turvallisuusilmoituksen vapaa teksti ja pysyvä esto, koska molemmat koskevat ihmistä,
joka ei ole kirjoittanut niitä.]**

## 11. Mitä tapahtuu, kun poistat tilin

Voit poistaa tilisi sovelluksen asetuksista. Poisto tapahtuu heti, sitä ei voi peruuttaa,
eikä sille ole harkinta-aikaa. Kerromme erikseen sivulla
[tietojen poistaminen](/tietojen-poisto), mikä poistuu ja mikä jää.

Lyhyesti: **tilin tiedot pyyhitään, mutta rivi jää.** Puhelinnumero, sähköpostiosoite,
nimimerkki, syntymäaika, sukupuoli, kuva, luotettavan henkilön numero, toiveet ja
treffialue poistetaan, ja kuva poistetaan myös tallennustilasta. Kirjautumiset katkeavat
kaikilta laitteilta samalla hetkellä.

Jää kaksi ryhmää, eikä kumpaakaan voi poistaa:

- **Tiedot, jotka ovat yhtä lailla toisen osapuolen tietoja.** Treffit, palautteet,
  ilmoitukset saapumatta jättämisestä ja turvallisuusilmoitukset. Toinen osapuoli näkee
  sinun tilallasi *Joku*.
- **Turvallisuuspäätökset, joita lähteminen ei saa kumota.** Esto, joka on syntynyt siitä,
  ettei joku kokenut oloaan turvalliseksi, pysyy. Muuten palvelusta lähteminen olisi tapa
  purkaa toisen ihmisen turvallisuuspäätös.

Lisäksi jäävät kipinöiden liikkeet, jotta saldot pysyvät täsmäävinä, ja merkintä siitä,
että tili on ollut olemassa.

Voit rekisteröityä samalla puhelinnumerolla uudelleen. Saat tyhjän tilin, eikä mikään
yhdistä sitä vanhaan.

## 12. Sinun oikeutesi

Sinulla on oikeus

- **saada pääsy tietoihisi**;
- **oikaista** virheelliset tiedot;
- **poistaa** tiedot siltä osin kuin laki sen sallii (luku 11);
- **rajoittaa** käsittelyä;
- **vastustaa** käsittelyä;
- **siirtää tiedot** järjestelmästä toiseen;
- **peruuttaa suostumus**, jos käsittely perustuu siihen;
- **olla joutumatta pelkästään automaattisen päätöksenteon kohteeksi** (luku 15).

Osan näistä voit tehdä itse: profiilisi ja toiveesi näkyvät ja muuttuvat asetuksissa,
sijainnin näyttämisen lopetat yhdellä painalluksella, ja tilin poistat asetuksista.

Rehellisyyden nimissä kaksi rajoitusta, jotka ovat totta tänään:

- **Tietoja ei saa ulos koneellisesti.** Sovelluksessa ei ole vientitoimintoa, joten
  pyyntö hoidetaan käsin.
- **Et näe, mitä joku muu on kirjoittanut sinusta**, eikä sitä voi oikaista. Ilmoitukset
  ovat vain luettavia myös meille.

Pyynnöt osoitetaan luvun 1 yhteysosoitteeseen.
**[TODO(legal): miten pyytäjä tunnistetaan ja missä ajassa vastaamme.]**

## 13. Miten teet valituksen

Jos katsot, että käsittelemme henkilötietojasi tietosuojalainsäädännön vastaisesti, voit
tehdä valituksen tietosuojavaltuutetun toimistolle.

Tietosuojavaltuutetun toimisto, PL 800, 00531 Helsinki. Puhelinvaihde 029 566 6700.
Lisätiedot ja lomakkeet: [tietosuoja.fi](https://tietosuoja.fi/).

Toivomme, että otat ensin yhteyttä meihin, mutta valituksen voi tehdä myös suoraan.

## 14. Tietoturva

Kerromme tässä mitä teemme, emmekä anna takuita.

- **Tilillä ei ole salasanaa.** Kirjautuminen tapahtuu kertakoodilla puhelinnumeroosi.
  Istuntotunnuksesta tallennetaan vain tiiviste, ei tunnusta itseään, ja jokainen laite
  kirjautuu erikseen.
- Puhelimessa istuntotunnus on käyttöjärjestelmän suojatussa säilössä, ja se on rajattu
  pois laitteen varmuuskopioista.
- Ylläpito-oikeudet ovat rajattuja: sijaintirivejä ei näytetä ylläpidossa lainkaan, ja
  ilmoitukset saapumatta jättämisestä ovat vain luettavia.
- ⚠️ **Valokuvat ovat osoitteessa, joka ei vaadi kirjautumista.** Kuvan osoitteen
  tunteva voi hakea sen. **[TODO(legal): korjataanko tämä ennen julkaisua vai kerrotaanko
  se tässä.]**

**[TODO(legal): tässä selosteessa ei sanota mitään salauksesta siirron aikana, koska
Android-sovellus sallii tällä hetkellä myös salaamattoman yhteyden. Poistakaa asetus
ennen julkaisua ja lisätkää lause, tai jättäkää lause pois.]**

## 15. Automaattiset päätökset

Ehdokkaiden etsiminen on automaattista, mutta se tuottaa **ehdotuksen**: kolme ehdokasta,
jotka voit ohittaa.

Automaattisia ja sinulle kielteisiä ovat **hidastukset**. Ne tarkoittavat, ettet näy
muiden ehdokkaissa tai ettet voi nostaa uusia ehdokkaita, ja ne seuraavat perumisista ja
saapumatta jättämisistä.

⚠️ Yksi näistä perustuu **toisen ihmisen sanaan**: jos sinusta tehdään ilmoitus
saapumatta jättämisestä, hidastus tulee automaattisesti ja purkautuu itsestään vain, jos
teet vastailmoituksen vuorokauden sisällä. **[TODO(legal): lakimiehen arvio 22 artiklasta,
ja se, riittääkö vastailmoitus ihmisen tekemäksi arvioksi.]**

Turvallisuusilmoitus ei aiheuta mitään automaattisesti. Sen käsittelee ihminen.

## 16. Muutokset selosteeseen

Jokaisella versiolla on päivämäärä, ja se näkyy tämän sivun alussa. Sovellus näyttää
saman version numeron ehtojen yhteydessä, ja tallennamme sen version, jonka olet
hyväksynyt.

**[TODO(legal): miten muutoksesta kerrotaan, ja pitääkö uusi versio hyväksyä vai
riittääkö että se näytetään. Huomaa, että tilit jotka on luotu ennen ensimmäistä
julkaistua versiota eivät ole hyväksyneet mitään, ja se on tallennettu tyhjänä.]**
