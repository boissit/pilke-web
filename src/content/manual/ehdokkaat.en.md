---
title: Candidates
lead: How to open a set of candidates and choose who your invitation goes to.
kind: guide
order: 40
draft: true
---

A set holds {{candidates.per_set}} candidates. You pick one of them and offer them times and places. Opening a set costs {{petals.set_cost}} petals.

## Opening a set

On the Dates page, press **Find a date!**.

![The first step: your calendar and the Next button](shot:date-wizard-kalenteri#date-wizard-next)

First you see your calendar. Candidates are found from it, so check that it is up to date, then press **Next** (1).

![The second step: your petals and the Send an invitation! button](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Next you see your petals (1). Press **Send an invitation!** (2) and Pilke looks for candidates for you.

This is the moment the petals are spent. Sending the invitation itself costs nothing more. Without enough petals you see *You need more petals* and a **Back** button instead.

## Looking through the candidates

![Candidates: a candidate's photo, the times you both have and something to do together](shot:platter#card-map-toggle,timeslot-chip-0,activity-chip-0,propose)

The candidates are cards side by side. Swipe sideways for the next one. The middle card is the one Pilke thinks suits you best.

Each card has the candidate's photo, name and age. **Map** (1) swaps the photo for a map of the places you could meet, and **Photo** swaps it back.

To put an invitation together:

1. Under **Times you both have** (2), choose the times that would suit you. The card shows at most the {{candidates.times_per_card}} soonest times you are both free.
2. Under **Something to do together** (3), choose the places you would like to go. The card shows at most {{candidates.venues_per_card}}.
3. Press **Propose!** (4).

Choose at least {{invitation.min_times_offered}} time and {{invitation.min_venues_offered}} place, and give the other person a choice: either {{invitation.choice_threshold}} times or {{invitation.choice_threshold}} places. Until you have, the card says what is missing and **Propose!** does nothing.

The invitation goes straight away. The other candidates in the set go, and you are back on the Dates page. The other person picks one of your times and one of your places. See [The invitation](/en/guide/kutsu).

## If you do not send it straight away

A set stays open for {{candidates.set_hours}} hours. Meanwhile the Dates page button reads **Finish your invitation** and takes you back to the same set.

A set closes sooner if its times go by. Petals spent on a set that closes unused do not come back.

## If no candidates are found

If Pilke cannot find {{candidates.per_set}} candidates who suit you, no petals are spent, and you are told why, for example:

- *Nobody suitable shares a single time with you.* Mark more times in your calendar.
- *What you are looking for does not match anybody right now.* Widen what you are looking for under Settings, Your details.
- *There is nobody suitable in your date area.* Choose more date areas.
- *There are too few suitable people right now.* Try again later.

If you cannot look for candidates right now, you are told why and until when. See [Cooldowns](/en/guide/jaahdytys). How the candidates are chosen is on [How candidates are chosen](/en/guide/ehdokkaiden-valinta).
