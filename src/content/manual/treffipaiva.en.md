---
title: The day of your date
lead: How you find each other at the venue, and what to do if your date doesn't turn up.
order: 70
draft: false
---

![An upcoming date: the time, the place and the Finding each other map](shot:date#agreed-time,live-map..date-map-directions)

The date's screen shows the time of the date (1), the place and a map (2). You get a reminder {{date.reminder_hours}} hour before, if reminders are on.

## Finding each other at the venue

You can share your location with your date on the map, so you find each other more easily. Sharing is up to you.

- **When.** From {{sharing.lead_minutes}} minutes before the start to {{sharing.trail_minutes}} minutes after it. You're notified when you can start sharing.
- **Where.** Within about {{sharing.radius_m}} metres of the venue.
- **Who.** Only your date. They're notified when you're there.
- **For how long.** Your date can see your location for at most {{sharing.trail_minutes}} minutes after the date starts, or until you choose to stop sharing.

![The venue map and the Share my location button](shot:date-map#meet-up-reveal)

To start sharing, press **Share my location** (1) on the map.

![The question Share your location? and its explanation](shot:date-location-consent)

Before you share, the app asks for your permission.

![The map while you're both sharing: both pins, when your date's location last updated, and the Stop sharing my location button](shot:date-map-sharing#meet-up-stop)

While you're sharing, the map shows you and the venue. If your date is sharing too, you see them as well, and under the map it says when their location last updated. Your own location updates automatically, even with your phone in your pocket. Sharing stops when the time runs out or you press **Stop sharing my location** (1).

## If your date doesn't turn up

If your date doesn't turn up, you can tell us. You can only report it during the date and at the venue:

- **When.** From {{noshow.grace_minutes}} minutes after the start time until the date ends, {{date.length_hours}} hour after the start. The wait leaves room for being a little late.
- **Where.** Within about {{noshow.venue_radius_m}} metres of the venue. Your phone checks your location when you report, and your location isn't stored.

To report:

1. Stay at the venue.
2. The date's screen has a section called **Were you left waiting?** Once {{noshow.grace_minutes}} minutes have passed since the start, press **Tell us they didn't turn up** there.
3. Confirm with **Tell us**.

![You can't report because you're not at the venue](shot:date-noshow-not-at-venue#no-show-report)

If you're not at the venue, the app tells you so (1), and no report is made.

You can't take a report back. Your date gets a {{cooldown.noshow_days}}-day time-out, during which they aren't shown in anyone's matches and can't look for new matches. If they also make a report from the venue during the date, the Pilke team will try to get to the bottom of it.

If you didn't make a report at the venue, tell us in your feedback after the date. Answer *How did the date go?* with *The date didn't happen*, then *My date didn't turn up*. The Pilke team is told, but your date doesn't get a time-out from it. Your feedback earns you {{sparks.per_date}} sparks. See [After the date](/en/guide/treffien-jalkeen#if-the-date-didnt-happen).

## Questions

**What happens when an invite is accepted?** It's a date. The chosen time is held for both of you, and the other times offered are freed. Whoever sent the invite is told, and the date shows up under **Upcoming dates** on the Dates page.

**Can the time or place be changed afterwards?** No. If the time or place no longer works, cancel the date. Cancelling gets you a time-out. See [Cancelling and time-outs](/en/guide/peruminen-ja-jaahy).

**I'm running late. Can I tell them?** No. Get there as soon as you can. Your date can report you as a no-show {{noshow.grace_minutes}} minutes after the start time at the earliest.

**I can't find them at the venue.** Share your location on the map. They're notified when you're there and can see you on the map.

**How long does a date last?** As long as you like. The suggested length of a date is about {{date.length_hours}} hour.

**Who can see where I am?** Only your date, and only while you share your location. You can share it for {{sharing.window_minutes}} minutes around the start of the date, and only near the venue.
