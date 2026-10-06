# Manual screenshots — the contract

This file is shared by three pieces of work: the capture pipeline in `pilke-app`, the page layout in this repo, and the manual text. Each still is named here once. Every piece refers to it by that name.

## Where a still lives

Written by pilke-app's `scripts/capture-site-pictures.sh`, whose `manual` step runs
`capture-screens.sh --manual`, and never by hand: "When the app changes" in
`docs/pictures.md` is the runbook.

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

## How a still is drawn

Whole, in the device frame `ManualStep.astro` asks `Phone.astro` for: a thin bezel in the app's ink, the colour of every border its buttons and cards have, with the still cut to the bezel's rounded opening and a punch-hole camera in the middle of the status bar. Nothing is cropped, for three reasons:

- The status bar and the navigation bar are what the reader sees on their own phone.
- The rounded corners fall on the bars, where the app draws nothing, so a map, a photo or a dimmed modal reaching the edge of the screen is never cut, and no margin of a single colour shows a square picture corner inside a round frame.
- The markers are drawn from the bounds below as they stand, in percentages of the whole still. Every badge is placed inside the picture and clear of its rounded corners.

The camera is drawn over the middle of the status bar, which is empty on the capture's Pixel 4 profile. A still with a notification icon or a clock there would have it covered.

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
| cooldown-decline | Treffit tab with the no-draw cooldown notice for a declined invitation | `cooldown-notice` |
| invitation | received invitation, several times and venues | `timeslot-0`, `venue-0` |
| sent | sent invitation, waiting for an answer, several venues | `withdraw-invitation-open` |
| date | the agreed date screen inside the sharing window, the live map under Löydättekö toisenne? | `agreed-time`, `live-map` |
| date-map | the date map inside the sharing window, not yet sharing | `meet-up-reveal` |
| date-map-sharing | the date map while you and your date are both sharing your locations | `meet-up-stop` |
| date-location-consent | the location-sharing consent | |
| date-noshow-not-at-venue | no-show report refused: not at the venue | `no-show-report` |
| feedback | post-date feedback, first question | `feedback-when` |
| date-history-open | the foot of the Treffit tab, with the Treffihistoria button | `open-date-history` |
| date-history | Treffihistoria: past dates, the newest with a swapped number in its row | `date-history-row-number` |
| asetukset-ilmoitukset | settings: notifications open, the three always-on rows in view | `notification-new_date-push`, `notification-new_date-email` |
| asetukset-tili | settings: account open (sign out everywhere, delete) | `sign-out-everywhere`, `delete-account` |

Four callouts need a word on where their bounds come from:

- `calendar-density`: the first shaded hour on screen, one cell of the yellow density shading drawn by `src/components/calendar/density.tsx`. The shading is one view per hour and day, with no wrapper around a band, so each hour row marks its first shaded cell and the sidecar keeps the first one on screen. The capture needs at least five people free at the same hours; it seeds them (`make seed-density`'s command) before the walk that takes this still, since every fixture reset clears them.
- `date-history-row-number` on `date-history`: the app's testID is `date-history-row-<match id>-number`, and the fixture makes new matches every run. `manual-shots.py` records the first such row on screen under this stable name as well (`ALIASES`), and the capture seeds the swapped number on the newest date so that row is the first.
- `meet-up-stop` on `date-map-sharing`, and no marker on the sentence about the other person's pin above it: the emulator's location provider sometimes answers with its own default place between two fixes, and the `too_far` line that brings is drawn between the sentence and the button. It came and went between the still and its hierarchy, which moved the sentence's bounds off the sentence in the picture. The button is anchored to the foot of the panel and stays put.
- `calendar-menu` on `kalenteri-valikko`: the menu is a modal, its own window, and the menu's view hierarchy has nothing behind the scrim in it. The flow photographs the calendar just before opening the menu, and the capture lays that hierarchy under the menu's.

In `asetukset-ilmoitukset` the "Aina päällä" heading is scrolled off the top of the current capture. The next capture should scroll so the heading and its three rows are both in view.

Callouts are filled in by whoever writes the text. When the text needs a new callout, add the testID in the table above. The capture pipeline then records its bounds on the next run. If a testID does not exist in the app yet, the capture work adds it.
