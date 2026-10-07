---
title: Sparks
lead: Pilke runs on sparks. They build up from a calendar kept up to date and from the dates you go on, and {{petals.set_cost}} sparks send a date invitation.
order: 30
draft: true
---

Your sparks are at the top of the Dates page. This page covers where they come from, where they go and when they come back to you.

## Where sparks come from and where they go

| What happens | Sparks |
|---|---|
| You confirm your phone number when you sign up | +{{petals.signup_bonus}}, once |
| You keep {{calendar.petal_week_hours}} hours of free time marked for a week | +1 |
| You go on a date and say how it went | +{{petals.per_date}}, when you send the feedback |
| You send a date invitation | −{{petals.set_cost}}, when you press **Send an invitation!** |
| Your invitation is declined | +{{petals.refund}} back |
| Your invitation lapses because nobody answered within {{invitation.answer_hours}} hours | +{{petals.refund}} back |
| The person you invited calls off your agreed date | +{{petals.refund}} back |
| No suitable candidates can be found | Your sparks stay put |
| You withdraw your invitation before it is answered | No refund |
| You invite none of the candidates you found | No refund |
| You call off an agreed date | No refund |

A refund gives you back the {{petals.refund}} sparks the invitation took.

The sparks for a date come with your feedback. Each of you gets your own once you have answered.

## Sparks from your calendar

Your calendar earns sparks for how long free time stays marked. {{calendar.petal_week_hours}} hours for a week bring one spark, and so do {{calendar.counted_hours_cap}} hours for a little under two days. Sparks arrive one at a time as they build up.

- Times still to come count, and only the part of them within the next {{calendar.earning_horizon_days}} days. An hour stops earning when it begins.
- At most {{calendar.counted_hours_cap}} hours count at once, so your calendar earns at most {{calendar.max_petals_per_week}} sparks a week.
- A time you mark and remove straight away earns nothing.

### Examples

| In your calendar | Sparks |
| --- | --- |
| Saturday 18–22 (4 hours), marked a week before | about 0.4 |
| The same Saturday, marked 20 days before: it starts earning once Saturday is {{calendar.earning_horizon_days}} days away | about 0.8 |
| About 10 hours a week, always marked two weeks ahead | about 2 a week |
| At least {{calendar.counted_hours_cap}} hours within the next {{calendar.earning_horizon_days}} days, all the time | {{calendar.max_petals_per_week}} a week |

## The cap

You can hold up to {{petals.cap}} sparks at a time, enough for {{petals.cap_roses}} invitations. Once you have {{petals.cap}}, new sparks wait. They arrive as soon as you send an invitation and make room, so a full count is worth sending on its way.

For example: you have {{petals.cap}} sparks, and your calendar earns 2 more in a week. Those 2 wait. When you send an invitation, {{petals.set_cost}} sparks go and the 2 that were waiting arrive. The sparks for feedback arrive only when they all fit at once.

Refunds arrive whatever your count, so you can sometimes have more than {{petals.cap}}.

## When sparks are spent

![The last step before your candidates: your sparks and the Send an invitation! button](shot:date-wizard-petals#wizard-balance,date-wizard-send)

You see your sparks (1) before you send an invitation. {{petals.set_cost}} of them go as soon as you press **Send an invitation!** (2). Then you find {{candidates.per_set}} candidates and choose who the invitation goes to.

If {{candidates.per_set}} suitable candidates cannot be found, your sparks stay put. If you find candidates and invite none of them, the sparks do not come back. Your candidates wait for you for {{candidates.set_hours}} hours: see [Who you are shown](/en/guide/ehdokkaat).
