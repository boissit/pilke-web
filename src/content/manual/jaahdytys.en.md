---
title: Cooldowns
lead: Call off an agreed date, withdraw an invitation or fail to turn up, and Pilke puts in a short pause. This is how it works.
kind: explainer
order: 30
draft: true
---

A cooldown is a pause after something that cost another person: an evening they set aside, or a wait. It takes no petals, and it is never a penalty for an answer. Declining an invitation never causes one.

A cooldown does one or both of two things:

- **You do not show up in other people's candidates.** Nobody can get you in a set.
- **You cannot look for new candidates.** You cannot open a new set.

## What you see

During a cooldown there is a notice at the top of the Dates page. It says what is in force, until when, and why. The same text appears on the Candidates screen if you try to look for candidates.

![Notice: you are not showing up in other people's candidates and cannot look for new ones](shot:cooldown-blocked#cooldown-notice)

**Both.** *You are not showing up in other people's candidates right now, and you cannot look for new candidates until …* This follows calling off an agreed date, or the other person telling us you did not turn up.

![Notice: you cannot look for new candidates](shot:cooldown-nodraw#cooldown-notice)

**No looking.** *You cannot look for new candidates until …* This follows withdrawing an invitation you sent before it was answered. You still show up in other people's candidates.

![Notice: you are not showing up in other people's candidates](shot:cooldown-hidden#cooldown-notice)

**Not showing.** *You are not showing up in other people's candidates until …* The app has a rule that can hide somebody whose invitations keep going unaccepted. That rule is not in use at the moment, so declining invitations, or leaving them unanswered, does not hide you.

With more than one cooldown in force, the notice gives the reason and end time of the one that lasts longest.

## How long

| What you did | How long |
|---|---|
| Withdrew an invitation you sent | {{cooldown.withdrawal_hours}} hours |
| Called off an agreed date at least {{cooldown.cancel_long_notice_days}} days ahead | {{cooldown.cancel_long_notice_hours}} hours |
| Called off an agreed date at least {{cooldown.cancel_short_notice_hours}} hours ahead | {{cooldown.cancel_short_notice_days}} days |
| Called off an agreed date later than that | {{cooldown.cancel_late_days}} days |
| The other person said you did not turn up | {{cooldown.noshow_days}} days |

Calling dates off repeatedly makes it longer. Each earlier call-off in the last {{cooldown.repeat_window_days}} days that led to a cooldown multiplies the next one by {{cooldown.repeat_multiplier}}. No cooldown ever lasts more than {{cooldown.ceiling_days}} days.

The earlier you call a date off, the shorter the pause. So call it off as soon as you know you cannot come.

## What a cooldown does not do

- It takes no petals.
- Your agreed dates and open invitations stay as they are.
- You can still answer invitations you receive, and go on your dates.
- It ends by itself at the time the notice gives.

If the other person says you did not turn up and you say the same about them, neither of you is penalised and your cooldown is lifted. See [Not turning up](/en/guide/saapumatta-jaaminen).

## The one permanent block

A cooldown is always temporary. The only permanent block comes from a safety report: if either of you says after a date that you did not feel safe, you are never suggested to each other again. It does not affect whether you show up for anybody else.
