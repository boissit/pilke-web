/**
 * Every string on the site, in both languages.
 *
 * Finnish is the product's language and the one written first; English is a full
 * translation rather than a fallback set, so a key missing from `en` is a type
 * error here in the same way it is in the app's own dictionaries.
 *
 * Product vocabulary is the app's own spelling: teralehdet and ruusut are what
 * the product calls its two currencies, and the site should not invent softer
 * words for them.
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
    'Pilke on suomalainen deittisovellus, joka tekee yhden asian: sopii teille oikeat treffit oikeaan aikaan.',

  'nav.how': 'Näin se toimii',
  'nav.safety': 'Turvallisuus',
  'nav.questions': 'Kysyttyä',
  'nav.language': 'Kieli',
  'nav.skip': 'Siirry sisältöön',

  'hero.title': 'Treffit, ei swaippailua',
  'hero.lead':
    'Pilke etsii teille yhteisen ajan ja paikan, ja sitten te menette sinne. Ei viestiketjuja, jotka hiipuvat kolmen päivän jälkeen. Ei selailua illasta toiseen.',
  'hero.note': 'Sovellus on suljetussa betavaiheessa.',

  'promise.title': 'Kolme lupausta',
  'promise.one.title': 'Kolme ehdokasta kerrallaan',
  'promise.one.body':
    'Saat kolme ehdokasta, joiden kanssa sinulla on vapaa hetki samaan aikaan ja paikka, johon molemmat pääsevät. Valitset yhden.',
  'promise.two.title': 'Aika ja paikka valmiina',
  'promise.two.body':
    'Kalenterisi kertoo, milloin voit. Kutsussa on jo ajankohta ja paikka, joten sopimista ei tarvitse käydä erikseen läpi.',
  'promise.three.title': 'Kasvokkain, ei ruudun takana',
  'promise.three.body':
    'Pilkkeessä ei ole chattia. Se on tarkoituksellista: sovellus vie teidät samaan pöytään sen sijaan, että korvaisi sen.',

  'how.title': 'Näin se toimii',
  'how.lead': 'Viisi vaihetta rekisteröinnistä ensimmäisille treffeille.',

  'how.one.title': 'Kerro kuka olet',
  'how.one.body':
    'Puhelinnumero ja vahvistuskoodi, nimi ja kuva. Numeroasi ei näytetä kenellekään.',
  'how.two.title': 'Käy tarinatesti',
  'how.two.body':
    'Neljätoista tilannetta, joissa valitset mitä tekisit. Ei asteikkoja yhdestä viiteen. Kysymyksiin vastaaminen ei toistaiseksi vaikuta ehdokkaisiin.',
  'how.three.title': 'Aseta toiveet ja kalenteri',
  'how.three.body':
    'Kenen kanssa, millaisia treffejä, millä alueella. Sitten merkitset kalenteriin ajat, jolloin sinulle sopii.',
  'how.four.title': 'Valitse ehdokas',
  'how.four.body':
    'Ruusu ostaa kolmen ehdokkaan valikoiman. Valitset yhden, valitset yhteisen ajan ja tekemisen, ja lähetät kutsun.',
  'how.five.title': 'Menkää treffeille',
  'how.five.body':
    'Kun kutsu on hyväksytty, treffit ovat sovitut. Jälkeenpäin kerrot miten meni, ja samalla terälehdet maksetaan.',

  'economy.title': 'Terälehdet ja ruusut',
  'economy.lead': 'Viisi terälehteä on yksi ruusu, ja ruusulla avaat kolmen ehdokkaan valikoiman.',
  'economy.earn.title': 'Näin terälehdet kertyvät',
  'economy.spend.title': 'Näin ruusu kuluu',
  'economy.spend.body':
    'Ruusu kuluu sillä hetkellä, kun avaat valikoiman. Kutsun lähettäminen ei maksa enää mitään.',
  'economy.earn.calendar': 'Kolme kalenteriin merkittyä treffiaikaa',
  'economy.earn.date': 'Treffit, kun olet kertonut miten meni',
  'economy.earn.signup': 'Rekisteröinnin viimeistely',
  'economy.amount.one': '1 terälehti',
  'economy.amount.two': '2 terälehteä',
  'economy.amount.five': '5 terälehteä',
  'economy.note':
    'Terälehtiä voi kerätä kerrallaan viidentoista asti. Määrät voivat muuttua betavaiheen aikana.',

  'safety.title': 'Turvallisuus',
  'safety.lead':
    'Tapaaminen tuntemattoman kanssa on eri asia kuin viestittely. Pilkkeessä on siihen kolme työkalua, ja ne kannattaa ottaa käyttöön ennen ensimmäisiä treffejä.',

  'safety.contact.title': 'Luotettava läheinen',
  'safety.contact.body':
    'Voit tallentaa yhden puhelinnumeron asetusten Turvallisuus-kohdassa. Se on ainoa numero, johon sovellus voi lähettää viestin puolestasi.',
  'safety.button.title': 'Turvapainike',
  'safety.button.body':
    'Näkyy treffinäytöllä, kun olet tallentanut luotettavan läheisen numeron. Yksi painallus lähettää hänelle tekstiviestin. Ilman tallennettua numeroa painiketta ei ole, joten aseta numero etukäteen. Viesti kertoo, että painoit painiketta ja pyydät yhteydenottoa. Se ei sisällä sijaintiasi eikä toisen osapuolen tietoja.',
  'safety.report.title': 'Ilmoitus',
  'safety.report.body':
    'Voit kertoa treffien jälkeen, jos olosi oli turvaton. Voit kirjoittaa omin sanoin mitä tapahtui, ja ilmoitus jää talteen Pilkkeen väelle luettavaksi. Emme lupaa vielä, kuinka nopeasti joku sen lukee.',

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
  'privacy.body':
    'Pilke kysyy suunnilleen missä asut, jotta se voi ehdottaa paikkoja joihin molemmat pääsevät. Sijainnin näyttäminen treffeillä on erikseen valittava, ja se toimii vain noin kymmenen minuuttia sovitun alkamisajan molemmin puolin ja vain treffipaikan lähellä. Sijainti näkyy ainoastaan toiselle osapuolelle, ei meille eikä luotettavalle läheiselle, ja se poistetaan heti kun aika umpeutuu. Voit lopettaa näyttämisen milloin tahansa.',

  'faq.title': 'Kysyttyä',
  'faq.chat.q': 'Voiko sovelluksessa viestitellä?',
  'faq.chat.a':
    'Ei, eikä se ole puute. Kutsussa on aika ja paikka, joten sopiminen ei vaadi keskustelua. Loput sanotaan kasvokkain.',
  'faq.who.q': 'Kuka näkee tietoni?',
  'faq.who.a':
    'Puhelinnumeroasi ei näytetä kenellekään. Ehdokas näkee nimesi, kuvasi ja sen, mitä teillä on yhteistä.',
  'faq.cost.q': 'Mitä se maksaa?',
  'faq.cost.a':
    'Betavaiheessa ei mitään. Terälehdet ja ruusut kerääntyvät käyttämällä sovellusta.',
  'faq.cancel.q': 'Entä jos treffit peruuntuvat?',
  'faq.cancel.a':
    'Kutsun hylkääminen on aina ilmaista, eikä siitä seuraa mitään. Sovitun tapaamisen peruminen onnistuu myös, ja toistuva peruminen tai paikalle saapumatta jättäminen hidastaa uusien ehdokkaiden saamista, koska se on toisen osapuolen kannalta merkityksellistä. Jos olosi ei ole turvallinen, pääset pois ilman seurauksia.',
  'faq.delete.q': 'Voinko poistaa tilini?',
  'faq.delete.a':
    'Kyllä, asetuksista. Nimesi, kuvasi ja yhteystietosi poistetaan heti. Menneet treffit ja niistä annetut palautteet jäävät talteen, koska ne ovat yhtä lailla toisen osapuolen tietoja.',

  'shot.treffit': 'Pilkkeen etusivu puhelimessa: ruusujen ja terälehtien määrä ylhäällä, alla omat treffit ja saapuneet kutsut.',
  'shot.kalenteri': 'Kalenterinäkymä, jossa viikon päivät ja niihin merkityt vapaat treffiajat.',
  'shot.story': 'Tarinatestin ensimmäinen kysymys onboardingissa: tilanne ja kolme vaihtoehtoa, joista valitaan yksi.',
  'shot.platter': 'Ehdokkaat-näkymä: yksi kolmesta ehdokkaasta, hänen kanssaan yhteiset ajat ja valittu tekeminen.',
  'shot.asetukset': 'Asetusten Turvallisuus-osio avattuna, ja siinä kenttä luotettavan henkilön numerolle.',
  'shot.date': 'Sovitut treffit puhelimessa: aika, paikka kartalla ja turvapainike.',

  'safety.summary': 'Voit tallentaa yhden luotettavan läheisen numeron, ja treffinäytöllä on turvapainike, joka lähettää hänelle tekstiviestin. Treffien jälkeen voit kertoa, jos olosi oli turvaton.',
  'safety.more': 'Lue turvallisuudesta',
  'safety.page.lead': 'Tapaaminen tuntemattoman kanssa on eri asia kuin viestittely. Tällä sivulla on se, mitä Pilke tekee asian eteen, ja se mitä kannattaa itse tehdä.',
  'nav.back': 'Takaisin etusivulle',

  'footer.beta': 'Pilke on suljetussa betavaiheessa.',
  'footer.rights': 'Pilke',
} as const;

const en: Record<keyof typeof fi, string> = {
  'meta.title': 'Pilke',
  'meta.description':
    'Pilke is a Finnish dating app that does one thing: it arranges a date that suits you both, at a time you are both free.',

  'nav.how': 'How it works',
  'nav.safety': 'Safety',
  'nav.questions': 'Questions',
  'nav.language': 'Language',
  'nav.skip': 'Skip to content',

  'hero.title': 'Dates, not swiping',
  'hero.lead':
    'Pilke finds you a time and a place you can both make, and then you go. No message threads that fade after three days. No scrolling one evening into the next.',
  'hero.note': 'The app is in closed beta.',

  'promise.title': 'Three promises',
  'promise.one.title': 'Three candidates at a time',
  'promise.one.body':
    'You get three people who are free when you are and who can reach the same place as you. You pick one.',
  'promise.two.title': 'Time and place already settled',
  'promise.two.body':
    'Your calendar says when you are free. An invitation already carries the time and the venue, so there is no arranging to do.',
  'promise.three.title': 'Face to face, not through a screen',
  'promise.three.body':
    'Pilke has no chat. That is deliberate: the app takes you to the same table rather than standing in for it.',

  'how.title': 'How it works',
  'how.lead': 'Five steps from signing up to your first date.',

  'how.one.title': 'Say who you are',
  'how.one.body':
    'A phone number and a confirmation code, a name and a photo. Your number is never shown to anybody.',
  'how.two.title': 'Walk the story test',
  'how.two.body':
    'Fourteen situations where you choose what you would do. No scales from one to five. Answering does not affect your candidates yet.',
  'how.three.title': 'Set your preferences and your calendar',
  'how.three.body':
    'Who you want to meet, what kind of date, which area. Then you mark the times that suit you.',
  'how.four.title': 'Pick a candidate',
  'how.four.body':
    'A rose buys a set of three candidates. You pick one, pick a time and something to do, and send the invitation.',
  'how.five.title': 'Go on the date',
  'how.five.body':
    'Once the invitation is accepted, the date is set. Afterwards you say how it went, and that is also when your petals are paid.',

  'economy.title': 'Petals and roses',
  'economy.lead': 'Five petals are one rose, and a rose opens a set of three candidates.',
  'economy.earn.title': 'How petals add up',
  'economy.spend.title': 'How a rose goes',
  'economy.spend.body':
    'A rose goes the moment you open a set. Sending the invitation costs nothing more.',
  'economy.earn.calendar': 'Three times marked in your calendar',
  'economy.earn.date': 'A date, once you have said how it went',
  'economy.earn.signup': 'Finishing your registration',
  'economy.amount.one': '1 petal',
  'economy.amount.two': '2 petals',
  'economy.amount.five': '5 petals',
  'economy.note':
    'You can hold up to fifteen petals at a time. The amounts may change during the beta.',

  'safety.title': 'Safety',
  'safety.lead':
    'Meeting a stranger is a different thing from messaging one. Pilke has three tools for it, and they are worth setting up before your first date.',

  'safety.contact.title': 'A trusted person',
  'safety.contact.body':
    'You can save one phone number under Safety in the settings. It is the only number the app can text on your behalf.',
  'safety.button.title': 'The safety button',
  'safety.button.body':
    'It appears on the date screen once you have saved a trusted person. One press texts them. Without a saved number there is no button, so set the number beforehand. The message says that you pressed it and are asking them to get in touch. It carries no location and nothing about the person you are meeting.',
  'safety.report.title': 'Reporting',
  'safety.report.body':
    'After a date you can say that you felt unsafe. You can write what happened in your own words, and the report is kept for Pilke staff to read. We are not promising yet how quickly somebody gets to it.',

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
  'privacy.body':
    'Pilke asks roughly where you live so it can suggest places you can both reach. Showing your location on a date is a separate choice, it works only for about ten minutes either side of the agreed start, and only near the venue. It is visible to the other person alone, not to us and not to your trusted contact, and it is deleted as soon as the window closes. You can stop it at any time.',

  'faq.title': 'Questions',
  'faq.chat.q': 'Can I message people in the app?',
  'faq.chat.a':
    'No, and that is not a gap. An invitation carries the time and the place, so arranging it needs no conversation. The rest is said in person.',
  'faq.who.q': 'Who sees my details?',
  'faq.who.a':
    'Your phone number is never shown to anybody. A candidate sees your name, your photo and what the two of you have in common.',
  'faq.cost.q': 'What does it cost?',
  'faq.cost.a':
    'Nothing during the beta. Petals and roses are collected by using the app.',
  'faq.cancel.q': 'What if a date falls through?',
  'faq.cancel.a':
    'Turning down an invitation is always free and carries no consequence. You can also call off a date you agreed to, and cancelling repeatedly or not turning up slows down how soon you get new candidates, because that matters to the person on the other side. If you do not feel safe, you can get out with nothing to pay.',
  'faq.delete.q': 'Can I delete my account?',
  'faq.delete.a':
    'Yes, from the settings. Your name, photo and contact details go straight away. Past dates and the feedback written about them stay, because those belong to the other person as much as to you.',

  'shot.treffit': 'The Pilke home screen on a phone: your roses and petals along the top, your dates and the invitations you have received below.',
  'shot.kalenteri': 'The calendar view, with the days of the week and the times marked as free.',
  'shot.story': 'The first question of the story test during onboarding: a situation and three options, one of which you pick.',
  'shot.platter': 'The candidates view: one of three candidates, the times you both have, and the chosen activity.',
  'shot.asetukset': 'The Safety section of the settings, open, with the field for a trusted person\u2019s number.',
  'shot.date': 'An agreed date on a phone: the time, the venue on a map, and the safety button.',

  'safety.summary': 'You can save one trusted person, and the date screen has a safety button that texts them. After a date you can say if you felt unsafe.',
  'safety.more': 'Read about safety',
  'safety.page.lead': 'Meeting a stranger is a different thing from messaging one. This page covers what Pilke does about that, and what is worth doing yourself.',
  'nav.back': 'Back to the front page',

  'footer.beta': 'Pilke is in closed beta.',
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
