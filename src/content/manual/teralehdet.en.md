---
title: Petals
lead: Petals open a set of candidates. You earn them by using the app, and they cannot be bought.
kind: explainer
order: 10
draft: true
---

Petals are Pilke's only currency. {{petals.per_rose}} petals make a rose, and a rose opens a set. There is no other price.

## What petals are spent on

Opening a set costs {{petals.set_cost}} petals. They go the moment you press **Send an invitation!** and the candidates are found. Sending the invitation itself costs nothing.

Answering an invitation costs nothing either, whether you accept it or decline it.

## Where petals come from

| From | How many |
|---|---|
| Finishing registration, once your code is confirmed | {{petals.signup_bonus}}, once |
| A date you went on, once you give feedback about it | {{petals.per_date}} |
| The other person calling off an agreed date | {{petals.consolation}} |
| Times marked in your calendar | about one a week for every {{calendar.petal_week_hours}} hours |

For a date, you each get your own once you have each given feedback. No feedback, no petals.

## Petals from your calendar

Your calendar earns for as long as the times in it stand. {{calendar.petal_week_hours}} hours of free time, left marked for a week, earns one petal.

- Only times that have not started yet count, and only the part of them within the next {{calendar.earning_horizon_days}} days.
- Each time has to be at least {{calendar.min_slot_hours}} h long.
- At most {{calendar.counted_hours_cap}} hours count at once, so your calendar earns at most {{calendar.max_petals_per_week}} petals a week.

Marking a time and deleting it straight away earns nothing. What earns is how long a time stays marked.

## The limit

You can earn up to {{petals.cap}} petals, which is {{petals.cap_roses}} roses. Once you reach it, whatever you earn waits, and arrives when you spend some and there is room under the limit again. Nothing is lost.

Refunds are not earnings, so they arrive whatever your balance, and a balance can sometimes sit above the limit. Compensation for a date the other person called off is an earning, and waits for room like the rest.

## When petals come back

| What happened | What you get |
|---|---|
| Your invitation was declined | {{petals.refund}} back |
| Nobody answered your invitation within {{invitation.answer_hours}} hours | {{petals.refund}} back |
| The other person called off an agreed date you invited them to | {{petals.refund}} back, and {{petals.consolation}} on top as compensation |
| Pilke could not find enough candidates | Nothing was charged |

Petals do not come back if you withdraw your own invitation before it is answered, or if a set you opened closes unused. Both of those were your call.

## What petals cannot do

Petals are not sold. There is no visibility, highlighting or better place in the suggestions to buy.
