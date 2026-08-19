---
title: Privacy policy
lead: What Pilke collects, what it is used for, and what you can ask us to do.
version: 2026-09-01
effective: 2026-09-01
draft: true
---

> **Note to whoever finishes this.** A draft. The structure and register follow Finnish
> practice — Wolt Oy's privacy statement, with the dating-specific sections modelled on
> Tinder's Finnish one — while **the content is written from Pilke's own source**, by way
> of the audit in `docs/legal/privacy-policy.md`, and is copied from neither. Every
> `TODO(legal)` is an owner or counsel decision that cannot be read out of the code; do
> not fill one in with what a dating app usually says. The Finnish is the original and
> this is its translation. Once a lawyer has read the finished text, remove `draft: true`
> and this note.

## 1. Who processes your data

The controller of your personal data is **[TODO(legal): the company's registered name,
business ID and address]**, which provides the Pilke app.

For anything to do with data protection, write to
**[TODO(legal): email address — this cannot be published without one, see GDPR Art. 13]**.

**[TODO(legal): has a data protection officer been appointed? If so, name and contact
details here.]**

## 2. Who this concerns

This policy concerns you if you use Pilke. It also concerns two people who do not use the
app themselves:

- **The trusted person** whose phone number you have saved for the safety feature. The
  number is their data rather than yours, which is why it is shown to nobody else.
- **Somebody another user writes a safety report about.** The subject of a report did not
  write it and could not have prevented it.

## 3. What we process

### 3.1 Account and profile

| Data | Detail |
| --- | --- |
| Phone number | This is how you identify yourself. The account has no password. |
| Email address | Asked for at registration. |
| Nickname | Shown to other users. |
| Date of birth | We store the day, but other users are shown only your age. |
| Gender | Shown to other users. |
| Photo | Shown to other users. |
| Language | Finnish or English. Decides which language notifications and text messages arrive in. |
| Trusted person's phone number | Optional. Shown to nobody but you. |
| What you are looking for | Which genders you are interested in, what kind of dates, an age range, languages. |
| Date area | A point you pick on a map and a radius in kilometres. You never tell us where you live. |
| Registration time and account state | |

What you are looking for includes whether you are looking for sex. **[TODO(legal):
counsel's view on whether this, together with your gender and the genders you are
interested in, is a special category of personal data under GDPR Art. 9, and what follows
for this policy.]**

### 3.2 Signing in

A sign-in code is six digits, valid for five minutes, and stops working after a fifth
wrong guess. Every signed-in device leaves its own row, and only a hash of the session
token is stored — never the token itself. A session expires after 90 days unused. We also
limit how often a code can be requested for the same number.

### 3.3 Calendar, dates and glimmers

| Data | Detail |
| --- | --- |
| Calendar | The times you have marked as free. |
| Credited times | Which of the times you marked earned you glimmers, including ones you later withdrew. |
| Candidates | Who the system worked out as a possible date for you. |
| Candidate draws | Who was offered to you, and who you picked. |
| Dates and invitations | The two parties, the time proposed and agreed, the venue, the state, and who called it off and why. |
| Glimmer ledger | Every movement of glimmers, with its reason. |
| Slowdowns | Any consequence you are currently serving, and why. |
| Blocks | Pairs who are never offered each other again. |

### 3.4 Question sets and feedback

You answer a question set by choosing an option; there is no way to write free text. The
same is true of the feedback after a date: an answer is a choice, not a sentence.

⚠️ **Your answers to the question sets do not currently affect who is suggested to you.**
We collect them, but candidates are narrowed by gender, age, date type, area, calendar,
slowdowns and blocks.

### 3.5 Notifications and devices

Each device leaves a push identifier, its platform, and when that identifier was last
registered. The identifier is refreshed every time the app starts. We also keep a queue
of every notification sent: what it is about, which date it concerns, and the outcome of
delivery per device. **A notification's content often carries the other party's
nickname.**

### 3.6 Safety records

- **A safety report** and its free text. This is the only place in the whole service
  where anybody can write free text about another person.
- **A report of not turning up**, in both directions.
- **A record that the safety button was pressed**, and who the message went to.
- **A block**, created when somebody calls off a date because they did not feel safe. The
  other party is not told the reason.

### 3.7 What we do not collect

Worth saying out loud, because it is unusual:

- No analytics and no advertising identifiers.
- No cookies. Pilke is not a website, and this site sets none.
- No crash reporting.
- No chat. Users cannot send each other messages at all.
- We never ask for your home address, and we never read your device's location except as
  described in 4.2.

**[TODO(legal): what the server and network logs record — IP addresses, for instance, and
for how long. The application writes none, but the hosting does.]**

## 4. Location

The word location means two entirely different things in Pilke, and they cannot be
described together.

### 4.1 Your date area — not your device's location

You pick a point and a radius on a map: how far you could travel for a date. You set it
yourself, it comes from no sensor, and it decides which venues are within your reach and
therefore who we can suggest to you. **It is not shown to other users.** You can change
it in the settings at any time, and it is deleted when you delete your account.

### 4.2 Showing your location at the venue

When a date is starting, you can show your location to the person you are meeting. There
is one purpose: two people who have never met find each other outside the bar.

**The location is exact.** It is not blurred, coarsened or approximated — it is where your
phone is, to about a metre. We do not offer that precision as a safeguard, because it is
not one. There are five safeguards, and these are they:

1. **The date has to be agreed and it has to have a venue.** Otherwise the feature does
   not exist.
2. **The window is twenty minutes** — ten minutes either side of the agreed start. It has
   nothing to do with when the date ends. Outside it, a location can neither be shown nor
   seen.
3. **Within 300 metres of the venue.** Your phone checks this before it sends anything,
   and the server checks it again. A location attempted from your sofa never leaves your
   device at all.
4. **One recipient:** the person you are meeting. No other user sees it, and it is not
   carried into any staff view.
5. **Deletion.** The row is deleted when the window closes, by a job that runs every
   minute — so its real lifetime is at most about 21 minutes. When you stop showing it
   yourself, the row goes immediately, and no record of that is kept. A missing location
   cannot be told apart from never having shown one.

The location is used for nothing else. No consequence, no report and no compensation
reads it.

Showing it continues when you leave the screen or put the phone in your pocket — that is
the point, and it is why the app says so before you agree. We do not ask for background
location access beyond these twenty minutes.

⚠️ **One qualification it is honest to make.** The first time you show your location, a
notification goes to the other party with your nickname in its title. The location itself
is not in that notification, but the fact that you arrived travels through the push
service and Google (section 8).

## 5. What other users see about you

Another user sees **your nickname, your age, your gender and your photo** — nothing else.
They also see the chosen venue and time, the times you offered, and, inside the window at
the venue, your location if you show it.

Another user **never** sees your phone number, your email address, your date of birth,
your trusted person's number, your date area, what you are looking for, your glimmer
balance, your slowdowns, your feedback or any report.

## 6. What we use your data for

1. Creating an account and signing in.
2. Finding candidates: gender, age, what you are looking for, area, calendar, slowdowns
   and blocks.
3. Arranging and running a date: invitations, choosing a time and a venue, calling off.
4. Helping the two of you find each other at the venue (4.2).
5. Notifying you about invitations, arrival and feedback prompts.
6. Safety: blocks, reports, the safety button and the slowdowns that follow.
7. Fair use of the service: slowdowns from calling off and not turning up, and the glimmer
   economy that paces invitations.
8. The question sets. We collect them now; they do not yet affect candidates (3.4).
9. Support and dealing with misuse.

## 7. The basis for processing

**[TODO(legal): the lawful basis for each purpose in section 6. This cannot be read out of
the code, and a wrong guess is the expensive kind. The specific questions:**

- **the core service (1–5): contract or consent;**
- **showing your location (4): separate consent, or contract necessity with a confirmation
  on top;**
- **what one user writes about another: the subject has not consented and cannot.
  Legitimate interests is the obvious candidate and needs a documented balancing test;**
- **the trusted person's number: the code assumes that somebody saving a number has that
  person's permission. An assumption is not a lawful basis;**
- **date type and gender preferences, if they are Art. 9 data (3.1);**
- **the free text in a safety report, plus Art. 10 if it describes an offence.]**

## 8. Who receives your data

**Other users**, to the extent described in section 5.

**Your trusted person**, one text message carrying your nickname, if you press the safety
button. The message names no location, no venue and no date partner.

**The push service (Expo, 650 Industries, Inc., United States)**: your device's push
identifier, and the notification's title, body and content. In three of the four kinds of
notification, that content carries the other party's nickname. Expo passes the
notification on to **Google's FCM**, which is therefore also a recipient.
**[TODO(legal): the contracting entity, whether a data processing agreement is signed, and
the transfer mechanism.]**

**The text message provider (GatewayAPI, Denmark)**: the recipient's phone number and the
message body. Two kinds: a sign-in code to your own number, and a safety message to your
trusted person's number. The service is in the EU. ⚠️ **No text message is sent from any
environment today**, because the provider is not yet connected. **[TODO(legal): whether a
data processing agreement is signed.]**

**The map service (OpenFreeMap)**: your device's IP address and the map tiles it requests
— which is to say, which area you are looking at. The request goes from your device, not
from our server. This covers choosing your date area, an invitation's map, and the map at
the venue. **[TODO(legal): the operating entity, its country, and whether a processing
agreement is possible at all with a free service. If not, the map service has to change.]**

**The hosting provider [TODO(legal): provider, country and processing agreement]**. Every
piece of personal data in this service lives in one database, with the photos beside it.

**Pilke's staff**, through an administration view. Location rows do not appear there at
all. Reports of not turning up are read-only, to us as well. **[TODO(legal): how many
people hold administrative access.]**

**Google Play**, whatever it receives as the app's distributor.

We do not sell your data and we do not pass it on for marketing.

## 9. Transfers outside the EU

Push notifications travel to the **United States** (Expo) and on to Google. This is the
one transfer that certainly happens today. **[TODO(legal): the transfer mechanism.]**

The text message provider is in Denmark, inside the EU. The countries of the hosting
provider and the map service are **[TODO(legal)]**.

## 10. How long we keep it

These delete themselves:

| Data | Rule |
| --- | --- |
| A shown location | When the window closes; the deletion job runs every minute. Also immediately when you stop showing it. |
| The notification that you arrived | By the same job, including ones already delivered. |
| A sign-in code | Replaced by the next one; stops working after five minutes. |
| Background job results | 7 days, or 30 if the job failed. |

⚠️ **Everything else is currently kept with no time limit.** Dates, glimmer movements,
calendar credits, slowdowns, blocks, reports of not turning up, safety reports with their
free text, safety messages, candidate draws and feedback all stay. No scheduled job
deletes any of them.

**[TODO(legal): a retention period for every group above. GDPR Art. 5(1)(e) requires one
and the code has none. The two most urgent are the free text in a safety report and the
permanent block, because both concern somebody who did not write them.]**

## 11. What happens when you delete your account

You can delete your account in the app's settings. It happens immediately, it cannot be
undone, and there is no grace period. The page on
[deleting your data](/en/tietojen-poisto) says what goes and what stays.

In short: **the account's details are wiped, and the row stays.** Your phone number, email
address, nickname, date of birth, gender, photo, trusted person's number, what you are
looking for and your date area are all deleted, and the photo goes from storage as well.
Every device is signed out in the same instant.

Two groups remain, and neither can be deleted:

- **Data that belongs to the other person as much as to you.** Dates, feedback, reports of
  not turning up, and safety reports. The other person sees *Someone* where you were.
- **Safety decisions that leaving must not undo.** A block created because somebody did
  not feel safe stays. Otherwise leaving the service would be a way to undo another
  person's safety decision.

Glimmer movements also stay, so that balances still add up, along with a record that the
account existed.

You can register the same phone number again. You get an empty account, and nothing links
it to the old one.

## 12. Your rights

You have the right to

- **access** your data;
- **correct** anything inaccurate;
- **erase** your data to the extent the law allows (section 11);
- **restrict** processing;
- **object** to processing;
- **port** your data from one system to another;
- **withdraw consent**, where processing rests on it;
- **not be subject to a decision based solely on automated processing** (section 15).

Some of these you can exercise yourself: your profile and preferences are visible and
editable in the settings, you stop showing your location with one tap, and you delete your
account from the settings.

Two limitations that are true today, said plainly:

- **There is no machine-readable export.** The app has no export function, so a request is
  handled by hand.
- **You cannot see what somebody else wrote about you**, and it cannot be corrected.
  Reports are read-only, to us as well.

Send requests to the contact address in section 1.
**[TODO(legal): how a requester is identified, and the time within which we answer.]**

## 13. How to complain

If you think we are processing your personal data contrary to data protection law, you can
complain to the Finnish Data Protection Ombudsman.

Tietosuojavaltuutetun toimisto, PL 800, 00531 Helsinki, Finland. Switchboard
+358 29 566 6700. More information and forms: [tietosuoja.fi](https://tietosuoja.fi/en/).

We would rather you came to us first, but you may complain directly.

## 14. Security

What we do, rather than guarantees.

- **The account has no password.** Signing in uses a one-time code to your phone number.
  Only a hash of the session token is stored, never the token, and every device signs in
  separately.
- On the phone the session token sits in the operating system's secure store, and is
  excluded from device backups.
- Administrative access is limited: location rows are not shown in it at all, and reports
  of not turning up are read-only.
- ⚠️ **Photos sit at an address that requires no sign-in.** Anybody who knows a photo's
  address can fetch it. **[TODO(legal): whether this is fixed before launch or disclosed
  here.]**

**[TODO(legal): this policy says nothing about encryption in transit, because the Android
app currently also permits an unencrypted connection. Remove that setting before launch and
add a sentence, or leave the sentence out.]**

## 15. Automated decisions

Finding candidates is automated, but it produces a **suggestion**: three candidates, which
you may ignore.

**Slowdowns** are automated and they are adverse to you. They mean you do not appear among
other people's candidates, or that you cannot draw new ones, and they follow from calling
off and from not turning up.

⚠️ One of them rests on **another person's word**: if somebody reports that you did not
turn up, the slowdown is imposed automatically and lifts by itself only if you file a
counter-report within a day. **[TODO(legal): counsel's view on Art. 22, and whether a
counter-report amounts to human review.]**

A safety report causes nothing automatically. A person handles it.

## 16. Changes to this policy

Every version has a date, and it is shown at the top of this page. The app displays the
same version alongside the terms, and we record the version you accepted.

**[TODO(legal): how a change is communicated, and whether a new version has to be accepted
or merely shown. Note that accounts created before the first published version have
accepted nothing, and that is recorded as empty.]**
