---
title: Sparks
lead: Every date needs a spark. You earn sparks by keeping your calendar up to date and going on dates, and {{petals.set_cost}} sparks send an invite.
order: 30
draft: true
---

Your sparks are at the top of the Dates page. This page explains where they come from, where they go and when you get them back.

## Where sparks come from and where they go

| What happens | Sparks |
|---|---|
| You confirm your phone number when you sign up | +{{petals.signup_bonus}}, once |
| You keep {{calendar.petal_week_hours}} hours of free time marked for a week | +1 |
| You go on a date and say how it went | +{{sparks.per_date}}, when you send your feedback |
| You send an invite | −{{petals.set_cost}}, when you press **Find a date** |
| Your invite is declined | +{{petals.refund}} back |
| Your invite expires because nobody answered within {{invitation.answer_hours}} hours | +{{petals.refund}} back |
| The person you invited cancels your date | +{{petals.refund}} back |
| Pilke can't find enough matches | Your sparks stay put |
| You withdraw your invite before it's answered | No refund |
| You invite none of the matches you found | No refund |
| You cancel a date | No refund |

A refund gives you back the {{petals.refund}} sparks the invite cost.

The sparks for a date come with your feedback. You each get yours once you've answered.

## Sparks from your calendar

Your calendar earns sparks for how long your free time stays marked. {{calendar.petal_week_hours}} hours for a week earns one spark, and so does {{calendar.counted_hours_cap}} hours for a little under two days. Sparks arrive one at a time as they add up.

- Only future times count, and only the part of them within the next {{calendar.earning_horizon_days}} days. An hour stops earning when it starts.
- At most {{calendar.counted_hours_cap}} hours count at once, so your calendar earns at most {{calendar.max_petals_per_week}} sparks a week.
- A time you mark and then remove straight away earns nothing.

### Examples

| In your calendar | Sparks |
| --- | --- |
| Saturday 18:00–22:00 (4 hours), marked a week ahead | about 0.4 |
| The same Saturday, marked 20 days ahead: it starts earning once Saturday is {{calendar.earning_horizon_days}} days away | about 0.8 |
| About 10 hours a week, always marked two weeks ahead | about 2 a week |
| At least {{calendar.counted_hours_cap}} hours within the next {{calendar.earning_horizon_days}} days, all the time | {{calendar.max_petals_per_week}} a week |

## The limit

You can hold up to {{petals.cap}} sparks at a time, enough for {{petals.cap_roses}} invites. Once you have {{petals.cap}}, any new sparks wait. They arrive as soon as you send an invite and make room, so a full count is worth using.

For example: you have {{petals.cap}} sparks, and your calendar earns 2 more in a week. Those 2 wait. When you send an invite, {{petals.set_cost}} sparks go and the 2 that were waiting arrive. The sparks for feedback only arrive when they all fit at once.

Refunds arrive whatever your count, so you can sometimes have more than {{petals.cap}}.

## When sparks are spent

![The last step before your matches: your sparks and the Find a date button](shot:date-wizard-petals#wizard-balance,date-wizard-send)

You see your sparks (1) before you send an invite. {{petals.set_cost}} of them go as soon as you press **Find a date** (2). Then you see {{candidates.per_set}} matches and choose who gets the invite.

If Pilke can't find {{candidates.per_set}} matches, your sparks stay put. If you see your matches and invite none of them, you don't get the sparks back. Your matches wait for you for {{candidates.set_hours}} hours: see [Who you're shown](/en/guide/ehdokkaat).
