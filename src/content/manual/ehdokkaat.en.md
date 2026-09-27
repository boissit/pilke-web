---
title: Who you are shown
lead: Why these people are your candidates, in what order you see them, and why someone stops turning up.
order: 40
draft: true
---

You find {{candidates.per_set}} candidates at a time. Pilke goes through everyone you could have a date with and picks the {{candidates.per_set}} who suit you best. If there are not {{candidates.per_set}} of them, no petals are charged.

![The Candidates screen: the middle candidate's card, the times you both have and something to do together](shot:platter#timeslot-chip-0,activity-chip-0)

Each card shows the candidate's photo, name and age, up to {{candidates.times_per_card}} of the soonest times you both have free (1), and up to {{candidates.venues_per_card}} venues that suit you both (2). Those are what you build an invitation from. See [Invitations](/en/guide/kutsut).

## Why these people

A candidate has to meet every one of these, and each is checked both ways: you have to fit their wishes too.

- **Shared time.** Your calendars share at least {{calendar.min_shared_hours}} hour. Hours already held by an open invitation or an agreed date do not count.
- **Date area.** An area you have both chosen has a venue that suits what you both want to do.
- **Language.** You have at least one language in common.
- **Things to do.** You want at least partly the same kind of date.
- **Wishes.** Gender and age fit what each of you is looking for, and you share an answer to what you want from a date.
- **A choice.** You share at least {{invitation.choice_threshold}} times or at least {{invitation.choice_threshold}} venues, so an invitation can offer a choice.

**The pace setting** counts too: *How often would you like to go on a date?* in Your details. Someone who chose *Once a week* is not shown to anyone while they have an agreed date within {{matching.pace_weekly_days}} days either way. *Once every two weeks* works the same within {{matching.pace_fortnightly_days}} days. The same applies to you when you are someone else's candidate. It does not limit when you find candidates yourself.

## Why someone stops turning up

- **One of you has already sent the other an invitation.** Once there has been an invitation between two people, either way and however it ended, they are not suggested to each other again. The exception is when you both said after a date that you would like to meet again. See [After the date](/en/guide/treffien-jalkeen).
- **They were shown to you recently.** A recently shown candidate moves down the order, and the effect halves every {{candidates.exposure_half_life_days}} days. Once someone has been among your candidates {{candidates.max_appearances}} times, they are not shown to you again.
- **One of you made a safety report.** Then you are never suggested to each other again.

## In what order

The personality quiz shapes the order: the more of its questions you have both answered the same way, the higher a candidate comes. Recently shown candidates move down, as above.

## How long your candidates wait

Your candidates wait for you for {{candidates.set_hours}} hours. If you leave, the button on the Dates page reads **Finish your invitation** and takes you back to the same candidates at no cost. You can find new candidates once you have sent an invitation or these candidates have expired.

Your candidates expire sooner if any one of them can no longer be sent an invitation: the card's times have passed, or they have been taken by another invitation. Then they all expire, and no petals come back.

When you send an invitation, the other two candidates go.

![A notice on the Dates page: you cannot look for new candidates until a given time](shot:cooldown-nodraw#cooldown-notice)

If you cannot find candidates right now, the Dates page carries a notice (1) with the reason and the time it ends. See [Cancelling and cooldowns](/en/guide/peruminen-ja-jaahy).

## Questions

**Why were no candidates found?** There were fewer than {{candidates.per_set}} suitable candidates. The app says which condition ruled out the last of them: your wishes, things to do, date areas, shared time, or simply too few suitable people right now. Marking more time usually helps most, especially in the yellow hours. No petals are charged.

**Can someone see they were my candidate?** No. A candidate only learns about you when you send them an invitation.

**How do I get suggested more often?** Mark more time, especially in the yellow hours, and choose more date areas and things to do. You are not suggested to anyone during a cooldown.
