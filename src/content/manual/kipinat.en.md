---
title: Sparks
lead: Every date needs a spark. You earn sparks by keeping your calendar up to date and going on dates, and {{petals.set_cost}} sparks send an invite.
order: 30
draft: true
---

Your sparks are at the top of the Dates page. This page covers how you earn them and what they're spent on.

## How you earn sparks and what they're spent on

| What happens | Sparks |
|---|---|
| You confirm your phone number when you sign up | +{{petals.signup_bonus}}, once |
| You keep {{calendar.petal_week_hours}} hours of free time marked for a week | +1 |
| You go on a date and say how it went | +{{sparks.per_date}}, when you send your feedback |
| You send an invite | −{{petals.set_cost}}, when you press **Find a date** |
| Your invite is declined | +{{petals.refund}} back |
| Nobody answers your invite within {{invitation.answer_hours}} hours, and it expires | +{{petals.refund}} back |
| The person you invited cancels your date | +{{petals.refund}} back |
| There aren't enough matches for you | Your sparks stay put |
| You withdraw your invite before it's answered | No refund |
| You invite none of the matches you found | No refund |
| You cancel a date | No refund |

A refund gives you back the {{petals.refund}} sparks the invite cost.

You get the sparks for a date once you've filled in your date feedback.

## Sparks from your calendar

The longer a free time stays marked, the more sparks it earns. {{calendar.petal_week_hours}} hours marked for a week earns one spark. So does {{calendar.counted_hours_cap}} hours for a little under two days. Your sparks arrive one at a time as they add up.

- A future time counts for the part of it within the next {{calendar.earning_horizon_days}} days.
- At most {{calendar.counted_hours_cap}} hours count at once, so your calendar earns up to {{calendar.max_petals_per_week}} sparks a week.
- A time you mark and then remove straight away earns nothing.

### Examples

| In your calendar | Sparks |
| --- | --- |
| Saturday 18:00–22:00 (4 hours), marked a week ahead | about 0.4 |
| The same Saturday, marked 20 days ahead. Sparks start adding up once Saturday is {{calendar.earning_horizon_days}} days away | about 0.8 |
| About 10 hours a week, always marked two weeks ahead | about 2 a week |
| Always at least {{calendar.counted_hours_cap}} hours within the next {{calendar.earning_horizon_days}} days | {{calendar.max_petals_per_week}} a week |

## The limit

You can hold up to {{petals.cap}} sparks at a time, enough for {{petals.cap_roses}} invites. Once you reach the limit, new sparks wait. You can get more once you send an invite and make room. When you're at the limit, send an invite!

Say you have {{petals.cap}} sparks, and your calendar earns 2 more in a week. You get them once you send an invite and make room.

Refunds arrive whatever your count, so you can sometimes have more than {{petals.cap}}.

## When sparks are spent

![The last step before your matches: your sparks and the Find a date button](shot:date-wizard-petals#wizard-balance,date-wizard-send)

Before you send an invite, you see your sparks (1). When you press **Find a date** (2), {{petals.set_cost}} sparks are spent straight away. Then you see {{candidates.per_set}} matches and choose who to invite.

If there are fewer than {{candidates.per_set}} matches for you, your sparks stay put. If you invite none of the matches you found, you don't get the sparks back. Your matches wait for you for {{candidates.set_hours}} hours. See [Who you're shown](/en/guide/ehdokkaat).
