/**
 * Every string on the site, in both languages.
 *
 * Finnish is the product's language and the one written first; English is a full
 * translation rather than a fallback set, so a key missing from `en` is a type
 * error here in the same way it is in the app's own dictionaries.
 *
 * Product vocabulary is the app's own spelling: teralehdet are what the product
 * calls its currency, and five of them make a ruusu. The site should not invent
 * a softer word for either.
 *
 * The front page argues one thing: there is no chat, and the shortest path to
 * meeting somebody is a kutsu with the time already in it. The currency belongs
 * to `nain-se-toimii`, because a price list on a front page reads as a game to
 * be played rather than as an app for meeting people.
 *
 * Sentences here are short on purpose. A clause that can be its own sentence is
 * one, and a paragraph says its point in its first six words.
 */

export const languages = {
  fi: 'Suomi',
  en: 'English',
} as const;

export const defaultLang = 'fi';

export type Lang = keyof typeof languages;

const fi = {
  'meta.title': 'Pilke',
  'meta.description':
    'Pilke on suomalainen deittisovellus ilman chattia. Saat kutsun, jossa on jo aika ja paikka, ja menet treffeille.',

  'nav.how': 'Näin se toimii',
  'nav.safety': 'Turvallisuus',
  'nav.questions': 'Kysyttyä',
  'nav.language': 'Kieli',
  'nav.skip': 'Siirry sisältöön',
  'nav.back': 'Takaisin etusivulle',

  'hero.title': 'Treffit, ei swaippailua',
  'hero.lead':
    'Ei chattia, ei viikkojen viestittelyä. Saat kutsun, jossa aika ja paikka ovat jo valmiina — valitse sopiva hetki, niin treffit on sovittu.',

  'fact.one.title': 'Sinä valitset, kenet kutsut',
  'fact.one.body': 'Ei loputonta pinoa selattavaksi.',
  'fact.two.title': 'Aika ja paikka valmiina',
  'fact.two.body': 'Kalenterisi sopii treffit puolestasi.',
  'fact.three.title': 'Ei mitään pelattavaa',
  'fact.three.body': 'Ei ostettavaa näkyvyyttä, ei nostoja.',

  'diff.title': 'Miksi tämä on erilaista',
  'diff.lead':
    'Muut sovellukset opettivat, että tutustuminen tapahtuu ruudulla ja tapaaminen on palkinto lopussa. Meillä se menee toisin päin.',

  // The two routes, drawn as chips. Each step is one word, because the point is
  // the length of the chain rather than what any link in it contains.
  'diff.old.label': 'Muualla',
  'diff.old.body':
    'Hiot profiilia, selaat päiviä, chattailet viikkoja. Suurin osa keskusteluista hiipuu ennen kuin kukaan ehdottaa mitään.',
  'diff.old.one': 'Profiili',
  'diff.old.two': 'Selailu',
  'diff.old.three': 'Chat',
  'diff.old.four': 'Ehkä treffit',

  'diff.new.label': 'Pilkkeessä',
  'diff.new.body':
    'Vastaa pariin kysymyssarjaan ja merkitse kalenteriin sopivat ajat. Sen jälkeen tapaat ihmisiä. Tunnissa kahvilassa opit toisesta enemmän kuin kahdessa viikossa viestejä.',
  'diff.new.one': 'Kysymykset',
  'diff.new.two': 'Kalenteri',
  'diff.new.three': 'Treffit',

  'diff.learn.title': 'Ensimmäinen ei ole se oikea, eikä sen tarvitse olla',
  'diff.learn.body':
    'Harva ensimmäinen tapaaminen osuu kohdalleen. Se ei ole epäonnistuminen vaan alku. Kerro joka kerran jälkeen lyhyesti miten meni, niin seuraavat ehdotukset osuvat lähemmäs — ja huomaat samalla itsekin, mitä oikeastaan etsit.',

  'how.title': 'Näin se toimii',
  'how.more': 'Lue tarkemmin',

  'how.one.title': 'Lähetä treffikutsu',
  'how.one.body':
    'Avaa valikoima ja valitse, kenelle lähetät kutsun. Tarjoa pari sinulle sopivaa aikaa ja paikka. Kutsu lähtee.',
  'how.two.title': 'Vastaa saapuneisiin kutsuihin',
  'how.two.body':
    'Näet kutsujan, sen mitä teillä on yhteistä ja hänen tarjoamansa ajat. Valitse yksi, niin treffit on sovittu. Se ei maksa sinulle mitään.',
  'how.three.title': 'Menkää treffeille',
  'how.three.body':
    'Treffinäytöllä on aika, paikka ja kartta. Sovittuna hetkenä voitte näyttää sijaintinne toisillenne, jotta löydätte perille.',
  'how.four.title': 'Kerro miten meni',
  'how.four.body':
    'Sovellus kysyy lyhyesti, miten meni ja vastasiko toinen toiveitasi. Vastaa hetkessä, niin seuraavat ehdotukset osuvat paremmin.',
  'how.loop': 'Sitten kierros alkaa alusta — ja tiedämme sinusta enemmän kuin viime kerralla.',

  // The section between the loop and the safety cards. Its job is that both
  // halves of a date are somebody's decision: one person asks, one person
  // answers, and the app is built so that both are worth doing.
  'both.title': 'Kutsu, ja vastaa kutsuihin',
  'both.lead':
    'Treffit syntyvät vain jos joku kutsuu ja joku vastaa. Pilke on tehty niin, että molemmat kannattavat.',
  'both.invite.title': 'Kutsu ensin',
  'both.invite.body':
    'Kutsu on sovelluksen ainoa varsinainen teko. Valikoiman avaaminen kuluttaa terälehtiä, ja terälehtiä saa käyttämällä sovellusta. Rahalla niitä ei saa.',
  'both.answer.title': 'Vastaa kutsuun',
  'both.answer.body':
    'Kutsuun vastaaminen ei kuluta mitään. Kieltäydy vapaasti, siitä ei seuraa sinulle mitään. Kutsu on voimassa vuorokauden ja raukeaa itsestään, jos jätät sen.',
  'both.note':
    'Treffeillä käyminen ja palautteen antaminen tuovat terälehtiä, eli seuraavan kutsun. Määrät voivat muuttua betan aikana.',
  'both.more': 'Terälehdet ja koko kierto tarkemmin',

  // The safety block on the front page. Three short cards; the page at
  // `turvallisuus` carries the whole of it. The location card is here because it
  // is the most concrete thing this product can say and it says it in numbers.
  'safety.front.title': 'Turvallisuus ei ole lisäosa',
  'safety.front.lead':
    'Tuntemattoman tapaaminen on eri asia kuin viestittely. Siihen Pilkkeessä on kolme työkalua, ja ne kannattaa ottaa käyttöön ennen ensimmäisiä treffejä.',
  'safety.card.contact.title': 'Luotettava läheinen',
  'safety.card.contact.body':
    'Tallennat asetuksiin yhden numeron. Se on ainoa numero, johon sovellus voi lähettää viestin puolestasi.',
  'safety.card.button.title': 'Turvapainike',
  'safety.card.button.body':
    'Treffinäytöllä. Yksi painallus lähettää läheisellesi tekstiviestin: siinä on nimesi ja pyyntö ottaa yhteyttä. Se ei kerro sijaintiasi, treffipaikkaa eikä mitään toisesta osapuolesta.',
  'safety.card.places.title': 'Paikat valitsemme itse',
  'safety.card.places.body':
    'Treffipaikat eivät ole käyttäjien ehdotuksia. Jokainen niistä on julkinen paikka, jonka olemme itse valinneet: kahvila, ravintola tai muu tila, jossa on muita ihmisiä ympärillä.',

  // Forward-looking, and marked as such in the copy itself. It sits under the
  // cards rather than in one, because a card next to two shipped features reads
  // as a third shipped feature.
  'safety.future.title': 'Tulossa: vahva tunnistautuminen',
  'safety.future.body':
    'Haluamme varmistaa käyttäjien henkilöllisyyden suomalaisella vahvalla tunnistautumisella. Sitä ei ole vielä käytössä, emmekä lupaa sille päivämäärää.',

  'safety.title': 'Turvallisuus',
  'safety.contact.title': 'Luotettava läheinen',
  'safety.contact.body':
    'Voit tallentaa yhden puhelinnumeron asetusten Turvallisuus-kohdassa. Se on ainoa numero, johon sovellus voi lähettää viestin puolestasi.',
  'safety.button.title': 'Turvapainike',
  'safety.button.body':
    'Turvapainike näkyy treffinäytöllä, kun olet tallentanut luotettavan läheisen numeron. Yksi painallus lähettää hänelle tekstiviestin. Ilman tallennettua numeroa painiketta ei ole, joten aseta numero etukäteen. Viestissä on nimesi ja se, että painoit painiketta ja pyydät yhteydenottoa. Se ei kerro sijaintiasi, treffipaikkaa, kellonaikaa eikä mitään toisesta osapuolesta. Toinen osapuoli ei saa tietää painalluksesta mitään.',
  'safety.report.title': 'Ilmoitus',
  'safety.report.body':
    'Jos jokin ei mennyt niin kuin sen olisi pitänyt, voit kertoa siitä treffien jälkeen omin sanoin. Ilmoitus jää talteen Pilkkeen väelle luettavaksi. Emme lupaa vielä, kuinka nopeasti joku sen lukee.',

  'tips.title': 'Näin tapaat turvallisesti',
  'tips.lead':
    'Nämä eivät ole Pilkkeen erityispiirteitä vaan tavallista järkeä, joka on helppo unohtaa jännittävänä iltana.',
  'tips.one': 'Aseta luotettavan läheisen numero ennen ensimmäisiä treffejä.',
  'tips.two': 'Kerro jollekin minne menet ja milloin arvioit olevasi kotona.',
  'tips.three': 'Valitse ensimmäisille treffeille paikka, jossa on muita ihmisiä.',
  'tips.four': 'Järjestä oma kulkeminen molempiin suuntiin.',
  'tips.five': 'Pidä puhelin ladattuna.',
  'tips.six':
    'Jos olo on epämukava, lähde. Sinun ei tarvitse selittää sitä kenellekään, ei meillekään.',

  'privacy.title': 'Sijainti ja yksityisyys',

  // Two paragraphs, because these are two different things and conflating them is
  // how the earlier version came to claim something the app does not do. The area
  // is a choice on a map; the position is a permission during a date.
  'privacy.area':
    'Pilke ei kysy kotiosoitettasi eikä sitä, missä asut. Valitset kartalta alueen ja sen, kuinka kauas voisit lähteä treffeille, ja treffipaikkoja ehdotetaan tuon ympyrän sisältä.',
  'privacy.body':
    'Laitteesi sijaintia luetaan vain treffeillä ja vain jos itse valitset näyttää sen. Näyttäminen toimii kymmenen minuuttia sovitun alkamisajan molemmin puolin ja vain 300 metrin säteellä treffipaikasta, joten kotoa sinua ei voi paikantaa. Sijainnin näkee vain toinen osapuoli, ei luotettava läheisesi. Se poistetaan heti kun aika umpeutuu, eikä sitä käytetä mihinkään muuhun: se ei vaikuta hyvityksiin, hidastuksiin eikä ilmoituksiin. Voit lopettaa näyttämisen milloin tahansa.',

  'safety.more': 'Lue turvallisuudesta',
  'safety.page.lead':
    'Tapaaminen tuntemattoman kanssa on eri asia kuin viestittely. Tällä sivulla on se, mitä Pilke tekee asian eteen, ja se mitä kannattaa itse tehdä.',

  // The detail page. Every number here is the backend's own constant, and the
  // README records which.
  'detail.title': 'Näin Pilke toimii',
  'detail.lead':
    'Etusivu kertoo kierron neljässä vaiheessa. Tällä sivulla on sama tarkemmin: mistä ehdokkaat tulevat, mistä terälehdet tulevat ja mitä tapahtuu kun suunnitelmat muuttuvat.',

  'detail.start.title': 'Ennen ensimmäistä kutsua',
  'detail.start.body':
    'Rekisteröinti alkaa puhelinnumerosta ja tekstiviestillä tulevasta koodista. Sen jälkeen annat kutsumanimen, syntymäpäivän ja kuvan.',
  'detail.story.title': 'Tarinatesti',
  'detail.story.body':
    'Neljätoista tilannetta, joissa valitset mitä tekisit. Yksi kysymys kerrallaan, ja voit jatkaa myöhemmin siitä mihin jäit. Kysymyssarjoihin voit vastata omaan tahtiisi myös myöhemmin.',
  'detail.prefs.title': 'Toiveet ja kalenteri',
  'detail.prefs.body':
    'Kerrot kenen kanssa haluat tavata, minkä ikäisiä ehdokkaita otat vastaan ja millaisia treffejä etsit. Kartalta valitset, kuinka kauas lähdet. Lopuksi merkitset kalenteriin ajat, jolloin sinulle sopii: vähintään yksi tunnin mittainen aika tarvitaan, jotta sinulle voi ehdottaa ketään.',

  'detail.draw.title': 'Mistä ehdokkaat tulevat',
  'detail.draw.body':
    'Kun avaat valikoiman, Pilke etsii ihmisiä, joiden toiveet ja sinun toiveesi käyvät yksiin, joilla on kalenterissa vähintään tunnin yhteinen aika sinun kanssasi, ja joiden kanssa on paikka johon molemmat pääsevät. Sinä valitset, kenelle kutsu lähtee.',
  'detail.invite.title': 'Kutsu ja vastaus',
  'detail.invite.body':
    'Tarjoat vähintään kaksi aikaa ja yhden tekemisen. Toinen valitsee niistä yhden, ja treffit on sovittu. Kutsu on voimassa vuorokauden.',

  'detail.economy.title': 'Terälehdet',
  'detail.economy.body':
    'Terälehti on se, mitä keräät ja käytät. Viisi terälehteä tekee ruusun, ja ruusu avaa valikoiman. Muuta hintaa ei ole. Terälehtiä ei myydä.',
  'detail.economy.earn': 'Näin terälehtiä kertyy',
  'detail.earn.signup': 'Rekisteröinnin viimeistely',
  'detail.earn.signup.note': 'Kerran tilin elinkaaressa, koodin vahvistamisen jälkeen.',
  'detail.earn.calendar': 'Kolme kalenteriin merkittyä aikaa',
  'detail.earn.calendar.note':
    'Jokaisen ajan on oltava vähintään tunnin mittainen, eivätkä ajat saa olla päällekkäisiä.',
  'detail.earn.date': 'Käydyt treffit',
  'detail.earn.date.note':
    'Maksetaan, kun olet kertonut miten meni. Molemmat saavat omansa erikseen.',
  'detail.earn.cancelled': 'Jos toinen perui sovitut treffit',
  'detail.earn.cancelled.note':
    'Hyvitys sinulle. Jos olit kutsun lähettäjä, saat lisäksi terälehtesi takaisin.',

  'detail.economy.spend': 'Näin terälehdet kuluvat',
  'detail.economy.spend.body':
    'Viisi terälehteä kuluu sillä hetkellä, kun avaat valikoiman. Kutsun lähettäminen ei maksa enää mitään. Terälehtiä voi ansaita viisitoista kerrallaan, eli kolmen treffikutsun verran: kun raja tulee vastaan, ansaitut terälehdet odottavat, kunnes käytät niitä. Hyvitykset, kuten rauenneen kutsun palautus, tulevat perille rajasta riippumatta.',

  'detail.changes.title': 'Jos suunnitelmat muuttuvat',
  'detail.changes.expired': 'Kutsuun ei vastata vuorokaudessa',
  'detail.changes.expired.note': 'Kutsu raukeaa itsestään ja saat terälehtesi takaisin.',
  'detail.changes.declined': 'Kutsu hylätään',
  'detail.changes.declined.note':
    'Saat terälehtesi takaisin. Hylkääminen on aina ilmaista, eikä siitä seuraa hylkääjälle mitään.',
  'detail.changes.withdrawn': 'Perut oman kutsusi',
  'detail.changes.withdrawn.note':
    'Terälehdet on käytetty, ja uuden valikoiman avaaminen odottaa hetken.',
  'detail.changes.canceled': 'Sovitut treffit perutaan',
  'detail.changes.canceled.note':
    'Peruminen onnistuu, ja jos treffit eivät tunnu oikeilta, pääset pois ilman seurauksia. Toistuva peruminen hidastaa uusien ehdokkaiden saamista.',

  'detail.chat.title': 'Miksi chattia ei ole',
  'detail.chat.body':
    'Kutsussa on jo aika ja paikka, joten sopimiseen ei tarvita keskustelua. Se on koko idea: Pilke vie teidät samaan pöytään sen sijaan, että korvaisi sen. Treffipäivänä kartta kertoo, missä toinen on, jotta löydätte perille ilman viestittelyä.',

  'economy.lead': 'Viisi terälehteä avaa valikoiman.',
  'economy.rose.alt': 'Ruusu, jonka kaikki viisi terälehteä on kerätty.',
  'economy.amount.one': '1 terälehti',
  'economy.amount.two': '2 terälehteä',
  'economy.amount.five': '5 terälehteä',

  // The waitlist. TODO(pilke-web): the form posts nowhere yet — see README.
  'cta.title': 'Pilke on suljetussa betassa',
  'cta.body': 'Jätä sähköpostiosoitteesi, niin kerromme heti kun pääset mukaan.',
  'cta.label': 'Sähköpostiosoite',
  'cta.placeholder': 'sina@esimerkki.fi',
  'cta.button': 'Liity betaan',
  'cta.note': 'Käytämme osoitetta vain betakutsuun. Emme lähetä muuta emmekä anna sitä eteenpäin.',
  // The link this form may not collect an address without. Its own key rather
  // than a clause inside `cta.note`, so the promise and the document that has to
  // back it up are not one sentence somebody has to re-translate together.
  'cta.privacy': 'Lue tietosuojaselosteesta, mitä osoitteellesi tapahtuu.',

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
    'Puhelinnumeroasi ei näytetä kenellekään. Ehdokas näkee nimesi, kuvasi ja sen, mitä teillä on yhteistä.',
  'faq.safety.q': 'Näkeekö toinen, missä olen?',
  'faq.safety.a':
    'Vain jos valitset niin. Sijainti näkyy kymmenen minuuttia sovitun alun molemmin puolin ja vain 300 metrin säteellä treffipaikasta, ja voit lopettaa näyttämisen milloin tahansa. Se poistetaan kun aika umpeutuu, eikä sitä käytetä mihinkään muuhun.',
  'faq.cost.q': 'Mitä se maksaa?',
  'faq.cost.a':
    'Betavaiheessa ei mitään. Terälehtiä ei voi ostaa, vaan niitä kertyy käyttämällä sovellusta.',
  'faq.cancel.q': 'Entä jos treffit peruuntuvat?',
  'faq.cancel.a':
    'Kutsun hylkääminen on aina ilmaista eikä siitä seuraa mitään. Sovitun tapaamisen voi perua sovelluksessa, ja jos treffit eivät tunnu oikeilta, pääset pois ilman seurauksia. Toistuva peruminen tai saapumatta jättäminen hidastaa uusien ehdokkaiden saamista, koska se on toiselle osapuolelle merkityksellistä.',
  'faq.delete.q': 'Voinko poistaa tilini?',
  'faq.delete.a':
    'Kyllä, asetuksista. Nimesi, kuvasi ja yhteystietosi poistetaan heti. Menneet treffit ja niistä annetut palautteet jäävät talteen, koska ne ovat yhtä lailla toisen osapuolen tietoja.',

  'shot.treffit':
    'Pilkkeen etusivu puhelimessa: terälehtien määrä ylhäällä, alla omat treffit ja saapuneet kutsut.',
  'shot.kalenteri': 'Kalenterinäkymä, jossa viikon päivät ja niihin merkityt vapaat treffiajat.',
  'shot.story':
    'Tarinatestin ensimmäinen kysymys onboardingissa: tilanne ja kolme vaihtoehtoa, joista valitaan yksi.',
  'shot.platter':
    'Ehdokkaat-näkymä: yksi ehdokas, hänen kanssaan yhteiset ajat ja valittu tekeminen.',
  'shot.invitation': 'Saapunut treffikutsu: kutsujan nimi ja kuva, tarjotut ajat ja paikka.',
  'shot.feedback':
    'Treffipalaute puhelimessa: kuka oli treffeillä, milloin, ja ensimmäinen kysymys vastausvaihtoehtoineen.',
  'shot.asetukset':
    'Asetusten Turvallisuus-osio avattuna, ja siinä kenttä luotettavan henkilön numerolle.',
  'shot.date': 'Sovitut treffit puhelimessa: aika, paikka kartalla ja turvapainike.',

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
    'Esto, joka syntyy kun joku ei ole kokenut oloaan turvalliseksi. Sitä ei voi purkaa lähtemällä.',
  'legal.deletion.kept.five': 'Ilmoitukset saapumatta jättämisestä, molempiin suuntiin.',
  'legal.deletion.kept.six': 'Terälehtien liikkeet, jotta saldot pysyvät täsmäävinä.',
  'legal.deletion.kept.seven':
    'Käynnissä oleva hidastus, jos sinulla on sellainen. Lähteminen ei lyhennä sitä.',
  'legal.deletion.kept.eight':
    'Ketkä ehdokkaat sinulle on tarjottu, ja keiden ehdokkaissa olet ollut.',
  'legal.deletion.kept.nine':
    'Virhe- ja suorituskykytiedot, joissa on tilisi numero. Ne eivät poistu tilin mukana, vaan häviävät itsestään 30 päivän kuluessa.',

  'legal.deletion.others.title': 'Mitä tapahtuu sovituille treffeille',
  'legal.deletion.others.body':
    'Lähettämäsi kutsut perutaan ja saamasi kutsut hylätään, ja kutsujan terälehdet palautetaan. Tulevat treffit peruutetaan, ja toinen osapuoli hyvitetään kuten missä tahansa perumisessa. Sinulle ei tule tästä seurauksia, emmekä kerro kenellekään erikseen, että lähdit.',

  'legal.deletion.again.title': 'Jos palaat myöhemmin',
  'legal.deletion.again.body':
    'Voit rekisteröityä samalla puhelinnumerolla uudelleen. Saat tyhjän tilin, eikä mikään yhdistä sitä vanhaan.',

  'legal.deletion.more': 'Lue tarkemmin tietosuojaselosteesta',

  'footer.rights': 'Pilke',
} as const;

const en: Record<keyof typeof fi, string> = {
  'meta.title': 'Pilke',
  'meta.description':
    'Pilke is a Finnish dating app with no chat. An invitation arrives with the time and place already in it, and you go on the date.',

  'nav.how': 'How it works',
  'nav.safety': 'Safety',
  'nav.questions': 'Questions',
  'nav.language': 'Language',
  'nav.skip': 'Skip to content',
  'nav.back': 'Back to the front page',

  'hero.title': 'Dates, not swiping',
  'hero.lead':
    'No chat, no weeks of messaging. You get an invitation with the time and the place already in it — pick the hour that suits you, and the date is set.',

  'fact.one.title': 'You choose who to invite',
  'fact.one.body': 'No endless stack to scroll.',
  'fact.two.title': 'Time and place already set',
  'fact.two.body': 'Your calendar does the arranging.',
  'fact.three.title': 'Nothing to game',
  'fact.three.body': 'No visibility to buy, no boosts.',

  'diff.title': 'Why this is different',
  'diff.lead':
    'Other apps taught us that getting to know somebody happens on a screen, and that meeting them is the prize at the end. Here it goes the other way round.',

  'diff.old.label': 'Elsewhere',
  'diff.old.body':
    'You polish a profile, scroll for days, chat for weeks. Most of those conversations fade before anybody suggests anything.',
  'diff.old.one': 'Profile',
  'diff.old.two': 'Scrolling',
  'diff.old.three': 'Chat',
  'diff.old.four': 'Maybe a date',

  'diff.new.label': 'On Pilke',
  'diff.new.body':
    'Answer a couple of question sets and mark the times that suit you. After that you meet people. You learn more in an hour at a cafe than in two weeks of messages.',
  'diff.new.one': 'Questions',
  'diff.new.two': 'Calendar',
  'diff.new.three': 'A date',

  'diff.learn.title': 'The first one is not the one, and it does not have to be',
  'diff.learn.body':
    'Few first meetings land perfectly. That is a beginning, not a failure. Say briefly how each one went and the next suggestions land closer — and you notice what you are actually looking for.',

  'how.title': 'How it works',
  'how.more': 'Read more',

  'how.one.title': 'Send a date invitation',
  'how.one.body':
    'Open a set and choose who to invite. Offer a couple of times that suit you, and a place. The invitation goes.',
  'how.two.title': 'Answer the invitations you get',
  'how.two.body':
    'You see who sent it, what you have in common, and the times they offer. Pick one, and the date is set. It costs you nothing.',
  'how.three.title': 'Go on the date',
  'how.three.body':
    'The date screen carries the time, the place and a map. At the agreed hour you can show each other your locations so you actually find one another.',
  'how.four.title': 'Say how it went',
  'how.four.body':
    'The app asks briefly how it went and whether the other person matched what you hoped for. Answer in a moment, and the next suggestions fit better.',
  'how.loop': 'Then it starts again — and we know more about you than we did last time.',

  'both.title': 'Invite, and answer invitations',
  'both.lead':
    'A date happens only if somebody asks and somebody answers. Pilke is built so that both are worth doing.',
  'both.invite.title': 'Invite first',
  'both.invite.body':
    'An invitation is the one real action in the app. Opening a set spends petals, and petals come from using the app. Money does not buy them.',
  'both.answer.title': 'Answer an invitation',
  'both.answer.body':
    'Answering costs you nothing. Turn one down freely, and nothing follows for you. An invitation stands for a day and lapses by itself if you leave it.',
  'both.note':
    'Going on dates and giving feedback earn petals, which is your next invitation. The amounts may change during the beta.',
  'both.more': 'Petals and the whole loop in detail',

  'safety.front.title': 'Safety is not an add-on',
  'safety.front.lead':
    'Meeting a stranger is a different thing from messaging one. Pilke has three tools for it, and they are worth setting up before your first date.',
  'safety.card.contact.title': 'A trusted person',
  'safety.card.contact.body':
    'You save one number in the settings. It is the only number the app can text on your behalf.',
  'safety.card.button.title': 'The safety button',
  'safety.card.button.body':
    'On the date screen. One press texts your trusted person: the message carries your name and a request to get in touch. It names no location, no venue and nothing about the person you are meeting.',
  'safety.card.places.title': 'We choose the places',
  'safety.card.places.body':
    'Date venues are not user suggestions. Every one of them is a public place we picked ourselves: a cafe, a restaurant, somewhere with other people around.',

  'safety.future.title': 'Coming: strong electronic identification',
  'safety.future.body':
    'We want to verify identities using Finnish strong electronic identification. It is not in the app yet, and we are not promising a date for it.',

  'safety.title': 'Safety',
  'safety.contact.title': 'A trusted person',
  'safety.contact.body':
    'You can save one phone number under Safety in the settings. It is the only number the app can text on your behalf.',
  'safety.button.title': 'The safety button',
  'safety.button.body':
    'The safety button appears on the date screen once you have saved a trusted person. One press texts them. Without a saved number there is no button, so set the number beforehand. The message carries your name and the fact that you pressed the button and are asking them to get in touch. It names no location, no venue, no time and nothing about the person you are meeting. The other party learns nothing about the press.',
  'safety.report.title': 'Reporting',
  'safety.report.body':
    'If something did not go the way it should have, you can say so after the date, in your own words. The report is kept for Pilke staff to read. We are not promising yet how quickly somebody gets to it.',

  'tips.title': 'Meeting somebody safely',
  'tips.lead':
    'None of this is particular to Pilke. It is ordinary sense, and easy to forget on a nervous evening.',
  'tips.one': 'Save a trusted person before your first date.',
  'tips.two': 'Tell somebody where you are going and when you expect to be home.',
  'tips.three': 'Pick somewhere with other people around for a first date.',
  'tips.four': 'Arrange your own way there and your own way back.',
  'tips.five': 'Keep your phone charged.',
  'tips.six':
    'If you feel uncomfortable, leave. You do not owe anybody an explanation for it, us included.',

  'privacy.title': 'Location and privacy',
  'privacy.area':
    'Pilke does not ask for your home address, or where you live at all. You choose an area on a map and how far you would travel for a date, and venues are suggested inside that circle.',
  'privacy.body':
    'Your device location is read only on a date, and only if you choose to show it. Sharing works for ten minutes either side of the agreed start and only within 300 metres of the venue, so you cannot be located from home. Only the other person sees it, not your trusted contact. It is deleted as soon as the window closes, and it is not used for anything else: it feeds no compensation, no slowdown and no report. You can stop at any time.',

  'safety.more': 'Read about safety',
  'safety.page.lead':
    'Meeting a stranger is a different thing from messaging one. This page covers what Pilke does about that, and what is worth doing yourself.',

  'detail.title': 'How Pilke works',
  'detail.lead':
    'The front page gives the loop in four steps. This page is the same thing in detail: where candidates come from, where petals come from, and what happens when plans change.',

  'detail.start.title': 'Before your first invitation',
  'detail.start.body':
    'Signing up starts with a phone number and a code by text. After that you give a name, a birthday and a photo.',
  'detail.story.title': 'The story test',
  'detail.story.body':
    'Fourteen situations where you choose what you would do, one question at a time, and you can pick up where you left off. The question sets are there to answer at your own pace later on.',
  'detail.prefs.title': 'Preferences and calendar',
  'detail.prefs.body':
    'You say who you want to meet, what ages you will consider and what kind of date you are looking for. On a map you set how far you will travel. Then you mark the times that suit you: at least one hour-long slot is needed before anybody can be suggested to you.',

  'detail.draw.title': 'Where candidates come from',
  'detail.draw.body':
    'When you open a set, Pilke looks for people whose preferences and yours agree, who share at least an hour of calendar time with you, and who have somewhere to meet that you can both reach. You choose which of them the invitation goes to.',
  'detail.invite.title': 'The invitation and the answer',
  'detail.invite.body':
    'You offer at least two times and one thing to do. The other person picks one of them, and the date is set. An invitation stands for a day.',

  'detail.economy.title': 'Petals',
  'detail.economy.body':
    'A petal is what you collect and what you spend. Five petals make a rose, and a rose opens a set. There is no other price. Petals are not sold.',
  'detail.economy.earn': 'How petals add up',
  'detail.earn.signup': 'Finishing your registration',
  'detail.earn.signup.note': 'Once in the life of an account, after the code is confirmed.',
  'detail.earn.calendar': 'Three times marked in your calendar',
  'detail.earn.calendar.note':
    'Each has to be at least an hour long, and they cannot overlap each other.',
  'detail.earn.date': 'A date you went on',
  'detail.earn.date.note': 'Paid once you have said how it went. Each of you gets your own.',
  'detail.earn.cancelled': 'If the other person calls off an agreed date',
  'detail.earn.cancelled.note':
    'Compensation for you. If you were the one who invited, you also get your petals back.',

  'detail.economy.spend': 'How petals go',
  'detail.economy.spend.body':
    'Five petals go the moment you open a set. Sending the invitation costs nothing more. You can earn fifteen at a time, which is three invitations worth: once you reach that, what you have earned waits until you spend some. Reimbursements, such as the petals returned when an invitation lapses, arrive regardless of the limit.',

  'detail.changes.title': 'If plans change',
  'detail.changes.expired': 'An invitation goes unanswered for a day',
  'detail.changes.expired.note': 'It lapses by itself and your petals come back.',
  'detail.changes.declined': 'An invitation is turned down',
  'detail.changes.declined.note':
    'Your petals come back. Turning one down is always free and costs the person doing it nothing.',
  'detail.changes.withdrawn': 'You withdraw your own invitation',
  'detail.changes.withdrawn.note':
    'The petals are spent, and opening a new set waits a little while.',
  'detail.changes.canceled': 'An agreed date is called off',
  'detail.changes.canceled.note':
    'You can do it, and if the date does not feel right you can get out with nothing to pay. Calling off repeatedly slows down how soon you get new candidates.',

  'detail.chat.title': 'Why there is no chat',
  'detail.chat.body':
    'An invitation already carries the time and the place, so arranging it needs no conversation. That is the whole idea: Pilke takes you to the same table rather than standing in for it. On the day, the map shows where the other person is so you find each other without messaging.',

  'economy.lead': 'Five petals open a set.',
  'economy.rose.alt': 'A rose with all five of its petals collected.',
  'economy.amount.one': '1 petal',
  'economy.amount.two': '2 petals',
  'economy.amount.five': '5 petals',

  'cta.title': 'Pilke is in closed beta',
  'cta.body': 'Leave your email address and we will tell you as soon as you can get in.',
  'cta.label': 'Email address',
  'cta.placeholder': 'you@example.com',
  'cta.button': 'Join the beta',
  'cta.note':
    'We use the address for the beta invitation and nothing else. We do not pass it on.',
  'cta.privacy': 'The privacy policy says what happens to your address.',
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
    'Your phone number is never shown to anybody. A candidate sees your name, your photo and what the two of you have in common.',
  'faq.safety.q': 'Can the other person see where I am?',
  'faq.safety.a':
    'Only if you choose to show them. It runs for ten minutes either side of the agreed start and only within 300 metres of the venue, and you can stop at any time. It is deleted when the window closes, and nothing else reads it.',
  'faq.cost.q': 'What does it cost?',
  'faq.cost.a':
    'Nothing during the beta. Petals cannot be bought; they come from using the app.',
  'faq.cancel.q': 'What if a date falls through?',
  'faq.cancel.a':
    'Turning down an invitation is always free and carries no consequence. You can call off a date you agreed to, and if it does not feel right you can get out with nothing to pay. Cancelling repeatedly or not turning up slows down how soon you get new candidates, because that matters to the person on the other side.',
  'faq.delete.q': 'Can I delete my account?',
  'faq.delete.a':
    'Yes, from the settings. Your name, photo and contact details go straight away. Past dates and the feedback written about them stay, because those belong to the other person as much as to you.',

  'shot.treffit':
    'The Pilke home screen on a phone: your petals along the top, your dates and the invitations you have received below.',
  'shot.kalenteri':
    'The calendar view, with the days of the week and the times marked as free.',
  'shot.story':
    'The first question of the story test during onboarding: a situation and three options, one of which you pick.',
  'shot.platter':
    'The candidates view: one candidate, the times you both have, and the chosen activity.',
  'shot.invitation':
    'A date invitation received: who sent it, with their photo, the times offered and the place.',
  'shot.feedback':
    'Date feedback on a phone: who the date was with, when it was, and the first question with its options.',
  'shot.asetukset':
    'The Safety section of the settings, open, with the field for a trusted person’s number.',
  'shot.date': 'An agreed date on a phone: the time, the venue on a map, and the safety button.',

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
    'The block created when somebody did not feel safe. Leaving does not lift it.',
  'legal.deletion.kept.five': 'Reports of not turning up, in both directions.',
  'legal.deletion.kept.six': 'Petal movements, so that balances still add up.',
  'legal.deletion.kept.seven':
    'Any slowdown you are currently serving. Leaving does not shorten it.',
  'legal.deletion.kept.eight':
    'Which candidates you were offered, and whose candidates you appeared among.',
  'legal.deletion.kept.nine':
    'Error and performance records, which carry your account number. They do not go with the account, but clear on their own within 30 days.',

  'legal.deletion.others.title': 'What happens to dates you agreed to',
  'legal.deletion.others.body':
    'Invitations you sent are withdrawn and invitations you received are declined, with the sender’s petals refunded. Dates still ahead are cancelled and the other person is compensated exactly as for any cancellation. Nothing is held against you, and nobody is told separately that you left.',

  'legal.deletion.again.title': 'If you come back later',
  'legal.deletion.again.body':
    'You can register the same phone number again. You get an empty account, and nothing links it to the old one.',

  'legal.deletion.more': 'Read the detail in the privacy policy',

  'footer.rights': 'Pilke',
};

export const ui = { fi, en } as const;

export type UiKey = keyof typeof fi;

/** Returns a lookup that falls back to Finnish, so a gap is visible, not blank. */
export function useTranslations(lang: Lang) {
  return function t(key: UiKey): string {
    return ui[lang][key] ?? ui[defaultLang][key];
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
