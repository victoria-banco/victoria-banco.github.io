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

## Still outstanding

- **Languages**: each taught language on its own subpage, in all four site
  languages. Victoria confirmed all four. `.media-split` caps its image at
  340px, which is why the roundtable photograph is the same small size at 861
  and at 1280; that rule is now used only on Languages and gets replaced here.
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
