---
title: Who you're shown
lead: Why these people are your matches, what order you see them in, and why someone stops showing up.
order: 40
draft: true
---

You find {{candidates.per_set}} matches at a time. Pilke goes through everyone you could go on a date with and picks the ones who suit you best. If fewer than {{candidates.per_set}} suit you, the search is called off and no sparks are spent.

![Your matches: the middle match's card, the times you're both free and the places](shot:platter#timeslot-chip-*,activity-chip-*)

A match's card shows their photo, name and age. It also has up to {{candidates.times_per_card}} of the soonest times you're both free (1) and up to {{candidates.venues_per_card}} places that suit you both (2). You build your invite from these. See [Invites](/en/guide/kutsut).

## Favourite spots

You can choose up to {{candidates.favourite_venues_max}} favourite spots on the Places page of Your details. When a favourite suits you both, it comes first on a candidate's card. Your candidates are chosen the same way as always; favourites only decide which places their cards show first.

On a card, a star tells you whose favourite a spot is: {star:mine} is yours, {star:theirs} theirs, and {star:both} a favourite of you both. You'll see the same stars on the invitation and on the date's page.

A favourite stays saved if you remove its date area or date activity from your choices, and works again once you choose them.

## Why these people

A match has to meet all of these. Each one is checked both ways, so you have to fit their preferences too.

- **Shared time.** You share at least {{calendar.min_shared_hours}} hour of free time. Times already held by another open invite or an upcoming date aren't included.
- **Date area.** An area you've both chosen has a place that suits what you both want to do.
- **Language.** You have at least one language in common.
- **Things to do.** You've both asked for at least one of the same things to do.
- **Preferences.** Your gender, age and other preferences fit what the other is looking for.
- **Something to choose from.** You share at least {{invitation.choice_threshold}} times or {{invitation.choice_threshold}} places, so whoever gets the invite has a choice.

**How often you date** counts too. You choose it on the Times page of Your details, under *How often would you like to go on a date?* If a match chose *Once a week*, they're suggested for times before their latest upcoming date, or at least {{matching.pace_weekly_days}} days after it. With *Once every two weeks*, the gap is {{matching.pace_fortnightly_days}} days. When you look for matches yourself, times that fit your own pace come first.

Your personality quiz answers are the starting point for finding your matches. Later on, the feedback you give after your dates steers us towards the matches who suit you best.

## Why someone stops showing up

- **You've already been on a date.** Once two people have been on a date, they aren't suggested to each other again. The exception is when you both said in your feedback that you'd like to meet again through Pilke. See [After the date](/en/guide/treffien-jalkeen).
- **They were shown to you recently.** A recently shown match moves down the order, and the effect halves every {{candidates.exposure_half_life_days}} days. Once someone has been among your matches {{candidates.max_appearances}} times, you won't see them again.

## How long your matches wait

Your matches wait for you for {{candidates.set_hours}} hours. If you leave your invite unfinished, the button on the Dates page says **Finish your invite**. It takes you back to the same matches without spending more sparks. You can find new matches once you've sent an invite or these have expired.

Your matches expire sooner if any one of them can no longer be invited. That happens when the times on their card have passed or another invite has taken them. Then all your matches expire, and you don't get the sparks back.

When you send an invite, the other matches go.

![A notice on the Dates page: you can't look for new matches until a given time](shot:cooldown-nodraw#cooldown-notice)

If you can't find matches right now, a notice on the Dates page (1) tells you why and when your time-out ends. See [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).

## Questions

**Why weren't any matches found?** There were fewer than {{candidates.per_set}} people who suit you. The app tries to tell you if your choices can change this. Your preferences, things to do, date areas and shared time all affect it, and so can there being too few people who suit you signed up so far. Its button takes you straight to the calendar or to the page in Your details where you can change that condition. **Next steps** on the Dates page shows the same steps. Marking more time usually helps most, especially in the [highlighted hours](/en/guide/vapaat-ajat#the-yellow-hours). If no matches were found, no sparks are spent.

**Can someone see that they were one of my matches?** No. A match only finds out about you when you send them an invite.

**How do I show up more often in other people's matches?** Mark more time, especially in the [highlighted hours](/en/guide/vapaat-ajat#the-yellow-hours), and choose more date areas and things to do.
