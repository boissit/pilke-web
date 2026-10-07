/**
 * Every string on the site, in both languages.
 *
 * Finnish is the product's language and the one written first; English is a full
 * translation rather than a fallback set, so a key missing from `en` is a type
 * error here in the same way it is in the app's own dictionaries.
 *
 * Product vocabulary is the app's own spelling: the tokens are *kipinät*, one
 * *kipinä*, in English *sparks*, and five of them send a treffikutsu. They are
 * never called a currency: Pilke *pyörii kipinöiden ympärillä*, runs on sparks.
 * A zero balance is never *ei kipinää*, which means no chemistry, and *kipinöitä
 * lentää* belongs to the moment two people say yes. The constants keep their old
 * names, `{{petals.*}}`, because the backend does.
 *
 * The front page argues one thing: the shortest path to meeting somebody is a
 * kutsu with the time already in it. Sparks get one short section there — what
 * they are for and the two ways they build up week to week — and the whole ledger
 * belongs to `nain-se-toimii`, because a full price list on a front page reads as
 * a game to be played rather than as an app for meeting people.
 *
 * The owner's rules for new copy: short, warm, direct and in the second person.
 * A sentence opens with what something is, never with what it is not, and carries
 * no emphatic add-on ("aina", "ei koskaan enempää") and no reassurance nobody
 * asked for. The terms are fixed: *löydä ehdokkaat*, *persoonallisuuskysely*,
 * *kipinät*, *jäähy*, *ylläpidetty kalenteri*.
 *
 * Sentences here are short on purpose. A clause that can be its own sentence is
 * one, and a paragraph says its point in its first six words.
 */

import { resolveTokens } from '../manual/constants';

export const languages = {
  fi: 'Suomi',
  en: 'English',
} as const;

export const defaultLang = 'fi';

export type Lang = keyof typeof languages;

const fi = {
  'meta.title': 'Pilke',
  'meta.description':
    'Pilke on suomalainen treffisovellus ilman swaippailua ja chättäilyä. Saat kutsun, jossa on jo aika ja paikka, ja menet treffeille.',

  'nav.how': 'Näin se toimii',
  'nav.safety': 'Turvallisuus',
  'nav.questions': 'Kysyttyä',
  'nav.manual': 'Ohjeet',
  'nav.language': 'Kieli',
  'nav.skip': 'Siirry sisältöön',
  'nav.back': 'Takaisin etusivulle',
  'nav.home': 'Pilke, etusivu',
  'nav.main': 'Päävalikko',
  'nav.menu': 'Valikko',

  // The owner's own words, negations included: this one line is the exception to
  // the house rule against opening with what something is not. The soft hyphen is
  // where the compound may break when a phone is too narrow for it whole.
  'hero.title': 'Vihdoin, treffi\u00adsovellus',
  'hero.lead': 'Ei swaippailua, ei chättäilyä. Pilke järjestää treffit silloin, kun sinulle sopii.',

  // The three cards under the hero. One line of body each: the headline has
  // already made the argument, and these are the three things to remember of it.
  'fact.one.title': 'Kutsu ja tule kutsutuksi',
  'fact.one.body':
    'Lähetä kutsu ehdokkaalle, joka tuntuu sinun tyypiltäsi, ja vastaa kutsuihin, joita saat.',
  'fact.two.title': 'Aika ja paikka valmiina',
  'fact.two.body': 'Kalenterisi sopii treffit puolestasi.',
  'fact.three.title': 'Anna kipinöiden lentää',
  'fact.three.body':
    'Ylläpidetty kalenteri ja käydyt treffit tuovat kipinöitä. Niillä lähetät treffikutsuja.',

  'how.title': 'Näin se toimii',
  'how.lead': 'Ensin persoonallisuuskysely ja kalenteri. Sitten treffeille!',
  'how.more': 'Lue tarkemmin',

  // What happens once, before the loop starts. Its own card above the four steps,
  // because it is not one of them: nobody does it a second time.
  'how.start.tag': 'Ennen ensimmäistä kutsua',
  'how.start.title': 'Aloita persoonallisuus\u00adkyselystä',
  'how.start.body':
    '{{profile.story_questions}} pientä tilannetta, joissa valitset, mitä tekisit. Kysely etenee kysymys kerrallaan, ja voit jatkaa myöhemmin siitä, mihin jäit. Sitten kerrot toiveesi ja merkitset kalenteriin ajat, jolloin sinulle sopii käydä treffeillä.',

  'how.one.title': 'Lähetä treffikutsu',
  'how.one.body':
    'Löydä ehdokkaat ja kutsu sinulle sopivin. Tarjoa pari aikaa ja paikkaa, niin kutsu lähtee.',
  'how.two.title': 'Vastaa kutsuihin',
  'how.two.body': 'Näet, kuka kutsui ja mitä hän ehdottaa. Valitse aika ja paikka, niin treffit on sovittu.',
  'how.three.title': 'Menkää treffeille',
  'how.three.body':
    'Pilke kertoo ajan, paikan ja reitin. Paikan päällä voitte jakaa sijaintinne, niin löydätte toisenne.',
  'how.four.title': 'Kerro, miten meni',
  'how.four.body':
    'Vastaa treffien jälkeen pariin kysymykseen. Saat kipinöitä, ja seuraavat ehdokkaat osuvat paremmin.',
  'how.loop': 'Ylläpidetty kalenteri tuo uusia ehdokkaita ja lisää kipinöitä.',

  // Sparks, on the front page in two lines and no more: what they are for, the two
  // ways they build up week to week, and a link to the rest. The full ledger —
  // the welcome sparks, the ceiling, refunds — is `nain-se-toimii`'s.
  'sparks.title': 'Pilke pyörii kipinöiden ympärillä.',
  'sparks.body':
    'Kipinöitä kertyy, kun merkitset kalenteriin vapaita aikoja ja käyt treffeillä. Kun niitä on {{petals.set_cost}}, voit lähettää treffikutsun.',
  'sparks.earn': 'Näin niitä kertyy',
  'sparks.calendar.amount': '+1',
  'sparks.calendar.note': 'enintään {{calendar.max_petals_per_week}} viikossa',
  'sparks.date.amount': '+{{petals.per_date}}',
  'sparks.date.note': 'kun olet kertonut, miten meni',
  'sparks.highlight': 'Kun toinen sanoo kutsullesi kyllä, kipinöitä lentää.',
  'sparks.art.alt': 'Pilkkeen kipinälaskuri, jossa on kaksi kipinää.',
  'sparks.more': 'Kipinät ja koko kierto tarkemmin',

  // The safety block on the front page. Two cards, venues first because a reader
  // who has not used the app yet is best served by where they will be sent; the
  // trusted person and the button are one card, because the one does nothing
  // without the other. The page at `turvallisuus` carries the whole of it.
  'safety.front.title': 'Turvallisuus on mukana alusta asti.',
  'safety.front.lead':
    'Tuntemattoman tapaaminen on eri asia kuin viestittely. Siksi valitsemme treffipaikat itse ja annamme sinulle turvapainikkeen. Ota se käyttöön ennen ensimmäisiä treffejä.',
  'safety.card.places.title': 'Paikat valitsemme itse',
  'safety.card.places.body':
    'Jokainen treffipaikka on julkinen paikka, jonka olemme itse valinneet: kahvila, ravintola tai muu tila, jossa on muita ihmisiä ympärillä.',
  'safety.card.button.title': 'Turvapainike',
  'safety.card.button.body':
    'Tallenna asetuksiin luotettavan läheisen numero. Treffien aikana yksi painallus lähettää hänelle tekstiviestin, jossa pyydät häntä ottamaan yhteyttä.',

  // Forward-looking, and marked as such in the copy itself. It sits under the
  // cards rather than in one, because a card next to two shipped features reads
  // as a third shipped feature.
  'safety.future.title': 'Tulossa: vahva tunnistautuminen',
  'safety.future.body':
    'Haluamme varmistaa käyttäjien henkilöllisyyden suomalaisella vahvalla tunnistautumisella. Kerromme, kun se on käytössä.',

  'safety.title': 'Turvallisuus',
  'safety.contact.title': 'Luotettava läheinen',
  'safety.contact.body':
    'Tallenna asetusten Turvallisuus-kohtaan yhden läheisesi puhelinnumero ja sovi asiasta hänen kanssaan etukäteen. Se on ainoa numero, johon sovellus voi lähettää viestin puolestasi.',
  'safety.button.title': 'Turvapainike',
  'safety.button.body':
    'Turvapainike ilmestyy treffinäytölle, kun olet tallentanut luotettavan läheisen numeron, joten tallenna se etukäteen. Yksi painallus lähettää hänelle tekstiviestin, jossa on nimesi ja pyyntö ottaa sinuun yhteyttä. Sijaintisi, treffipaikka, kellonaika ja tiedot treffikumppanistasi jäävät viestistä pois. Treffikumppanisi ei saa tietää painalluksesta.',
  'safety.report.title': 'Ilmoitus',
  'safety.report.body':
    'Jos olosi oli treffeillä turvaton, kerro siitä treffien jälkeisessä palautteessa, halutessasi omin sanoin. Ilmoitus menee Pilkkeen työntekijöille, ja vain he lukevat sen. Luemme sen niin pian kuin mahdollista.',

  'tips.title': 'Näin tapaat turvallisesti',
  'tips.lead':
    'Tavallista järkeä, joka unohtuu helposti, kun jännittää.',
  'tips.one': 'Tallenna luotettavan läheisen numero ennen ensimmäisiä treffejä.',
  'tips.two': 'Kerro jollekin minne menet ja milloin arvioit olevasi kotona.',
  'tips.three': 'Valitse ensimmäisille treffeille paikka, jossa on muita ihmisiä.',
  'tips.four': 'Mene treffeille ja tule kotiin omin kyydein.',
  'tips.five': 'Pidä puhelin ladattuna.',
  'tips.six':
    'Jos olo on epämukava, lähde. Sinun ei tarvitse selittää sitä kenellekään, ei meillekään.',

  'privacy.title': 'Sijainti ja yksityisyys',

  // Two paragraphs, because these are two different things and conflating them is
  // how the earlier version came to claim something the app does not do. The area
  // is a choice on a map; the position is a permission during a date.
  'privacy.area':
    'Treffialueet valitset kartalta. Pilke on jakanut kartan valmiiksi alueisiin, ja sinä valitset niistä ne, joilla voisit käydä treffeillä. Treffipaikkoja ehdotetaan vain valitsemiltasi alueilta, joten kotiosoitettasi ei tarvita.',
  'privacy.body':
    'Laitteesi sijaintia luetaan vain treffeillä ja vain, jos itse valitset jakaa sen. Jakaminen toimii {{sharing.lead_minutes}} minuuttia ennen sovittua alkamisaikaa ja {{sharing.trail_minutes}} minuuttia sen jälkeen ja vain {{sharing.radius_m}} metrin säteellä treffipaikasta, joten kotoa sinua ei voi paikantaa. Sijainnin näkee vain treffikumppanisi. Se poistetaan heti, kun aika umpeutuu, ja voit lopettaa jakamisen milloin tahansa.',

  'safety.more': 'Lue turvallisuudesta',
  'safety.page.lead':
    'Tuntemattoman tapaaminen on eri asia kuin viestittely. Tältä sivulta näet, mitä Pilke tekee turvallisuutesi eteen ja mitä kannattaa tehdä itse.',

  // The detail page. Every number here is the backend's own constant, and the
  // README records which.
  'detail.title': 'Näin Pilke toimii',
  'detail.lead':
    'Mistä ehdokkaat tulevat, miten kipinät kertyvät ja mitä tapahtuu, kun suunnitelmat muuttuvat. Tässä koko kierto tarkemmin.',

  'detail.start.title': 'Ennen ensimmäistä kutsua',
  'detail.start.body':
    'Rekisteröinti alkaa puhelinnumerosta ja tekstiviestillä tulevasta koodista. Sen jälkeen annat kutsumanimen, syntymäpäivän ja kuvan.',
  'detail.story.title': 'Persoonallisuuskysely',
  'detail.story.body':
    '{{profile.story_questions}} pientä tilannetta, joissa valitset, mitä tekisit. Vastauksesi vaikuttavat siihen, missä järjestyksessä ehdokkaasi näytetään. Kysely etenee kysymys kerrallaan, ja voit jatkaa siitä, mihin jäit. Kysymyssarjoihin voit vastata myöhemmin omaan tahtiisi.',
  'detail.prefs.title': 'Toiveet ja kalenteri',
  'detail.prefs.body':
    'Kerrot, kenen kanssa haluat tavata, minkä ikäisiä ehdokkaita otat vastaan ja millaisia treffejä etsit. Kartalta valitset alueet, joilla voisit käydä treffeillä. Lopuksi merkitset kalenteriin ajat, jolloin sinulle sopii. Alkuun riittää yksi aika, joka on vähintään {{calendar.min_slot_hours}} tunnin mittainen.',

  'detail.draw.title': 'Mistä ehdokkaat tulevat',
  'detail.draw.body':
    'Kun löydät ehdokkaat, jokainen heistä täyttää kolme ehtoa: toiveenne käyvät yksiin, kalentereissanne on vähintään tunti yhteistä aikaa, ja löytyy paikka, johon pääsette molemmat. Sinä valitset, kenelle kutsu lähtee.',
  'detail.invite.title': 'Kutsu ja vastaus',
  'detail.invite.body':
    'Tarjoat kortin yhteisistä ajoista ja paikoista ne, jotka sopivat sinulle. Jotta toinen voi valita, kutsussa on vähintään {{invitation.choice_threshold}} aikaa tai {{invitation.choice_threshold}} paikkaa. Hän valitsee yhden kumpaakin, ja treffit on sovittu. Kutsuun on vastattava {{invitation.answer_hours}} tunnissa.',

  'detail.economy.title': 'Kipinät',
  'detail.economy.body':
    'Pilke pyörii kipinöiden ympärillä. Niitä kertyy ylläpidetystä kalenterista ja käydyistä treffeistä, ja niillä lähetät treffikutsuja.',
  'detail.economy.earn': 'Näin kipinöitä kertyy',
  'detail.earn.signup': 'Tervetuliaiskipinät',
  'detail.earn.signup.note': 'Kerran, kun vahvistat puhelinnumerosi. Ne riittävät ensimmäiseen kutsuun.',
  'detail.earn.calendar': '{{calendar.petal_week_hours}} tuntia kalenterissa viikon ajan',
  'detail.earn.calendar.note':
    'Mukaan lasketaan seuraavan {{calendar.earning_horizon_days}} päivän ajat, kerrallaan enintään {{calendar.counted_hours_cap}} tuntia. Viikossa kipinöitä kertyy siis enintään {{calendar.max_petals_per_week}}.',
  'detail.earn.date': 'Käydyt treffit',
  'detail.earn.date.note':
    'Kipinät tulevat, kun olet kertonut, miten meni. Kumpikin saa omansa.',

  'detail.economy.spend': 'Näin kipinät kuluvat',
  'detail.economy.spend.body':
    'Treffikutsuun kuluu {{petals.set_cost}} kipinää. Ne kuluvat heti, kun aloitat kutsun, eli jo ennen kuin valitset, kenet kutsut. Jos sopivia ehdokkaita ei löydy, kipinäsi pysyvät tallessa. Kipinöitä mahtuu kerrallaan {{petals.cap}}, eli {{petals.cap_roses}} kutsun verran, ja sen jälkeen uudet odottavat, kunnes lähetät kutsun. Palautukset tulevat perille, vaikka kipinöitä olisi jo {{petals.cap}}.',

  'detail.changes.title': 'Jos suunnitelmat muuttuvat',
  'detail.changes.expired': 'Kutsuun ei vastata vuorokaudessa',
  'detail.changes.expired.note':
    'Kutsu raukeaa itsestään, ja kipinäsi palaavat sinulle. Vastaamatta jättänyt saa {{cooldown.no_answer_hours}} tunnin jäähyn, jonka aikana hän ei voi löytää uusia ehdokkaita.',
  'detail.changes.declined': 'Kutsu hylätään',
  'detail.changes.declined.note':
    'Kipinäsi palaavat sinulle. Kutsun hylännyt saa {{cooldown.decline_hours}} tunnin jäähyn, jonka aikana hän ei voi löytää uusia ehdokkaita.',
  'detail.changes.withdrawn': 'Perut oman kutsusi',
  'detail.changes.withdrawn.note':
    'Kipinät jäävät käytetyiksi, ja saat {{cooldown.withdrawal_hours}} tunnin jäähyn, jonka aikana et voi löytää uusia ehdokkaita.',
  'detail.changes.canceled': 'Sovitut treffit perutaan',
  'detail.changes.canceled.note':
    'Voit perua, mutta se on toiselle epäkohteliasta: hän on varannut aikaa sinulle. Perumisesta seuraa jäähy, jonka aikana et näy muiden ehdokkaissa etkä pääse löytämään uusia ehdokkaita. Mitä lähempänä treffit ovat ja mitä useammin perut, sitä pidempään se kestää. Jos kutsuttu peruu, kutsuja saa kipinänsä takaisin.',

  'detail.chat.title': 'Miksi chattia ei ole',
  'detail.chat.body':
    'Chättäily sovelluksessa on oikeastaan turha rituaali ennen treffejä, joilla vasta pääsee tapaamaan toisen ja juttelemaan kunnolla. Pilke hyppää suoraan siihen: kutsussa on jo aika ja paikka, ja juttu alkaa samassa pöydässä. Treffipäivänä kartta näyttää, missä toinen on, joten löydätte toisenne ilman viestejä.',

  'economy.lead': '{{petals.set_cost}} kipinää, yksi treffikutsu.',
  'economy.spark.alt': 'Pilkkeen kipinälaskuri, jossa on viisi kipinää, yhden treffikutsun verran.',
  'economy.amount.one': '1 kipinä',
  'economy.amount.two': '2 kipinää',
  'economy.amount.five': '5 kipinää',

  // The waitlist. TODO(pilke-web): the form posts nowhere yet — see README.
  'cta.title': 'Pilke on suljetussa betassa',
  'cta.body': 'Jätä sähköpostiosoitteesi, niin kerromme heti, kun pääset mukaan.',
  'cta.label': 'Sähköpostiosoite',
  'cta.placeholder': 'sina@esimerkki.fi',
  'cta.button': 'Liity betaan',
  'cta.note': 'Käytämme osoitetta vain betakutsuun. Emme lähetä muuta emmekä anna sitä eteenpäin.',
  // The link this form may not collect an address without. Its own key rather
  // than a clause inside `cta.note`, so the promise and the document that has to
  // back it up are not one sentence somebody has to re-translate together.
  'cta.privacy': 'Lue lisää tietosuojaselosteesta.',

  /*
    The three states the form has beyond its own copy. `closed` stands in for
    `cta.note` while the privacy statement is a draft — the note promises what we
    do with an address, and promising that before the statement exists is the one
    thing this form must not do.
  */
  'cta.closed': 'Betajono avautuu pian.',
  'cta.sending': 'Lähetetään…',
  'cta.failed': 'Liittyminen ei onnistunut. Yritä hetken kuluttua uudelleen.',

  'faq.title': 'Kysyttyä',
  'faq.lead': 'Lyhyet vastaukset siihen, mitä Pilkkeestä useimmin kysytään.',
  'faq.chat.q': 'Voiko sovelluksessa viestitellä?',
  'faq.chat.a':
    'Ei. Kutsussa on jo aika ja paikka, joten sopiminen ei vaadi keskustelua. Loput sanotaan kasvokkain.',
  'faq.who.q': 'Kuka näkee tietoni?',
  'faq.who.a':
    'Ehdokas näkee kutsumanimesi, ikäsi, kuvasi ja sen, mitä teillä on yhteistä. Puhelinnumerosi välitämme toiselle vain, jos valitsette treffien jälkeen molemmat, että numerot saa jakaa. Tarkemmin tietosuojaselosteessa.',
  'faq.safety.q': 'Näkeekö toinen, missä olen?',
  'faq.safety.a':
    'Vain jos valitset niin. Sijainti näkyy {{sharing.lead_minutes}} minuuttia ennen sovittua alkua ja {{sharing.trail_minutes}} minuuttia sen jälkeen, ja vain {{sharing.radius_m}} metrin säteellä treffipaikasta. Voit lopettaa jakamisen milloin tahansa, ja sijainti poistetaan, kun aika umpeutuu.',
  'faq.cost.q': 'Mitä se maksaa?',
  'faq.cost.a':
    'Pilke on maksuton. Se pyörii kipinöiden ympärillä: niitä kertyy, kun pidät kalenterisi ajan tasalla ja käyt treffeillä, ja {{petals.set_cost}} kipinällä lähetät treffikutsun. Kipinöitä ei voi ostaa.',
  'faq.refund.q': 'Milloin kipinät palaavat?',
  'faq.refund.a':
    'Kun kutsusi hylätään, kun se raukeaa vastaamattomana {{invitation.answer_hours}} tunnissa tai kun kutsumasi henkilö peruu sovitut treffit, {{petals.refund}} kipinää palaa sinulle. Jos peruutat kutsun itse tai perut sovitut treffit, kipinät jäävät käytetyiksi.',
  'faq.cancel.q': 'Entä jos treffit peruuntuvat?',
  'faq.cancel.a':
    'Sovitut treffit voi perua sovelluksessa, mutta se on toiselle epäkohteliasta: hän on varannut aikaa sinulle. Perumisesta seuraa jäähy, jonka aikana et näy muiden ehdokkaissa etkä pääse löytämään uusia ehdokkaita. Mitä aikaisemmin perut, sitä lyhyempi jäähy on. Saapumatta jättämisestä seuraa samanlainen jäähy. Jos toinen kutsui sinut, hän saa kipinänsä takaisin. Kutsun hylkäämisestä ja vastaamatta jättämisestä seuraa lyhyt jäähy: {{cooldown.decline_hours}} tuntiin et voi löytää uusia ehdokkaita.',
  'faq.delete.q': 'Voinko poistaa tilini?',
  'faq.delete.a':
    'Kyllä, asetuksista. Nimesi, kuvasi ja yhteystietosi poistetaan heti. Menneet treffit ja niistä annetut palautteet jäävät talteen, koska ne ovat yhtä lailla toisen osapuolen tietoja.',

  'shot.treffit':
    'Treffit-sivu puhelimessa: kipinät ylhäällä, alla omat treffit ja saapuneet kutsut.',
  'shot.kalenteri': 'Kalenterinäkymä, jossa viikon päivät ja niihin merkityt vapaat treffiajat.',
  'shot.story':
    'Persoonallisuuskyselyn ensimmäinen kysymys onboardingissa: tilanne ja kolme vaihtoehtoa, joista valitaan yksi.',
  'shot.platter':
    'Ehdokkaat-näkymä: yksi ehdokas, hänen kanssaan yhteiset ajat ja valittu tekeminen.',
  'shot.invitation': 'Saapunut treffikutsu: kutsujan nimi ja kuva, tarjotut ajat ja paikka.',
  'shot.feedback':
    'Treffipalaute puhelimessa: kuka oli treffeillä, milloin, ja ensimmäinen kysymys vastausvaihtoehtoineen.',
  'shot.asetukset':
    'Asetusten Turvallisuus-osio avattuna, ja siinä kenttä luotettavan henkilön numerolle.',
  'shot.date': 'Sovitut treffit puhelimessa: aika, paikka kartalla ja turvapainike.',

  // The front page's photographs. Each is a stock photo with a real still of the
  // app set into its phone, so the alt says both what the scene is and what the
  // screen shows.
  'photo.hero':
    'Käsi pitelee puhelinta, jossa on Pilkkeen etusivu: saapunut treffikutsu, sovitut treffit ja lähetetty kutsu.',
  'photo.start':
    'Sohvalla kissan vieressä vastataan puhelimessa persoonallisuuskyselyn ensimmäiseen kysymykseen.',
  'photo.beta':
    'Puhelin kädessä persikanvärisen talon edessä, näytöllä saapunut treffikutsu: kutsuja, ajat ja paikat.',
  'photo.loop':
    'Puhelin kädessä oranssia seinää vasten, näytöllä Pilkkeen kalenteri: viikon vapaat treffiajat ja omat menot.',

  // The legal documents. Their titles and ledes live in their own frontmatter,
  // in the document's language, so they are not repeated here; these are the
  // strings the pages around them need.
  'legal.effective': 'Voimassa {date} alkaen',
  'legal.draft.title': 'Tämä teksti on kesken',
  'legal.draft.body':
    'Lakimies käy sisällön läpi ennen kuin Pilke avautuu. Siihen asti teksti ei sido ketään eikä siihen voi vedota.',

  'legal.nav': 'Ehdot ja tietosuoja',
  'legal.deletion.nav': 'Tietojen poisto',
  'legal.deletion.title': 'Näin poistat tietosi',
  'legal.deletion.lead':
    'Poistat tilisi itse sovelluksesta. Tällä sivulla kerromme, mikä poistuu heti ja mikä jää talteen.',

  'legal.deletion.pending.title': 'Sähköpostiosoite puuttuu vielä',
  'legal.deletion.pending.body':
    'Tälle sivulle tulee osoite, johon voit kirjoittaa, jos et enää pääse sovellukseen. Osoitetta ei ole vielä hankittu, joten sivu on siltä osin kesken.',

  'legal.deletion.app.title': 'Poista tili sovelluksessa',
  'legal.deletion.app.body':
    'Avaa Pilke, mene Asetuksiin ja valitse Poista tili. Vahvista puhelinnumerollasi. Tili poistuu heti, eikä sitä saa takaisin.',

  'legal.deletion.gone.title': 'Jos et enää pääse sovellukseen',
  'legal.deletion.gone.body':
    'Kirjoita meille, niin poistamme tilin puolestasi. Kerro se puhelinnumero, jolla olet kirjautunut, jotta löydämme oikean tilin.',

  'legal.deletion.removed.title': 'Mikä poistuu heti',
  'legal.deletion.removed.one': 'Puhelinnumero ja sähköpostiosoite.',
  'legal.deletion.removed.two':
    'Nimimerkki, ikä, sukupuoli ja valokuva. Kuva poistuu myös tallennustilasta.',
  'legal.deletion.removed.three': 'Luotettavan henkilön numero.',
  'legal.deletion.removed.four': 'Treffitoiveet ja alue, jonne voisit lähteä treffeille.',
  'legal.deletion.removed.five': 'Kalenteriin merkityt ajat ja vastaukset kysymyssarjoihin.',
  'legal.deletion.removed.six':
    'Kirjautumiset kaikilta laitteilta samalla hetkellä, ja ilmoitusten vastaanotto.',
  'legal.deletion.removed.seven': 'Jaetut sijainnit.',

  'legal.deletion.kept.title': 'Mikä jää talteen',
  'legal.deletion.kept.lead':
    'Osa tiedoista on yhtä lailla toisen osapuolen tietoja, ja osa on turvallisuuspäätöksiä, joita lähteminen ei saa kumota. Nämä jäävät, mutta nimesi ei ole niissä enää kiinni.',
  'legal.deletion.kept.one':
    'Sovitut ja menneet treffit sekä niistä annetut palautteet. Toinen osapuoli näkee sinun tilallasi ”Joku”.',
  'legal.deletion.kept.two':
    'Turvallisuusilmoitukset ja niiden vapaa teksti, sekä sinun kirjoittamat että sinusta kirjoitetut.',
  'legal.deletion.kept.three': 'Merkintä siitä, että olet painanut turvapainiketta.',
  'legal.deletion.kept.four':
    'Esto, joka syntyy turvallisuusilmoituksesta. Sitä ei voi purkaa lähtemällä.',
  'legal.deletion.kept.five': 'Ilmoitukset saapumatta jättämisestä, molempiin suuntiin.',
  'legal.deletion.kept.six': 'Kipinähistoria, jotta saldot täsmäävät.',
  'legal.deletion.kept.seven':
    'Käynnissä oleva jäähy, jos sinulla on sellainen. Lähteminen ei lyhennä sitä.',
  'legal.deletion.kept.eight':
    'Ketkä ehdokkaat sinulle on tarjottu, ja keiden ehdokkaissa olet ollut.',
  'legal.deletion.kept.nine':
    'Virhe- ja suorituskykytiedot, joissa on tilisi numero. Ne eivät poistu tilin mukana, vaan häviävät itsestään 30 päivän kuluessa.',

  'legal.deletion.others.title': 'Mitä tapahtuu sovituille treffeille',
  'legal.deletion.others.body':
    'Lähettämäsi kutsut perutaan ja saamasi kutsut hylätään, ja kutsujan kipinät palautetaan. Tulevat treffit peruutetaan, ja jos toinen osapuoli oli lähettänyt kutsun, hän saa kipinänsä takaisin. Sinulle ei tule tästä seurauksia, emmekä kerro kenellekään erikseen, että lähdit.',

  'legal.deletion.again.title': 'Jos palaat myöhemmin',
  'legal.deletion.again.body':
    'Voit rekisteröityä samalla puhelinnumerolla uudelleen. Saat tyhjän tilin, eikä mikään yhdistä sitä vanhaan.',

  'legal.deletion.more': 'Lue tarkemmin tietosuojaselosteesta',

  'manual.title': 'Käyttöohje',
  'manual.lead': 'Näin Pilkettä käytetään ja näin sen osat toimivat.',
  'manual.guides': 'Vaihe vaiheelta',
  'manual.explainers': 'Taustaa',
  'manual.empty': 'Ohjeita ei ole vielä julkaistu.',
  'manual.draft.tag': 'Kesken',
  'manual.draft.title': 'Tämä ohje on kesken',
  'manual.draft.body':
    'Teksti ja kuvat voivat vielä muuttua, eikä kaikki tässä välttämättä vastaa sovellusta sellaisenaan.',
  'manual.shot.missing': 'Kuva puuttuu',
  'manual.back': 'Takaisin ohjeisiin',

  'footer.rights': 'Pilke',
  'footer.pages': 'Sivut',

  // The page GitHub Pages serves for any address it has no file for. One file for
  // both languages, so it carries a line of English under the Finnish.
  'notfound.title': 'Hups, tämä sivu jäi saapumatta',
  'notfound.lead': 'Linkki on ehkä vanhentunut. Etusivulta pääset jatkamaan.',
  'notfound.home': 'Etusivulle',
} as const;

const en: Record<keyof typeof fi, string> = {
  'meta.title': 'Pilke',
  'meta.description':
    'Pilke is a Finnish dating app with no swiping and no chatting. An invitation arrives with the time and place already in it, and you go on the date.',

  'nav.how': 'How it works',
  'nav.safety': 'Safety',
  'nav.questions': 'Questions',
  'nav.manual': 'Guide',
  'nav.language': 'Language',
  'nav.skip': 'Skip to content',
  'nav.back': 'Back to the front page',
  'nav.home': 'Pilke, home',
  'nav.main': 'Main menu',
  'nav.menu': 'Menu',

  'hero.title': 'Finally, a dating app',
  'hero.lead': 'No swiping, no chatting. Pilke arranges your dates for when it suits you.',

  'fact.one.title': 'Invite, and be invited',
  'fact.one.body':
    'Send an invitation to a candidate who feels like your type, and answer the ones you get.',
  'fact.two.title': 'Time and place already set',
  'fact.two.body': 'Your calendar arranges the date for you.',
  'fact.three.title': 'Let the sparks fly',
  'fact.three.body':
    'A calendar kept up to date and the dates you go on bring sparks. Sparks send date invitations.',

  'how.title': 'How it works',
  'how.lead': 'First the personality quiz and your calendar. Then you’re off on dates!',
  'how.more': 'Read more',

  'how.start.tag': 'Before your first invitation',
  'how.start.title': 'Start with the personality quiz',
  'how.start.body':
    '{{profile.story_questions}} little situations where you choose what you would do. It goes one question at a time, and you can pick up later where you left off. Then you say what you are looking for and mark the times that suit you for a date.',

  'how.one.title': 'Send a date invitation',
  'how.one.body':
    'Find candidates and invite the one who suits you best. Offer a couple of times and places, and your invitation is on its way.',
  'how.two.title': 'Answer invitations',
  'how.two.body': 'You see who invited you and what they suggest. Pick a time and a place, and the date is set.',
  'how.three.title': 'Go on the date',
  'how.three.body':
    'Pilke gives you the time, the place and the way there. At the venue you can share your locations, so you find one another.',
  'how.four.title': 'Say how it went',
  'how.four.body':
    'Answer a couple of questions after the date. You earn sparks, and your next candidates fit better.',
  'how.loop': 'A calendar kept up to date brings new candidates and more sparks.',

  'sparks.title': 'Pilke runs on sparks.',
  'sparks.body':
    'Sparks build up as you mark free time in your calendar and go on dates. Once you have {{petals.set_cost}}, you can send a date invitation.',
  'sparks.earn': 'How they add up',
  'sparks.calendar.amount': '+1',
  'sparks.calendar.note': 'at most {{calendar.max_petals_per_week}} a week',
  'sparks.date.amount': '+{{petals.per_date}}',
  'sparks.date.note': 'once you have said how it went',
  'sparks.highlight': 'And when they say yes to your invitation, sparks fly.',
  'sparks.art.alt': 'Pilke’s spark counter, showing two sparks.',
  'sparks.more': 'Sparks and the whole loop in detail',

  'safety.front.title': 'Safety is built in from the start.',
  'safety.front.lead':
    'Meeting a stranger is a different thing from messaging one. So we choose the venues ourselves and give you a safety button. Set it up before your first date.',
  'safety.card.places.title': 'We choose the places',
  'safety.card.places.body':
    'Every venue is a public place we picked ourselves: a cafe, a restaurant or somewhere else with other people around.',
  'safety.card.button.title': 'The safety button',
  'safety.card.button.body':
    'Save a trusted person’s number in the settings. During a date, one press sends them a text asking them to get in touch.',

  'safety.future.title': 'Coming: strong electronic identification',
  'safety.future.body':
    'We want to verify identities with Finnish strong electronic identification. We will tell you when it is in use.',

  'safety.title': 'Safety',
  'safety.contact.title': 'A trusted person',
  'safety.contact.body':
    'Save one trusted person’s phone number under Safety in the settings, and agree it with them beforehand. It is the only number the app can text on your behalf.',
  'safety.button.title': 'The safety button',
  'safety.button.body':
    'The safety button appears on the date screen once you have saved a trusted person’s number, so save it beforehand. One press texts them your name and a request to get in touch. Your location, the venue, the time and anything about your date are left out of the message. Your date is not told about the press.',
  'safety.report.title': 'Reporting',
  'safety.report.body':
    'If you did not feel safe on the date, say so in the feedback afterwards, in your own words if you like. The report goes to Pilke staff, and only they read it. We read it as soon as we can.',

  'tips.title': 'Meeting somebody safely',
  'tips.lead':
    'Ordinary sense, and easy to forget when you are nervous.',
  'tips.one': 'Save a trusted person before your first date.',
  'tips.two': 'Tell somebody where you are going and when you expect to be home.',
  'tips.three': 'Pick somewhere with other people around for a first date.',
  'tips.four': 'Arrange your own way there and your own way back.',
  'tips.five': 'Keep your phone charged.',
  'tips.six':
    'If you feel uncomfortable, leave. You do not owe anybody an explanation for it, us included.',

  'privacy.title': 'Location and privacy',
  'privacy.area':
    'You choose your date areas on a map. Pilke has divided the map into areas, and you pick the ones where you could go on a date. Venues are suggested only inside the areas you choose, so we do not need your home address.',
  'privacy.body':
    'Your device location is read only on a date, and only if you choose to share it. Sharing works from {{sharing.lead_minutes}} minutes before the agreed start to {{sharing.trail_minutes}} minutes after, and only within {{sharing.radius_m}} metres of the venue, so you cannot be located at home. Only your date sees it. It is deleted as soon as the window closes, and you can stop at any time.',

  'safety.more': 'Read about safety',
  'safety.page.lead':
    'Meeting a stranger is a different thing from messaging one. This page covers what Pilke does for your safety and what is worth doing yourself.',

  'detail.title': 'How Pilke works',
  'detail.lead':
    'Where candidates come from, how sparks build up, and what happens when plans change: the whole loop, in detail.',

  'detail.start.title': 'Before your first invitation',
  'detail.start.body':
    'Signing up starts with a phone number and a code by text. After that you give a name, a birthday and a photo.',
  'detail.story.title': 'The personality quiz',
  'detail.story.body':
    '{{profile.story_questions}} little situations where you choose what you would do. Your answers shape the order your candidates are shown in. It goes one question at a time, and you can pick up where you left off. The question sets are there to answer later, at your own pace.',
  'detail.prefs.title': 'Preferences and calendar',
  'detail.prefs.body':
    'You say who you want to meet, what ages you will consider and what kind of date you are looking for. On a map you choose the areas where you could go on a date. Then you mark the times that suit you. A single slot of {{calendar.min_slot_hours}} hour or more is enough to start.',

  'detail.draw.title': 'Where candidates come from',
  'detail.draw.body':
    'When you find candidates, every one of them meets three conditions: your wishes match, your calendars share at least an hour, and there is a place you can both get to. You choose who the invitation goes to.',
  'detail.invite.title': 'The invitation and the answer',
  'detail.invite.body':
    'You offer the shared times and places on the card that suit you. So that the other person has a choice, an invitation holds at least {{invitation.choice_threshold}} times or {{invitation.choice_threshold}} places. They pick one of each, and the date is set. An invitation has to be answered within {{invitation.answer_hours}} hours.',

  'detail.economy.title': 'Sparks',
  'detail.economy.body':
    'Pilke runs on sparks. They build up from a calendar kept up to date and from the dates you go on, and they are what you send invitations with.',
  'detail.economy.earn': 'How sparks add up',
  'detail.earn.signup': 'Welcome sparks',
  'detail.earn.signup.note': 'Once, when you confirm your phone number. Enough for your first invitation.',
  'detail.earn.calendar': '{{calendar.petal_week_hours}} hours in your calendar, kept for a week',
  'detail.earn.calendar.note':
    'Times in the next {{calendar.earning_horizon_days}} days count, up to {{calendar.counted_hours_cap}} hours at once, so a week brings at most {{calendar.max_petals_per_week}} sparks.',
  'detail.earn.date': 'A date you went on',
  'detail.earn.date.note': 'The sparks arrive once you have said how it went. Each of you gets your own.',

  'detail.economy.spend': 'How sparks are spent',
  'detail.economy.spend.body':
    'A date invitation takes {{petals.set_cost}} sparks. They go as soon as you start the invitation, before you choose who to invite. If no suitable candidates can be found, your sparks stay put. You can hold {{petals.cap}} sparks at a time, enough for {{petals.cap_roses}} invitations, and after that new ones wait until you send one. Refunds arrive even when you already have {{petals.cap}}.',

  'detail.changes.title': 'If plans change',
  'detail.changes.expired': 'An invitation goes unanswered for a day',
  'detail.changes.expired.note':
    'It lapses by itself and your sparks come back to you. Whoever left it unanswered gets a {{cooldown.no_answer_hours}}-hour cooldown, during which they cannot find new candidates.',
  'detail.changes.declined': 'An invitation is turned down',
  'detail.changes.declined.note':
    'Your sparks come back to you. Whoever declined gets a {{cooldown.decline_hours}}-hour cooldown, during which they cannot find new candidates.',
  'detail.changes.withdrawn': 'You withdraw your own invitation',
  'detail.changes.withdrawn.note':
    'The sparks stay spent, and you get a {{cooldown.withdrawal_hours}}-hour cooldown, during which you cannot find new candidates.',
  'detail.changes.canceled': 'An agreed date is called off',
  'detail.changes.canceled.note':
    'You can, but it is rude to the other person: they have set time aside for you. Calling it off brings a cooldown, during which you do not appear among other people’s candidates and cannot find new ones. The closer the date and the more often you call dates off, the longer it lasts. If the person invited calls it off, the sender gets their sparks back.',

  'detail.chat.title': 'Why there is no chat',
  'detail.chat.body':
    'Chatting in an app is really just an unnecessary ritual before the date, which is where you actually get to meet and talk. Pilke skips straight to the good part: the invitation already has the time and the place, and the talking starts at the same table. On the day, the map shows where the other person is, so you find each other without messaging.',

  'economy.lead': '{{petals.set_cost}} sparks, one date invitation.',
  'economy.spark.alt': 'Pilke’s spark counter with five sparks, enough for one date invitation.',
  'economy.amount.one': '1 spark',
  'economy.amount.two': '2 sparks',
  'economy.amount.five': '5 sparks',

  'cta.title': 'Pilke is in closed beta',
  'cta.body': 'Leave your email address and we will tell you as soon as you can get in.',
  'cta.label': 'Email address',
  'cta.placeholder': 'you@example.com',
  'cta.button': 'Join the beta',
  'cta.note':
    'We use the address for the beta invitation and nothing else. We do not pass it on.',
  'cta.privacy': 'Read more in the privacy policy.',
  'cta.closed': 'The waitlist opens soon.',
  'cta.sending': 'Sending…',
  'cta.failed': 'That did not go through. Please try again in a moment.',

  'faq.title': 'Questions',
  'faq.lead': 'Short answers to what people ask about Pilke most often.',
  'faq.chat.q': 'Can I message people in the app?',
  'faq.chat.a':
    'No. An invitation already carries the time and the place, so arranging it needs no conversation. The rest is said in person.',
  'faq.who.q': 'Who sees my details?',
  'faq.who.a':
    'A candidate sees your first name, your age, your photo and what the two of you have in common. We pass your phone number on only if you both choose, after a date, to share numbers. The privacy policy has the detail.',
  'faq.safety.q': 'Can the other person see where I am?',
  'faq.safety.a':
    'Only if you choose to share it. It is visible from {{sharing.lead_minutes}} minutes before the agreed start to {{sharing.trail_minutes}} minutes after, and only within {{sharing.radius_m}} metres of the venue. You can stop at any time, and the location is deleted when the window closes.',
  'faq.cost.q': 'What does it cost?',
  'faq.cost.a':
    'Pilke is free. It runs on sparks: you collect them by keeping your calendar up to date and going on dates, and {{petals.set_cost}} sparks send a date invitation. Sparks cannot be bought.',
  'faq.refund.q': 'When do sparks come back?',
  'faq.refund.a':
    'When your invitation is declined, when it lapses unanswered after {{invitation.answer_hours}} hours, or when the person you invited calls off your date, {{petals.refund}} sparks come back to you. If you withdraw the invitation or call off the date yourself, the sparks stay spent.',
  'faq.cancel.q': 'What if a date falls through?',
  'faq.cancel.a':
    'You can call off an agreed date in the app, but it is rude to the other person: they have set time aside for you. Calling it off brings a cooldown, during which you do not appear among other people’s candidates and cannot find new ones. The earlier you call it off, the shorter it is. Not turning up brings the same kind of cooldown. If they invited you, they get their sparks back. Declining an invitation, or leaving it unanswered, brings a short cooldown: for {{cooldown.decline_hours}} hours you cannot find new candidates.',
  'faq.delete.q': 'Can I delete my account?',
  'faq.delete.a':
    'Yes, from the settings. Your name, photo and contact details go straight away. Past dates and the feedback written about them stay, because those belong to the other person as much as to you.',

  'shot.treffit':
    'The Dates page on a phone: your sparks along the top, your dates and the invitations you have received below.',
  'shot.kalenteri':
    'The calendar view, with the days of the week and the times marked as free.',
  'shot.story':
    'The first question of the personality quiz during onboarding: a situation and three options, one of which you pick.',
  'shot.platter':
    'The candidates view: one candidate, the times you both have, and the chosen activity.',
  'shot.invitation':
    'A date invitation received: who sent it, with their photo, the times offered and the place.',
  'shot.feedback':
    'Date feedback on a phone: who the date was with, when it was, and the first question with its options.',
  'shot.asetukset':
    'The Safety section of the settings, open, with the field for a trusted person’s number.',
  'shot.date': 'An agreed date on a phone: the time, the venue on a map, and the safety button.',

  'photo.hero':
    'A hand holding a phone with the Pilke home screen: a date invitation received and a date agreed.',
  'photo.start':
    'On a sofa beside a sleeping cat, someone answers the first question of the personality quiz on their phone.',
  'photo.beta':
    'A phone held up in front of a peach-coloured house, showing a date invitation received: who sent it, the times and the places.',
  'photo.loop':
    'A phone held up against an orange wall, showing the Pilke calendar: the week’s free date slots and your own plans.',

  'legal.effective': 'In effect from {date}',
  'legal.draft.title': 'This text is unfinished',
  'legal.draft.body':
    'A lawyer goes through it before Pilke opens. Until then it binds nobody and cannot be relied on.',

  'legal.nav': 'Terms and privacy',
  'legal.deletion.nav': 'Deleting your data',
  'legal.deletion.title': 'How to delete your data',
  'legal.deletion.lead':
    'You delete your account yourself, in the app. This page says what goes straight away and what stays.',

  'legal.deletion.pending.title': 'There is no email address yet',
  'legal.deletion.pending.body':
    'An address for people who can no longer reach the app belongs on this page. It has not been bought yet, so the page is unfinished in that respect.',

  'legal.deletion.app.title': 'Delete your account in the app',
  'legal.deletion.app.body':
    'Open Pilke, go to Settings and choose Delete account. Confirm with your phone number. The account goes immediately and does not come back.',

  'legal.deletion.gone.title': 'If you can no longer reach the app',
  'legal.deletion.gone.body':
    'Write to us and we will delete the account for you. Tell us the phone number you signed in with, so we find the right account.',

  'legal.deletion.removed.title': 'What goes straight away',
  'legal.deletion.removed.one': 'Your phone number and email address.',
  'legal.deletion.removed.two':
    'Your nickname, age, gender and photo. The photo is deleted from storage as well.',
  'legal.deletion.removed.three': 'Your trusted person’s number.',
  'legal.deletion.removed.four': 'What you are looking for, and the area you could travel to.',
  'legal.deletion.removed.five': 'The times marked in your calendar, and your answers to the question sets.',
  'legal.deletion.removed.six':
    'Every session on every device, in the same instant, and any notifications to you.',
  'legal.deletion.removed.seven': 'Any location you shared.',

  'legal.deletion.kept.title': 'What stays',
  'legal.deletion.kept.lead':
    'Some of it belongs to the other person as much as to you, and some of it is a safety decision that leaving must not undo. These stay, with your name no longer attached to them.',
  'legal.deletion.kept.one':
    'Dates agreed and past, and the feedback given about them. The other person sees ”Someone” where you were.',
  'legal.deletion.kept.two':
    'Safety reports and the free text in them, both what you wrote about somebody and what somebody wrote about you.',
  'legal.deletion.kept.three': 'The fact that you pressed the safety button.',
  'legal.deletion.kept.four':
    'The block created by a safety report. Leaving does not lift it.',
  'legal.deletion.kept.five': 'Reports of not turning up, in both directions.',
  'legal.deletion.kept.six': 'Your spark history, so that balances still add up.',
  'legal.deletion.kept.seven':
    'Any cooldown you are currently serving. Leaving does not shorten it.',
  'legal.deletion.kept.eight':
    'Which candidates you were offered, and whose candidates you appeared among.',
  'legal.deletion.kept.nine':
    'Error and performance records, which carry your account number. They do not go with the account, but clear on their own within 30 days.',

  'legal.deletion.others.title': 'What happens to dates you agreed to',
  'legal.deletion.others.body':
    'Invitations you sent are withdrawn and invitations you received are declined, with the sender’s sparks refunded. Dates still ahead are cancelled, and if the other person sent the invitation, they get their sparks back. Nothing is held against you, and nobody is told separately that you left.',

  'legal.deletion.again.title': 'If you come back later',
  'legal.deletion.again.body':
    'You can register the same phone number again. You get an empty account, and nothing links it to the old one.',

  'legal.deletion.more': 'Read the detail in the privacy policy',

  'manual.title': 'User guide',
  'manual.lead': 'How to use Pilke, and how its parts work.',
  'manual.guides': 'Step by step',
  'manual.explainers': 'Background',
  'manual.empty': 'No guides have been published yet.',
  'manual.draft.tag': 'Unfinished',
  'manual.draft.title': 'This guide is unfinished',
  'manual.draft.body':
    'The text and the pictures may still change, and not everything here necessarily matches the app as it is.',
  'manual.shot.missing': 'Screenshot missing',
  'manual.back': 'Back to the guide',

  'footer.rights': 'Pilke',
  'footer.pages': 'Pages',

  'notfound.title': 'Oops, this page didn’t turn up',
  'notfound.lead': 'The link may be out of date. Carry on from the front page.',
  'notfound.home': 'To the front page',
};

export const ui = { fi, en } as const;

export type UiKey = keyof typeof fi;

/** Returns a lookup that falls back to Finnish, so a gap is visible, not blank. */
/**
 * A string in `lang`, with every `{{area.name}}` token filled in from the app's
 * constants, as the manual's are (`src/manual/constants.ts`). A figure the backend
 * owns, like how long location sharing runs, is written as a token rather than as
 * prose, so it moves when the backend's value does.
 */
export function useTranslations(lang: Lang) {
  return function t(key: UiKey): string {
    return resolveTokens(ui[lang][key] ?? ui[defaultLang][key], `src/i18n/ui.ts (${lang}.${key})`);
  };
}

/** The path to `route` in `lang`: Finnish at the root, English under /en. */
export function localePath(lang: Lang, route = ''): string {
  const clean = route.replace(/^\/+/, '');
  const prefix = lang === defaultLang ? '/' : `/${lang}/`;
  return `${prefix}${clean}`.replace(/\/+$/, '') || '/';
}

/**
 * The routes every page is built at: Finnish at the root, English under `/en`.
 *
 * A page file lives at `pages/[...lang]/<slug>.astro` and hands this to
 * `getStaticPaths`, so one file is both languages of one page and a section
 * cannot exist in Finnish and not in English. The Finnish entry has no segment
 * at all — a rest parameter matches zero of them — which is what puts Finnish at
 * the root without a redirect.
 */
export function localeRoutes() {
  return [{ params: { lang: undefined } }, { params: { lang: 'en' } }];
}

/** The language of the route being built, from the `[...lang]` segment. */
export function localeOf(params: { lang?: string | undefined }): Lang {
  return params.lang === 'en' ? 'en' : defaultLang;
}
