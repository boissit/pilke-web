---
title: Cancelling and cooldowns
lead: If you call off an agreed date, withdraw an invitation you sent, decline or leave unanswered an invitation you received, or don’t turn up to a date, you get a cooldown. This page shows what causes one, how long it lasts and what you can’t do during it.
order: 60
draft: true
---

An agreed date is something two people decided together. The other person has set time aside for you, and there is no messaging in the app, so they cannot ask you anything. Calling it off decides for both of you, which is rude to them, and it earns you a cooldown. A cooldown takes no petals and ends on its own.

## Two kinds of cooldown

| Cooldown | What you cannot do | The notice begins |
|---|---|---|
| Both | Show up in other people's candidates, or look for new candidates. | *You are not showing up in other people's candidates right now, and you cannot look for new candidates until …* |
| No looking | Look for new candidates. You still show up for others. | *You cannot look for new candidates until …* |

During a cooldown you can still answer invitations you receive and go on your agreed dates. Your open invitations and agreed dates stay as they are. If you had already found your candidates, you can still send one of them an invitation.

![A notice on the Dates page: you are not showing up in other people's candidates and cannot look for new ones](shot:cooldown-blocked#cooldown-notice)

During a cooldown the top of the Dates page carries a notice (1): what it stops, until when, and why. The same text appears if you try to look for candidates. With more than one cooldown running, the notice gives the reason and end time of the one that ends last.

## What starts one

| What you did | Cooldown | How long |
|---|---|---|
| Withdrew an invitation you sent before it was answered | No looking | {{cooldown.withdrawal_hours}} hours |
| Declined an invitation you received | No looking | {{cooldown.decline_hours}} hours |
| Left an invitation you received unanswered | No looking | {{cooldown.no_answer_hours}} hours |
| Called off an agreed date at least {{cooldown.cancel_long_notice_days}} days ahead | Both | {{cooldown.cancel_long_notice_hours}} hours |
| Called off an agreed date at least {{cooldown.cancel_short_notice_hours}} hours ahead | Both | {{cooldown.cancel_short_notice_days}} days |
| Called off an agreed date any later | Both | {{cooldown.cancel_late_days}} days |
| The other person told us you did not turn up | Both | {{cooldown.noshow_days}} days |

Calling off dates again and again makes the cooldown longer. Each date you called off in the last {{cooldown.repeat_window_days}} days multiplies the next one's length by {{cooldown.repeat_multiplier}}, up to a ceiling of {{cooldown.ceiling_days}} days. Withdrawn, declined and unanswered invitations and no-shows do not add to the multiplier.

![A notice on the Dates page: you cannot look for new candidates because you declined a date invitation you received](shot:cooldown-decline#cooldown-notice)

You can decline without giving a reason, and a no is a better answer for the one who invited than silence. Declining or leaving an invitation unanswered gives you a short cooldown (1): they spent petals on the invitation and waited for your answer. During it you still show up in other people's candidates and can answer the invitations you receive.

## What calling off means for the other person

When you call off an agreed date, the other person is told straight away. That notification cannot be switched off, because without it they would go and wait for someone who is not coming. The agreed time is freed for both of you. If you were the one who invited, the petals you spent do not come back. If they invited you, they get back the {{petals.refund}} petals they spent on the invitation.

You call off an agreed date with **Cancel the date** on its screen. Once the start time has passed, the button is gone.

So call off as soon as you know you cannot make it: the earlier you do, the shorter the cooldown.
