# Design standards for victoriaswart.com

Victoria's standards document, 5 November 2026, is the governing brief. This
file records what is enforced in code, what is a deliberate exception, and
what is still outstanding.

## Enforced in code

**Type scale.** Eight tokens in `:root`, and nothing is sized outside them:
`--fs-display --fs-h1 --fs-h2 --fs-h3 --fs-lead --fs-body --fs-caption
--fs-label`. Four heading levels, four text levels. Before this the stylesheet
held 33 different font-size values. 60 declarations now read from the scale.

**Two deliberate type exceptions**, each carrying its reasoning where it sits:
the landscape-phone hero override, because a phone on its side leaves about
320px under the header; and the footer wordmark, which is a number in an SVG
coordinate space rather than page typography.

**Measure.** Running text is capped at 68 characters. `section>*{max-width:100%}`
was cancelling this for any paragraph sitting directly in a section, which is
what made About read as loose text blocks at 1152px lines.

**Spacing.** Every margin, padding and gap of 8px or more is a multiple of 8.
103 values were snapped. Values under 8px are left alone on purpose: those are
optical corrections on inline elements and hairline offsets, not rhythm, and
snapping them to 8 would be worse rather than more consistent.

**Border radius.** One token, `--radius: 2px`, used by every card, button and
image. A 50% on a round dot stays, because that is a shape, not a corner.

**Colour.** Four families: black, bone, plum, accent. The `--forest` and
`--forest-2` aliases were resolved to the real tokens and deleted, since an
alias named for a colour the site does not use made the palette look larger
and the names misleading.

**Navigation.** Six plain links and one distinct CTA. Contact is now an
outlined button rather than a seventh flat link, which satisfies two rules at
once. Six is the stated maximum rather than the ideal 4 to 5: Journal is in
the nav because Victoria asked for the Substack essays to be visible.

**Target size.** WCAG 2.2 asks for 24x24 CSS pixels. Nav, footer, arrow links,
tick lists and the consent link gain padding rather than a larger type size,
so the scale is untouched and only the hit area grows. Three exemptions are
correct and intentional: the `_gotcha` honeypot, and inline links inside
sentences, which the success criterion explicitly exempts.

**Rhythm.** Bands alternate picture-right, picture-left. The flip applies only
above the 861px stacking breakpoint, so a phone always reads picture then
words and the order never jumbles.

## Verified

144 page-and-width combinations across all four languages at 360, 390, 414,
768, 861, 1024, 1280, 1440 and 1920: no horizontal scroll anywhere, header
holds at 72px, no element escapes the viewport.

## Languages, done 5 November

Four offerings, each with its own page in all four site languages: English,
Business English, Aviation English, German. 16 pages, every one carrying
correct hreflang, canonical and a single h1.

The hub keeps the introduction, my languages, how I teach, pricing,
translation, moderation and reviews, and links out through four doors. The two
specialisms used to be written out in full on the hub, which was most of why
it ran long; each can now rank on its own terms.

`.media-split` is gone from the page. Its 340px image cap is why the
roundtable photograph was the same small size at 861 and at 1280, and an
inline `max-width:min(520px,100%)` was doing the same to the speaking
photograph. Both are bands now. Verified: no band image is under 45% of the
viewport at any width from 861 up.

The second copy of the Naples photograph is gone from the hub; it lives on
About since the layout pass.

## Still outstanding

- **Portfolio**: scroll-based UX/UI animation for one project, with this site
  as the showcase.
- **Web Design**: project types as clickable blocks that open into detail.
- **HTTPS is not enforced.** `http://victoriaswart.com` still serves the full
  site unencrypted. GitHub, Settings, Pages, tick Enforce HTTPS.

## Reviews

Shown as text, never an embedded widget. A Google review carries the name as
Google shows it, a "Google review" label, and a link to the profile. The quote
stays in the language it was written in with the translation behind a toggle,
because the words belong to the person who wrote them. No widget and no Maps
iframe: both load third-party scripts, would make the privacy page untrue and
would force a consent banner onto a site that needs none.

## Privacy, 5 November

Three things GDPR Article 13 requires were missing and are now on the page in
all four languages:

- **Where the data goes.** Formspree is a United States company, so the name,
  email and message are processed outside the EU. Their own privacy policy
  confirms US processing but names no specific safeguard: no Data Privacy
  Framework certification, no standard contractual clauses, and their DPA page
  returned nothing. The page therefore states the transfer honestly and
  invites people to ask what safeguards apply, rather than claiming a
  mechanism that may not exist.
- **What the processing rests on.** You sent it, to get an answer or to begin
  working together.
- **The right to complain** to the Garante.

The cookies section now also discloses the two values the site saves in the
visitor's own browser: the dismissed language suggestion, and the referring
site that travels with the form. Both are functional, so no consent banner is
needed, but they are terminal storage and belong in the notice.

**Correction, 7 November.** The 5 November note here said Formspree named no
safeguard. That was wrong, and the mistake was mine: I had read their privacy
policy, where it is not stated, and found /legal/dpa returning 404, and
concluded there was none. Their security page says it plainly:

> We rely on Standard Contractual Clauses (SCCs) as a data processor.

They are also SOC 2 Type II audited. The privacy page now names the safeguard
rather than inviting people to ask about it.

**Still worth doing, but no longer urgent:** ask Formspree for a countersigned
DPA for the file. Relying on their published statement is reasonable; having
the paperwork is better. There is no DPA published at a public URL, so it has
to be requested from support.
