# Design rules for victoriaswart.com

From Victoria's note "MY WESITE", 4 November 2026. These are the standing
rules; anything new on the site is held to them.

## The rules

1. **Ping pong.** Bands alternate: picture right, picture left, picture right.
   Never two bands with the picture on the same side in a row.
2. **Blocks share edges.** Everything lines up on the same left edge or splits
   the screen cleanly in half. No floating insets at arbitrary widths.
3. **Font sizes stay consistent.** One size for a lead, one for body, one per
   heading level. A size is not picked per block.
4. **Text has a measure.** Running text never exceeds ~68 characters a line.
   Full-width paragraphs are what makes a page read as loose text blocks.
5. **One rhythm step between blocks.** Two stacked sections must not add their
   padding together and leave a void.
6. **Nothing starts without a transition.** A content band does not run
   straight into a decorative one in the same pixel.
7. **A hero image is half the screen.** If it is a column beside the text, it
   is not a hero.
8. **Intentional over random.** If a choice cannot be explained, it is wrong.

## What this fixed on 4 November

- `section>*{max-width:100%}` was cancelling the 68ch measure for every
  paragraph sitting directly in a section. About ran 1152px lines. Rule 4.
- Two plain sections in a row stacked 96px of padding each way, so a paragraph
  and the next heading sat ~190px apart. Rule 5.
- About was three bare text blocks and one picture. Now three alternating
  bands. Rules 1, 2.
- Strategy's hero picture was capped at 340px beside the text. Now half the
  screen. Rule 7.
- Contact ran from the form's bottom edge into the boat video with nothing
  between. Now "What happens next" sits there. Rule 6.

## Still to do, from the same note

- **Languages**: blocks not aligned, too long, badly structured. Victoria wants
  each language on its own subpage. Not started.
- **Portfolio**: scroll-based UX/UI animation for one project, with this site
  as the showcase. Not started.
- **Web Design**: project types as clickable blocks that open into detail,
  simple shop / one-page service business / artist spotlight / multi-page
  luxury / multi-page personal / hospitality booking. Not started.

## Reviews

Shown as text, never as an embedded widget. A Google review carries the
reviewer's name as Google shows it, a "Google review" label, and a link to the
profile. The quote stays in the language it was written in, with the
translation behind a toggle, because the words belong to the person who wrote
them. No widget and no Maps iframe: both load third-party scripts, would make
the privacy page untrue and would force a consent banner onto a site that
needs none.
