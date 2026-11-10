---
title: Cancelling and pauses
lead: If you cancel a date, withdraw your invite, decline an invite or leave it unanswered, or don't turn up, you're paused for a while. This page shows how long a pause lasts and what you can still do during it.
order: 60
draft: true
---

An upcoming date is something two people agreed on together. Your date has set time aside for you, and there's no messaging in the app, so they can't ask you anything. Cancelling decides for both of you, which is rude to them, and it gets you paused. A pause ends on its own, and your sparks stay as they are.

## Two kinds of pause

| Pause | What you can't do | The notice says |
|---|---|---|
| Both | Be shown to other people, or look for new matches. | *Until then, you can't look for new matches and won't be shown to anyone else.* |
| No looking | Look for new matches. You're still shown to others. | *Until then, you can't look for new matches.* |

While you're paused, you can still answer invites you receive and go on your upcoming dates. Your open invites and upcoming dates stay as they are. If you'd already found your matches, you can still send one of them an invite.

![A notice on the Dates page: you won't be shown to anyone else and can't look for new matches](shot:cooldown-blocked#cooldown-notice)

While you're paused, the top of the Dates page shows a notice (1): what it stops, until when, and why. You see the same text if you try to look for matches. If you're paused for more than one reason, the notice shows the reason and end time of the one that ends last.

## What starts one

| What you did | Pause | How long |
|---|---|---|
| Withdrew an invite you sent before it was answered | No looking | {{cooldown.withdrawal_hours}} hours |
| Declined an invite you received | No looking | {{cooldown.decline_hours}} hours |
| Left an invite you received unanswered | No looking | {{cooldown.no_answer_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_long_notice_days}} days ahead | Both | {{cooldown.cancel_long_notice_hours}} hours |
| Cancelled a date at least {{cooldown.cancel_short_notice_hours}} hours ahead | Both | {{cooldown.cancel_short_notice_days}} days |
| Cancelled a date any later | Both | {{cooldown.cancel_late_days}} days |
| Your date reported from the venue that you didn't turn up | Both | {{cooldown.noshow_days}} days |

Cancelling again and again makes the pause longer. Each date you've cancelled in the last {{cooldown.repeat_window_days}} days multiplies the next pause by {{cooldown.repeat_multiplier}}, up to {{cooldown.ceiling_days}} days at most. Withdrawn, declined and unanswered invites and no-shows don't count towards this.

![A notice on the Dates page: you can't look for new matches because you declined an invite](shot:cooldown-decline#cooldown-notice)

You can decline without giving a reason, and a no is a better answer for the person who invited you than silence. Declining or leaving an invite unanswered gets you a short pause (1): they spent sparks on the invite and waited for your answer. During it, you're still shown to other people and can answer the invites you receive.

## What cancelling means for your date

When you cancel a date, your date is told straight away. That notification can't be switched off, because without it they'd go and wait for someone who isn't coming. The agreed time is freed for both of you. If you sent the invite, the sparks you spent stay spent. If they invited you, they get {{petals.refund}} sparks back.

You cancel a date with **Cancel date** on its screen. Before you confirm, you see when your pause would end. Once the start time has passed, the button's gone.

So cancel as soon as you know you can't make it: the earlier you do, the shorter the pause.
