---
title: Cancelling and time-outs
lead: You get a time-out if you cancel a date or withdraw an invite you sent. The same goes if you decline an invite, leave it unanswered or don't turn up to a date. Here's how long a time-out lasts and what you can do during it.
order: 60
draft: true
---

A date is something the two of you decided on together. Your date has set time aside for you, and there are no messages in the app, so they can't ask you anything. That makes cancelling rude, and it gets you a time-out. A time-out ends on its own, and your sparks stay as they are.

## Two kinds of time-out

| Time-out | What it stops | The notice says |
|---|---|---|
| Both | You aren't shown in other people's matches, and you can't look for new matches. | *Until then, you can't look for new matches and won't be shown to anyone else.* |
| No looking | You can't look for new matches, but you're still shown in other people's matches. | *Until then, you can't look for new matches.* |

While you're on a time-out, you can answer invites you receive and go on your upcoming dates. Your open invites and upcoming dates stay as they are. If you'd already found your matches, you can still invite one of them.

![A notice on the Dates page: you won't be shown to anyone else and can't look for new matches](shot:cooldown-blocked#cooldown-notice)

The notice at the top of the Dates page (1) tells you what your time-out stops, until when and why. You see the same text if you try to look for matches. If you have more than one time-out, the notice gives the reason and end time of the one that ends last.

## What gets you a time-out

| What you did | Time-out | How long |
|---|---|---|
| Withdrew an invite you sent before it was answered | No looking | {{cooldown.withdrawal_hours}} hours |
| Declined an invite you received | No looking | {{cooldown.decline_hours}} hours |
| Left an invite you received unanswered | No looking | {{cooldown.no_answer_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_long_notice_days}} days ahead | Both | {{cooldown.cancel_long_notice_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_short_notice_hours}} hours ahead | Both | {{cooldown.cancel_short_notice_days}} days |
| Cancelled a date any later | Both | {{cooldown.cancel_late_days}} days |
| Your date reported from the venue that you didn't turn up | Both | {{cooldown.noshow_days}} days |

If you cancel often, your time-outs get longer. Each date you've cancelled in the last {{cooldown.repeat_window_days}} days multiplies the time-out for your next cancellation by {{cooldown.repeat_multiplier}}. The longest time-out is {{cooldown.ceiling_days}} days. Only cancelled dates count towards this, not time-outs from invites or from not turning up.

![A notice on the Dates page: you can't look for new matches because you declined an invite](shot:cooldown-decline#cooldown-notice)

You can decline without giving a reason, and for the person who invited you, a no is a better answer than silence. Declining or leaving an invite unanswered gets you a short time-out (1), because they spent sparks on the invite and waited for your answer. During it, you're still shown to other people and can answer the invites you receive.

## What cancelling means for your date

Your date is told straight away when you cancel. That notification can't be switched off, because otherwise they'd go and wait for someone who isn't coming. The time of the date is freed for both of you. If you invited them, your sparks stay spent. If they invited you, they get {{petals.refund}} sparks back.

To cancel a date, press **Cancel date** on its screen. Before you confirm, you see when your time-out would end. Once the date's start time has passed, the button's gone.

Cancel as soon as you know you can't make it. The earlier you cancel, the shorter the time-out.
