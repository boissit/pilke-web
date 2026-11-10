---
title: Invites
lead: An invite comes with the times and places already in it. The other person picks one of each, and it's a date.
order: 50
draft: true
---

You send an invite to one of your matches. It cost {{petals.set_cost}} sparks, which went when you pressed **Find a date**. See [Sparks](/en/guide/kipinat).

## What you offer

From the times and places on a card, you pick the ones that suit you. An invite has to have:

- at least {{invitation.min_times_offered}} time and at least {{invitation.min_venues_offered}} place, and
- a choice: at least {{invitation.choice_threshold}} times or at least {{invitation.choice_threshold}} places.

The other person picks exactly one of your times and one place. The date starts at the beginning of the chosen time and, as far as Pilke's concerned, lasts {{date.length_hours}} hour.

![An invite received: the times and places offered, and the Decline and It's a date! buttons](shot:invitation#timeslot-*,venue-*)

On an invite you receive, you pick one time (1) and, if there's more than one place, one place (2). **Back** only closes the screen: the invite waits, but the clock keeps running.

## Time to answer

An invite has to be answered within {{invitation.answer_hours}} hours of being sent. If you haven't answered, you get a reminder about {{invitation.expiry_warning_hours}} hours before it expires, if reminders are on in Settings. An unanswered invite expires on its own, and whoever sent it is told.

## An open invite holds its times

While an invite is open, every time it offers is held for both of you. Neither of you sees those hours on other matches' cards, and neither of you can offer them in another invite. That's why your calendar shows them as taken, and why you can't change them.

When the invite is accepted, only the agreed time stays held and the rest are freed. When it's declined, expires or is withdrawn, they're all freed straight away.

![An invite you sent: the times and places offered, with Withdraw invite at the bottom](shot:sent#withdraw-invitation-open)

**Withdraw invite** (1) takes back an invite you sent: see below for what happens next.

## What happens to your invitation

| How it ends | For the person who invited | For the person invited |
|---|---|---|
| **Accepted.** It's a date. | The sparks stay spent. You're told. | No time-out. |
| **Declined.** | {{petals.refund}} sparks come back to you. You're told. | You can't look for new matches for {{cooldown.decline_hours}} hours. |
| **Expired.** Nobody answered within {{invitation.answer_hours}} hours. | {{petals.refund}} sparks come back to you. You're told. | You can't look for new matches for {{cooldown.no_answer_hours}} hours. |
| **Withdrawn.** Taken back before an answer. | No refund. You can't look for new matches for {{cooldown.withdrawal_hours}} hours. | If they'd already been told about the invite, they're told it was withdrawn. |

The invited person's sparks stay as they are, whatever happens. You're told if that notification is on in Settings.

However an invite ends, the two of you aren't suggested to each other again. The only exception is when you went on the date and both said you'd like to meet again.

Cancelling a date is covered in [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).
