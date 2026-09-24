# Manual screenshots — the contract

This file is shared by three pieces of work: the capture pipeline in `pilke-app`, the page layout in this repo, and the manual text. Each still is named here once. Every piece refers to it by that name.

## Where a still lives

    src/assets/manual/fi/<name>.png
    src/assets/manual/fi/<name>.json
    src/assets/manual/en/<name>.png
    src/assets/manual/en/<name>.json

The sidecar `<name>.json`:

    {
      "name": "kalenteri-drag",
      "language": "fi",
      "commit": "<pilke-app HEAD sha, with -dirty if the tree was dirty>",
      "takenAt": "2026-09-24T12:00:00Z",
      "screen": { "width": 1080, "height": 2280 },
      "elements": { "<testID>": { "x": 0, "y": 0, "width": 0, "height": 0 } }
    }

Element bounds are in the PNG's own pixels. Only the testIDs listed under **Callouts** are required. Others may be present.

## How the text points at a still

A paragraph that contains only an image:

    ![Alt text in the page's language](shot:kalenteri-drag)
    ![Alt text](shot:kalenteri-drag#calendar-grid,calendar-tools)

After `#` comes an ordered list of testIDs. The page draws numbered markers 1, 2, … on those elements, using the bounds in the sidecar. The text refers to them as (1), (2).

## The stills

| name | screen and state | callouts (testIDs) |
|---|---|---|
| onboarding-tervetuloa | welcome | |
| onboarding-ehdot | terms acceptance | |
| onboarding-profiilin-luonti | profile creation | |
| onboarding-yhteystiedot | contact details | |
| onboarding-omat-tiedot | own details | |
| onboarding-profiilikuva | profile picture | |
| onboarding-persoonallisuus | personality | |
| onboarding-tarinatesti | story test, first question | |
| onboarding-kielet | languages | |
| onboarding-treffiaktiviteetit | date activities | |
| treffit | home screen with petals, a date and an invitation | `balance-counter`, `tip-bank`, `find-dates` |
| popover-petals | petals explainer open | |
| kalenteri | calendar week with free slots and density shading | `calendar-menu`, `calendar-explainer` |
| kalenteri-drag | mid-drag selecting a new slot | |
| kalenteri-toistuva | the repeat-week sheet open | `repeat-proposal`, `repeat-save`, `repeat-cancel` |
| popover-calendar | calendar explainer open | |
| date-wizard-kalenteri | date wizard, calendar step | `date-wizard-next` |
| date-wizard-petals | date wizard, petal balance step | `wizard-balance`, `date-wizard-send` |
| platter | a drawn set of candidates | `card-map-toggle`, `timeslot-chip-0`, `activity-chip-0`, `propose` |
| cooldown-blocked | what a blocked cooldown looks like | `cooldown-notice` |
| cooldown-hidden | hidden cooldown | `cooldown-notice` |
| cooldown-nodraw | no-draw cooldown | `cooldown-notice` |
| invitation | received invitation | `timeslot-0`, `venue-0`, `invitation-accept`, `invitation-decline` |
| sent | sent invitation, waiting for an answer | `waiting-explainer`, `withdraw-invitation-open` |
| date | the agreed date screen | `agreed-time`, `venue-map` |
| date-map | the date map | `meet-up-reveal` |
| date-location-consent | the location-sharing consent | |
| date-noshow-not-at-venue | no-show report refused: not at the venue | |
| feedback | post-date feedback | `feedback-when` |
| kysymykset | question sets tab | `retake-story-test`, `question-set-0` |
| kysymyssarja | a question set open | `question-0`, `save-survey` |
| popover-surveys | question sets explainer | |
| asetukset | settings | |
| asetukset-omat-tiedot | settings: own details open | `date-pace`, `save-own-info` |
| asetukset-turvallisuus | settings: safety open | `safety-contact-input`, `save-safety-contact` |
| asetukset-ilmoitukset | settings: notifications open | `save-notification-preferences` |
| asetukset-ehdot | settings: terms open | |
| asetukset-tili | settings: account open (sign out everywhere, delete) | `sign-out`, `sign-out-everywhere`, `delete-account` |

Four of the callouts above name a testID the app does not have yet, so the capture work adds them. What each one should sit on:

- `find-dates`: the `Löydä treffit!` / `Viimeistele kutsu` button in the Treffit tab's footer (`src/app/(tabs)/treffit.tsx`).
- `propose`: the `Ehdota!` button on the centred candidate card (`src/components/CandidateCard.tsx`).
- `invitation-accept`, `invitation-decline`: the `Sovittu!` and `Hylkää` buttons on a received invitation (`src/app/invitation/[matchId].tsx`).

Callouts are filled in by whoever writes the text. When the text needs a new callout, add the testID in the table above. The capture pipeline then records its bounds on the next run. If a testID does not exist in the app yet, the capture work adds it.
