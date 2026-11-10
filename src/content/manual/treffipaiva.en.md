---
title: The day of your date
lead: How you find each other when you get there, and what to do if your date doesn't turn up.
order: 70
draft: true
---

![An upcoming date: the time, the place and the Finding each other map](shot:date#agreed-time,live-map..date-map-directions)

The date's screen shows the agreed time (1), the place and a map (2). A reminder comes {{date.reminder_hours}} hour before, if it's on in Settings.

## Finding each other at the venue

You can share your location with your date on a map, so you find each other. It's up to you.

- **When.** From {{sharing.lead_minutes}} minutes before the start to {{sharing.trail_minutes}} minutes after it. You're notified when it opens.
- **Where.** Only within about {{sharing.radius_m}} metres of the venue.
- **Who.** Only your date. They're notified when you're there.
- **For how long.** Your location is only on the server while you're sharing it. It's deleted as soon as you stop or the time runs out. All that's kept is the fact that a location was shared.

![The venue map and the Share my location button](shot:date-map#meet-up-reveal)

Sharing starts from **Share my location** (1) on the map.

![The question Share your location? and its explanation](shot:date-location-consent)

Before anything is shared, the app explains what will happen and asks you.

![The map while you're both sharing: both pins, when your date's location last updated, and the Stop sharing my location button](shot:date-map-sharing#meet-up-stop)

While you're sharing, the map shows you, the venue and your date, if they're sharing too. Under the map you can see when their location last updated. Your location keeps updating by itself, even with your phone in your pocket. Sharing stops when the time runs out or when you press **Stop sharing my location** (1).

## If the other person does not come

There's no messaging in the app, so your date can't tell you they're late. If you're left waiting, you can tell us, but only during the date and only at the venue:

- **When.** From {{noshow.grace_minutes}} minutes after the agreed start until the date ends, {{date.length_hours}} hour after the start. The first few minutes leave room for being a little late.
- **Where.** Within about {{noshow.venue_radius_m}} metres of the venue. A report gets the other person a long time-out on one person's word, and made on the spot, it reflects what really happened. Your phone checks your location at the moment you report, and it isn't stored.

To report:

1. Stay at the venue.
2. **Were you left waiting?** appears on the date's screen. Once {{noshow.grace_minutes}} minutes have passed since the start, press **Tell us they didn't turn up**.
3. Confirm with **Tell us**.

![You can't report because you're not at the venue](shot:date-noshow-not-at-venue#no-show-report)

If you're not at the venue, no report is made, and the app tells you so (1).

A report can't be taken back. After it, your feedback is a single tap: on the Dates page you confirm your date didn't turn up, and you get {{sparks.per_date}} sparks for it. Your date isn't shown to anyone else and can't look for new matches for {{cooldown.noshow_days}} days, and their Dates page tells them a report has been made. If they also report, during the date and from the venue, that you didn't turn up, neither of you is penalised and someone from the Pilke team looks into it.

If you couldn't report at the venue, you can tell us in your feedback after the date: answer *How did the date go?* with *The date didn't happen*, then *My date didn't turn up*. We pass it on to the Pilke team, and nobody gets a time-out because of it. See [After the date](/en/guide/treffien-jalkeen).

## Questions

**What happens when an invite is accepted?** It's a date. The chosen time is held for both of you, the other times offered are freed, and whoever sent the invite is told. The date shows up under **Upcoming dates** on the Dates page.

**Can the time or place be changed afterwards?** No. If what you agreed no longer works, cancel the date, and you'll get a time-out. See [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).

**I'm running late. Can I tell them?** No. Get there as soon as you can. The first {{noshow.grace_minutes}} minutes leave room for being a little late.

**I can't find them at the venue.** Share your location on the map. They're notified when you're there and can see you on the map.

**How long does a date last?** As far as Pilke's concerned, {{date.length_hours}} hour from the start. After that you can give feedback: see [After the date](/en/guide/treffien-jalkeen). How long you actually stay is up to the two of you.

**Who can see where I am?** Only your date, only if you choose to share your location, and only for {{sharing.window_minutes}} minutes around the start.
