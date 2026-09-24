---
title: How candidates are chosen
lead: Who ends up in a set, in what order, and why sometimes nobody does.
kind: explainer
order: 20
draft: true
---

When you open a set, Pilke goes through everybody and sets aside anyone a date could not work with. From whoever is left it picks the {{candidates.per_set}} who suit you best. If there are not {{candidates.per_set}} of them, no set is opened and no petals are spent.

## Who a date is possible with

A candidate has to meet all of these, and every one is checked both ways: you have to fit their wishes as well.

- **Gender.** They are a gender you are looking for, and you are one they are looking for.
- **Age.** Their age is inside your range, and yours inside theirs.
- **What you expect from a date.** You share at least one answer.
- **Language.** You share a language.
- **Things to do.** You want at least partly the same kind of date.
- **Place.** There is at least one venue in an area you both chose, and it suits what you both want to do.
- **Time.** Your calendars share at least a {{calendar.min_shared_hours}}-hour stretch.

Times already offered in an open invitation, or held for an agreed date, do not count as shared. They are freed again if the invitation is declined or lapses.

## Who is never suggested

These people are not suggested even when everything above fits:

- people whose profile is missing details
- people on a cooldown that keeps them out of other people's candidates ([Cooldowns](/en/guide/jaahdytys))
- anybody you have already had an invitation with, in either direction and whatever the answer
- anybody who has already been in {{candidates.max_appearances}} of your sets
- people who want to date less often and already have an agreed date coming up
- anybody who filed a safety report about you, or whom you filed one about. That block is permanent.

One invitation per pair is the rule. There is one way round it: if you both said after a date that you would like to meet again, you can be suggested to each other again.

## In what order

The best of the candidates sits in the middle of the set. Two things decide the order:

- **The personality quiz.** The more alike your story test answers, the higher a candidate ranks. With no answers in common, a candidate gets a middling score.
- **Seen recently.** A candidate who was in one of your sets recently sinks down the order. The effect halves every {{candidates.exposure_half_life_days}} days, so the same person can come round again later.

Question set answers do not affect candidates at the moment. Neither petals nor anything else buys a better place.

## What a card shows

A card shows at most the {{candidates.times_per_card}} soonest times you share and at most {{candidates.venues_per_card}} of the places you share. When you share more places than that, different candidates' cards can show different ones.

A set stays open for {{candidates.set_hours}} hours, or until its times go by.

## When nobody is found

When a set cannot be opened, the app tells you which of the rules ruled out the last of them:

| Message | What you can do |
|---|---|
| *What you are looking for does not match anybody right now.* | Widen your age range, or add options in Your details. |
| *Nobody suitable wants the same kind of date as you.* | Add more date activities. |
| *There is nobody suitable in your date area.* | Choose more date areas. |
| *Nobody suitable shares a single time with you.* | Mark more times in your calendar. The yellow hours show when other people are free. |
| *There are too few suitable people right now.* | Try again later. |

## How you are suggested to other people

The same rules apply when somebody else opens a set. You can be suggested to them if your wishes agree, you share a venue and you share some time. The more times you mark, the more people you can be a candidate for.
