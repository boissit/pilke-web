/**
 * Single cards cut out of the app: three candidates from a platter and two agreed
 * dates from their date pages, in each language.
 *
 * Each is a real still of the app, cut to the card's outer ink rule with the corners
 * outside it transparent, so a page can lay them out like objects (fanned, tilted,
 * over a map) without redrawing any of the app's UI. How they are taken and cut is
 * `docs/pictures.md`, "Cards cut out of the app"; `scripts/cards/` has the tools.
 */
import arttuEn from './cards/en/candidate-arttu.png';
import veeraEn from './cards/en/candidate-veera.png';
import veetiEn from './cards/en/candidate-veeti.png';
import henriEn from './cards/en/date-henri.png';
import riikkaEn from './cards/en/date-riikka.png';
import arttuFi from './cards/fi/candidate-arttu.png';
import veeraFi from './cards/fi/candidate-veera.png';
import veetiFi from './cards/fi/candidate-veeti.png';
import henriFi from './cards/fi/date-henri.png';
import riikkaFi from './cards/fi/date-riikka.png';

const cards = {
  fi: { arttu: arttuFi, veeti: veetiFi, veera: veeraFi, riikka: riikkaFi, henri: henriFi },
  en: { arttu: arttuEn, veeti: veetiEn, veera: veeraEn, riikka: riikkaEn, henri: henriEn },
} as const;

/** The cards in a page's language. */
export function cardsFor(lang: 'fi' | 'en') {
  return cards[lang];
}
