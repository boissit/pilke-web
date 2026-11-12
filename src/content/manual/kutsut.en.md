---
title: Invites
lead: An invite comes with the times and places already in it. The person who gets it picks one time and one place, and it's a date.
order: 50
draft: false
---

## What goes in an invite

Pick the times and places on the card that suit you. An invite needs at least {{invitation.min_times_offered}} time and at least {{invitation.min_venues_offered}} place. So that whoever gets it has a choice, it also needs at least {{invitation.choice_threshold}} places or times, for example 3 times and 1 place, or 1 time and 2 places.

The person who gets it picks one of your times and one place. The date starts at the beginning of the chosen time, and the suggested length of a date is {{date.length_hours}} hour.

![An invite received: the times and places offered, and the Decline and It's a date! buttons](shot:invitation#timeslot-*,venue-*)

When you get an invite, pick the final time (1) and the final place (2) for the date. **Back** closes the screen, but the invite stays open and the clock keeps running.

## How long you have to answer

You have {{invitation.answer_hours}} hours from when an invite is sent to answer it. About {{invitation.expiry_warning_hours}} hours before time runs out, you get a reminder if you haven't answered yet and [reminders are on](/en/guide/tiedot-ja-tili#notifications). An unanswered invite expires on its own, and whoever sent it is told.

## An open invite holds its times

Every time offered in an invite is held for both of you until the invite ends. Neither of you sees those times on other matches' cards, and neither of you can offer them in another invite. Your calendar shows them as taken, and you can't change them.

When the invite is accepted, only the time of the date stays held, and the rest are freed. When it's declined, expires or is withdrawn, they're all freed straight away.

![An invite you sent: the times and places offered, with Withdraw invite at the bottom](shot:sent#withdraw-invitation-open)

To take back an invite you've sent, press **Withdraw invite** (1).

## What happens to your invite

| How it ends | For whoever sent it | For whoever got it |
|---|---|---|
| **Accepted.** It's a date. | The sparks stay spent. You're told. | No time-out. |
| **Declined.** | {{petals.refund}} sparks come back to you. You're told. | You can't look for new matches for {{cooldown.decline_hours}} hours. |
| **Expired.** Nobody answered within {{invitation.answer_hours}} hours. | {{petals.refund}} sparks come back to you. You're told. | You can't look for new matches for {{cooldown.no_answer_hours}} hours. |
| **Withdrawn.** The sender took it back before it was answered. | No refund. You can't look for new matches for {{cooldown.withdrawal_hours}} hours. | If you'd already been told about the invite, you're told it was withdrawn. |

After an invite, the two of you aren't suggested to each other again. The exception is when you went on the date and both said you'd like to meet again through Pilke.

Cancelling a date is covered in [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).
