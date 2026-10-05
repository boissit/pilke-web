---
title: Invitations
lead: An invitation comes with the times and places already in it. The other person picks one of each, and the date is agreed.
order: 50
draft: true
---

You send an invitation to one of your candidates. It costs {{petals.set_cost}} petals, and they went when you pressed **Send an invitation!** and found your candidates. See [Petals](/en/guide/teralehdet).

## What you offer

From the times and venues on a card you pick the ones that suit you. An invitation has to have:

- at least {{invitation.min_times_offered}} time and at least {{invitation.min_venues_offered}} venue, and
- a choice: at least {{invitation.choice_threshold}} times or at least {{invitation.choice_threshold}} venues.

The other person picks exactly one of your times and one venue. The date starts at the beginning of the chosen time and, as far as Pilke is concerned, lasts {{date.length_hours}} hour.

![A received invitation: the times and venues offered, and the Decline and Agreed! buttons](shot:invitation#timeslot-0,venue-0)

On an invitation you receive, you pick one time (1) and, if there is more than one venue, one venue (2). **Decide later** only closes the screen: the invitation waits, but the clock keeps running.

## Time to answer

An invitation has to be answered within {{invitation.answer_hours}} hours of being sent. If you have not answered, you get a reminder about {{invitation.expiry_warning_hours}} hours before it lapses, if reminders are on in Settings. An unanswered invitation lapses on its own, and whoever sent it is told.

## An open invitation holds its hours

For as long as an invitation is open, every time it offers is held for both of you. Neither of you is shown those hours on other candidates' cards, and neither of you can offer them in another invitation. That is why your calendar shows them as taken, and why they cannot be changed.

When the invitation is accepted, only the agreed time stays held and the rest are freed. When it is declined, lapses or is withdrawn, all of them are freed straight away.

![A sent invitation: the times and venues offered, with Withdraw the invitation at the bottom](shot:sent#withdraw-invitation-open)

**Withdraw the invitation** (1) takes back an invitation you sent: see below for what follows.

## What happens to your invitation

| Ending | For the one who invited | For the one invited |
|---|---|---|
| **Accepted.** The date is agreed. | The petals stay spent. You are told. | No petals, no cooldown. |
| **Declined.** | {{petals.refund}} petals back. You are told. | No petals. You cannot look for new candidates for {{cooldown.decline_hours}} hours. |
| **Lapsed.** Nobody answered within {{invitation.answer_hours}} hours. | {{petals.refund}} petals back. You are told. | No petals. You cannot look for new candidates for {{cooldown.no_answer_hours}} hours. |
| **Withdrawn.** Taken back before an answer. | No refund. You cannot look for new candidates for {{cooldown.withdrawal_hours}} hours. | If they had already been told about the invitation, they are told it was withdrawn. |

You are told if the notification is on in Settings.

However an invitation ends, the two of you are not suggested to each other again. The only exception is when you went on the date and both said you would like to meet again.

Calling off an agreed date is covered in [Cancelling and cooldowns](/en/guide/peruminen-ja-jaahy).
