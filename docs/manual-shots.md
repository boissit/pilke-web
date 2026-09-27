# Manual screenshots — the contract

This file is shared by three pieces of work: the capture pipeline in `pilke-app`, the page layout in this repo, and the manual text. Each still is named here once. Every piece refers to it by that name.

## Where a still lives

    src/assets/manual/fi/<name>.png
    src/assets/manual/fi/<name>.json
    src/assets/manual/en/<name>.png
    src/assets/manual/en/<name>.json

The sidecar `<name>.json`:

    {
      "name": "kalenteri",
      "language": "fi",
      "commit": "<pilke-app HEAD sha, with -dirty if the tree was dirty>",
      "takenAt": "2026-09-24T12:00:00Z",
      "screen": { "width": 1080, "height": 2280 },
      "elements": { "<testID>": { "x": 0, "y": 0, "width": 0, "height": 0 } }
    }

Element bounds are in the PNG's own pixels. Only the testIDs listed under **Callouts** are required. Others may be present.

## How the text points at a still

A paragraph that contains only an image:

    ![Alt text in the page's language](shot:kalenteri)
    ![Alt text](shot:kalenteri-toistuva#repeat-proposal,repeat-save)

After `#` comes an ordered list of testIDs. The page draws numbered markers 1, 2, … on those elements, using the bounds in the sidecar. The text refers to them as (1), (2).

## The stills

Only the stills the manual draws are listed. Each one is there because it shows a state people misread, so the state column says which state that is: a capture of the same screen in another state is a different picture.

| name | screen and state | callouts (testIDs) |
|---|---|---|
| treffit | home screen with petals, a received invitation and an agreed date | `balance-counter`, `find-dates` |
| kalenteri | calendar week with own free slots and the yellow density shading visible on several hours | `calendar-density` |
| kalenteri-valikko | the calendar's quick-actions menu open over the calendar, the ⋮ button still in view behind it | `calendar-menu`, `repeat-week` |
| kalenteri-toistuva | the repeat-week proposal, drawn dashed, with its summary bar | `repeat-proposal`, `repeat-save` |
| date-wizard-petals | date wizard, petal balance step, before the set is drawn | `wizard-balance`, `date-wizard-send` |
| platter | a drawn set of candidates, centred card | `timeslot-chip-0`, `activity-chip-0` |
| cooldown-blocked | Treffit tab with the blocked (hidden and no-draw) cooldown notice | `cooldown-notice` |
| cooldown-nodraw | Treffit tab with the no-draw cooldown notice | `cooldown-notice` |
| cooldown-hidden | Treffit tab with the hidden cooldown notice | `cooldown-notice` |
| invitation | received invitation, several times and venues | `timeslot-0`, `venue-0` |
| sent | sent invitation, waiting for an answer, several venues | `waiting-explainer`, `withdraw-invitation-open` |
| date | the agreed date screen once it has started, the live map under Löydättekö toisenne? | `agreed-time`, `live-map` |
| date-map | the date map inside the sharing window, not yet sharing | `meet-up-reveal` |
| date-location-consent | the location-sharing consent | |
| date-noshow-not-at-venue | no-show report refused: not at the venue | `no-show-report` |
| feedback | post-date feedback, first question | `feedback-when` |
| asetukset-ilmoitukset | settings: notifications open, the three always-on rows in view | `notification-reveal_prompt-push`, `notification-party_arrived-push`, `notification-date_cancelled-push` |
| asetukset-tili | settings: account open (sign out everywhere, delete) | `sign-out-everywhere`, `delete-account` |

Two callouts need a word on where their bounds come from:

- `calendar-density`: the first shaded hour on screen, one cell of the yellow density shading drawn by `src/components/calendar/density.tsx`. The shading is one view per hour and day, with no wrapper around a band, so each hour row marks its first shaded cell and the sidecar keeps the first one on screen. The capture needs at least five people free at the same hours, which `make seed-density` in the backend provides.
- `calendar-menu` on `kalenteri-valikko`: the menu is a modal, its own window, and the menu's view hierarchy has nothing behind the scrim in it. The flow photographs the calendar just before opening the menu, and the capture lays that hierarchy under the menu's.

In `asetukset-ilmoitukset` the "Aina päällä" heading is scrolled off the top of the current capture. The next capture should scroll so the heading and its three rows are both in view.

Callouts are filled in by whoever writes the text. When the text needs a new callout, add the testID in the table above. The capture pipeline then records its bounds on the next run. If a testID does not exist in the app yet, the capture work adds it.
