# Brand direction — decisions and open questions

Source: the rebrand brief (European Correspondent / Modern Diplomat).
This records what is settled in code and what is deliberately still open.

## Settled, in code

| Item | Value | Where |
|---|---|---|
| Ink black | `#0A0A0B` (`--black`) | page default |
| Ivory | `#F4EFE7` (`--bone`) | text on dark, light bands |
| Oxblood | `#5E1726` (`--oxblood`) | badges, quote rules |
| Rust | `#C87A52` (`--rust`), `#8A4120` on light | eyebrows, numerals, links |
| Headings | Cormorant Garamond, self-hosted | no external font request |
| Body | Inter, self-hosted | — |
| Wordmark | "Victoria Clara Swart", live HTML text | nav, footer |

Green is gone from the build, including the mobile `theme-color`.
Gold was never in the brief and has been removed.

## Deliberately open

- **Logo.** The brief names the horizontal signature as the preferred
  candidate. That is what the site already uses, as selectable text, so no
  mark is hard-coded anywhere. A key, monogram or seal can be added later as
  a secondary mark without touching layout.
- **Wax seal.** If one is produced: name or initials only. No "Europe".
- **Playfair Display.** The mockups pair it with Cormorant. Two display
  serifs is one too many for a site this size; adding it costs a font file
  on every page. Worth doing only if the wordmark itself becomes Playfair.
- **Hero video.** The existing photograph stays until real footage exists.
  Hero markup takes an image today; swapping in `<video>` with that image as
  the poster is a contained change.
- **Doorway / curtain / correspondence footage.** Produce and review
  outside the codebase first. No placeholder animations have been written to
  approximate them.

## Motion

Scroll reveal only, visible-by-default with a JS opt-in and a 2.5s failsafe,
so a script failure can never blank a page. `prefers-reduced-motion` is
honoured. No scroll-jacking, no intro sequence, no autoplay audio.
