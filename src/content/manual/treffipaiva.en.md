---
title: The day of the date
lead: How you find each other at the venue, and what to do if the other person does not come.
order: 70
draft: true
---

![An agreed date: the time, the place and the Finding each other map](shot:date#agreed-time,live-map)

The date's screen holds the agreed time (1), the place and a map (2). A reminder comes {{date.reminder_hours}} hour before, if it is on in Settings.

## Finding each other at the venue

You can share your location with your date on a map, so the two of you find each other. It is up to you.

- **When.** From {{sharing.lead_minutes}} minutes before the start to {{sharing.trail_minutes}} minutes after it. You are notified when it opens.
- **Where.** Only within about {{sharing.radius_m}} metres of the venue.
- **Who.** Only your date. They are notified when you are there.
- **For how long.** Your location is on the server only while you are sharing it. It is deleted as soon as you stop or the time runs out. All that is kept is the fact that a location was shared.

![The venue map and the Share my location button](shot:date-map#meet-up-reveal)

Sharing starts from **Share my location** (1) on the map.

![The question Share your location? and its explanation](shot:date-location-consent)

Before anything is shared, the app tells you what will happen and asks.

![The map while you are both sharing: what your date's pin says, and the Stop sharing my location button](shot:date-map-sharing#meet-up-status,meet-up-stop)

While you are sharing, the map shows you, the venue and your date, if they are sharing too. Under the map is when their location last updated (1). Your location keeps updating by itself, even with the phone in your pocket. Sharing stops when the time runs out or when you press **Stop sharing my location** (2).

## If the other person does not come

There is no messaging in the app, so the other person cannot tell you they are late. If you end up waiting alone, you can tell us, but only during the date and only at the venue:

- **When.** From {{noshow.grace_minutes}} minutes after the agreed start until the date ends, {{date.length_hours}} hour after the start. The first minutes leave room for being a little late.
- **Where.** Within about {{noshow.venue_radius_m}} metres of the venue. A report gives the other person a long cooldown on one person's word, and made on the spot it tells it as it was. Your phone checks your location at the moment you report, and it is not stored.

To report:

1. Stay at the venue.
2. **Did you end up waiting alone?** appears on the date's screen. Once {{noshow.grace_minutes}} minutes have passed since the start, press **Tell us they did not turn up**.
3. Confirm with **Tell us**.

![The report cannot be made because you are not at the venue](shot:date-noshow-not-at-venue#no-show-report)

If you are not at the venue, no report is made, and the app says so (1).

A report cannot be taken back, and we stop asking you for feedback on this date. The other person is left out of other people's candidates and cannot look for new ones for {{cooldown.noshow_days}} days, and their Dates page tells them a report has been made. If they too report, during the date and from the venue, that you did not turn up, neither of you is penalised and a member of Pilke's staff looks into it.

## Questions

**What happens when an invitation is accepted?** The date is agreed. The chosen time is held for both of you, the other times offered are freed, and whoever invited is told. The date appears under **Agreed dates** on the Dates page.

**Can the time or place be changed afterwards?** No. If what you agreed no longer works, call the date off, and a cooldown follows. See [Cancelling and cooldowns](/en/guide/peruminen-ja-jaahy).

**I am running late. Can I tell them?** No. Get there as soon as you can. The first {{noshow.grace_minutes}} minutes leave room for being a little late.

**I cannot find them at the venue.** Share your location on the map. They are notified when you are there and can see you on the map.

**How long does a date last?** As far as Pilke is concerned, {{date.length_hours}} hour from the start. After that you can give feedback: see [After the date](/en/guide/treffien-jalkeen). How long you actually stay is up to the two of you.

**Who can see where I am?** Only your date, only if you choose to share your location, and only for {{sharing.window_minutes}} minutes around the start.
