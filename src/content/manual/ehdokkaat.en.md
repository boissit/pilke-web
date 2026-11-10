---
title: Who you're shown
lead: Why these people are your matches, what order you see them in, and why someone stops showing up.
order: 40
draft: true
---

You find {{candidates.per_set}} matches at a time. Pilke goes through everyone you could go on a date with and picks the {{candidates.per_set}} who suit you best. If there aren't {{candidates.per_set}}, your sparks stay put.

![Your matches: the middle match's card, the times you're both free and the places](shot:platter#timeslot-chip-*,activity-chip-*)

Each card shows the match's photo, name and age, up to {{candidates.times_per_card}} of the soonest times you're both free (1), and up to {{candidates.venues_per_card}} places that suit you both (2). You build your invite from these. See [Invites](/en/guide/kutsut).

## Favourite spots

You can choose up to {{candidates.favourite_venues_max}} favourite spots on the Places page of Your details. When a favourite suits you both, it comes first on a candidate's card. Your candidates are chosen the same way as always; favourites only decide which places their cards show first.

On a card, a star tells you whose favourite a spot is: {star:mine} is yours, {star:theirs} theirs, and {star:both} a favourite of you both. You'll see the same stars on the invitation and on the date's page.

A favourite stays saved if you remove its date area or date activity from your choices, and works again once you choose them.

## Why these people

A match has to meet every one of these, and each is checked both ways: you have to fit their preferences too.

- **Shared time.** You're both free for at least {{calendar.min_shared_hours}} hour at the same time. Hours already held by an open invite or an upcoming date don't count.
- **Date area.** An area you've both chosen has a place that suits what you both want to do.
- **Language.** You have at least one language in common.
- **Things to do.** You want at least some of the same kinds of date.
- **Preferences.** Gender and age fit what each of you is looking for, and you want at least one of the same things from a date.
- **A choice.** You share at least {{invitation.choice_threshold}} times or at least {{invitation.choice_threshold}} places, so an invite can offer a choice.

**How often you date** counts too: *How often would you like to go on a date?* on the Times page of Your details. If someone chose *Once a week*, they're suggested for times before their latest upcoming date, or from {{matching.pace_weekly_days}} days after it (*Once every two weeks*: {{matching.pace_fortnightly_days}} days). The same goes for you when you're suggested to others. When you look for matches yourself, your own pace counts too: times that respect it come first.

## Why someone stops showing up

- **One of you has already invited the other.** Once there's been an invite between two people, either way and however it ended, they aren't suggested to each other again. The exception is when you both said after a date that you'd like to meet again. See [After the date](/en/guide/treffien-jalkeen).
- **They were shown to you recently.** A recently shown match moves down the order, and the effect halves every {{candidates.exposure_half_life_days}} days. Once someone has been among your matches {{candidates.max_appearances}} times, they aren't shown to you again.

## Who comes first

The personality quiz shapes the order: the more of its questions you've both answered the same way, the higher a match comes. Recently shown matches move down, as above.

## How long your matches wait

Your matches wait for you for {{candidates.set_hours}} hours. If you leave, the button on the Dates page says **Finish your invite** and takes you back to the same matches without spending more sparks. You can look for new matches once you've sent an invite or these have expired.

Your matches expire sooner if any of them can no longer be invited: the times on their card have passed, or another invite has taken them. Then they all expire, and you don't get the sparks back.

When you send an invite, the other two matches go.

![A notice on the Dates page: you can't look for new matches until a given time](shot:cooldown-nodraw#cooldown-notice)

If you can't look for matches right now, the Dates page shows a notice (1) with the reason and when it ends. See [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).

## Questions

**Why weren't any matches found?** There were fewer than {{candidates.per_set}} people who suit you. The app says which condition ruled out the last of them: your preferences, things to do, date areas, shared time, or simply too few people who suit you right now. Its button takes you straight to the calendar or to the page in Your details where you can change it, and **Next steps** on the Dates page shows the same steps. Marking more time usually helps most, especially in the yellow hours. Your sparks stay put.

**Can someone see that they were one of my matches?** No. A match only finds out about you when you send them an invite.

**How do I get suggested more often?** Mark more time, especially in the yellow hours, and choose more date areas and things to do. While you're on a time-out, you aren't suggested to anyone.
