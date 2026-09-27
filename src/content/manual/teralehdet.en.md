---
title: Petals
lead: "Petals are Pilke's currency: you earn them by going on dates and spend them by sending date invitations."
order: 30
draft: true
---

{{petals.per_rose}} petals make a rose, and a rose is the price of one date invitation. This page covers everything that earns them, spends them and gives them back.

## Earning and spending petals

| What happens | Petals |
|---|---|
| You keep {{calendar.petal_week_hours}} hours of free time marked for a week | +1 |
| You go on a date and give feedback on it | +{{petals.per_date}}, when you send the feedback |
| You send a date invitation | −{{petals.set_cost}}, when you press **Send an invitation!** |
| Your invitation is declined | +{{petals.refund}} back |
| Your invitation lapses because nobody answered within {{invitation.answer_hours}} hours | +{{petals.refund}} back |
| The person you invited calls off your agreed date | +{{petals.refund}} back |
| No suitable candidates can be found | Nothing is charged |
| You withdraw your invitation before it is answered | No refund |
| You invite none of the candidates you found | No refund |
| You call off an agreed date | No refund |

A refund gives you back the {{petals.refund}} petals the invitation cost.

The only petals a date brings are the ones for feedback. No feedback, no petals. Each of you gets your own once you have answered.

## Petals from the calendar

The calendar pays for how long free time stays marked. {{calendar.petal_week_hours}} hours for a week is one petal, and so is {{calendar.counted_hours_cap}} hours for a little under two days. Petals arrive one at a time as they build up.

- Only times that have not started yet count, and only the part of them within the next {{calendar.earning_horizon_days}} days. An hour stops earning when it begins.
- At most {{calendar.counted_hours_cap}} hours count at once, so the calendar earns at most {{calendar.max_petals_per_week}} petals a week.
- Marking a time and removing it straight away earns nothing.

### Examples

| In your calendar | Petals |
| --- | --- |
| Saturday 18–22 (4 hours), marked a week before | about 0.4 |
| The same Saturday, marked 20 days before: it starts earning once Saturday is {{calendar.earning_horizon_days}} days away | about 0.8 |
| About 10 hours a week, always marked two weeks ahead | about 2 a week |
| At least {{calendar.counted_hours_cap}} hours within the next {{calendar.earning_horizon_days}} days, all the time | {{calendar.max_petals_per_week}} a week |

## The cap

You can earn up to {{petals.cap}} petals, which is {{petals.cap_roses}} roses. Anything earned beyond that waits, and arrives once you spend petals and there is room under the cap. The {{petals.per_date}} petals for feedback only arrive when they all fit at once.

Refunds arrive whatever your balance, so it can sometimes be above {{petals.cap}}.

## When petals are spent

![The last step before your candidates: your petal balance and the Send an invitation! button](shot:date-wizard-petals#wizard-balance,date-wizard-send)

You see your petals (1) before you send an invitation. They are spent as soon as you press **Send an invitation!** (2). Then you find {{candidates.per_set}} candidates and choose who the invitation goes to.

If {{candidates.per_set}} suitable candidates cannot be found, nothing is charged. If you find candidates and invite none of them, the petals do not come back. Your candidates wait for you for {{candidates.set_hours}} hours: see [Who you are shown](/en/guide/ehdokkaat).
