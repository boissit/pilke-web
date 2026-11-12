---
title: Cancelling and time-outs
lead: You get a time-out if you cancel a date or withdraw an invite you sent. The same goes if you decline an invite, leave it unanswered or don't turn up to a date. Here's how time-outs work.
order: 60
draft: false
---

A date is a date, and time has been set aside for it. Cancelling is rude, and it gets you a time-out.

## Types of time-out

| Type of time-out | What it stops | The Dates page says |
|---|---|---|
| No looking, no invites | You aren't shown in other people's matches, and you can't look for new matches. | *Until then, you can't look for new matches and won't be shown to anyone else.* |
| No looking | You can't look for new matches, but you're still shown in other people's matches. | *Until then, you can't look for new matches.* |

While you're on a time-out, you can answer invites you receive and go on your upcoming dates. Your open invites and upcoming dates stay as they are.

![A notice on the Dates page: you won't be shown to anyone else and can't look for new matches](shot:cooldown-blocked#cooldown-notice)

The notice at the top of the Dates page (1) tells you what your time-out stops, until when and why.

## What gets you a time-out

| What you did | Type of time-out | How long |
|---|---|---|
| Withdrew an invite you sent before it was answered | No looking | {{cooldown.withdrawal_hours}} hours |
| Declined an invite you received | No looking | {{cooldown.decline_hours}} hours |
| Left an invite you received unanswered | No looking | {{cooldown.no_answer_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_long_notice_days}} days ahead | No looking, no invites | {{cooldown.cancel_long_notice_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_short_notice_hours}} hours ahead | No looking, no invites | {{cooldown.cancel_short_notice_days}} days |
| Cancelled a date any later | No looking, no invites | {{cooldown.cancel_late_days}} days |
| Your date reported from the venue that you didn't turn up | No looking, no invites | {{cooldown.noshow_days}} days |

If you cancel often, your time-outs get longer. Each date you've cancelled in the last {{cooldown.repeat_window_days}} days multiplies the length of the time-out for your next cancellation by {{cooldown.repeat_multiplier}}. The longest time-out is {{cooldown.ceiling_days}} days.

![A notice on the Dates page: you can't look for new matches because you declined an invite](shot:cooldown-decline#cooldown-notice)

You can always decline an invite without giving a reason, and it's better to decline than to leave it hanging. But the app doesn't work if everyone declines invites, so declining gets you a short time-out (1). During this time-out, you're still shown to other people and can answer the invites you receive.

## What your date sees when you cancel

Your date is told straight away when you cancel. The time of the date is freed for both of you. If you invited them, you don't get your sparks back. If they invited you, they get their sparks back.

To cancel a date, press **Cancel date** on its screen.

Cancel as soon as you know you can't make the date. The earlier you cancel, the shorter the time-out.
