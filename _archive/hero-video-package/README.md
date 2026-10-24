# Hero video package for victoriaswart.com

| File | Used for |
|---|---|
| hero-desktop.webm / .mp4 | 16:9 cut, any hero box wider than tall (laptops, big screens, tablets landscape) |
| hero-mobile.webm / .mp4 | 9:16 reframed cut, very tall boxes (phones) |
| hero-panel.webm / .mp4 | 4:5 reframed cut, near-square or portrait boxes (the split-layout image panel, tablets portrait) |
| hero-poster-desktop / -panel / -mobile (.webp + .jpg) | First paint and fallback: the portrait |
| hero-demo.html | Working reference implementation (open via a local server) |

Behaviour
- Portrait shows instantly; video fades in over it once it actually plays.
- Cut is chosen by the shape of the video box (ratio < 0.68 → 9:16, up to 1.25 → 4:5, wider → 16:9) and re-chosen on resize / rotation.
- No video with prefers-reduced-motion or Save-Data; portrait stays.
- If autoplay is blocked (iOS Low Power Mode) or the file fails, the portrait stays.
- Video pauses when scrolled out of view or the tab is hidden.
- Muted, looping, playsinline (required for iPhone autoplay). WebM first (smaller), MP4 for Safari.

To integrate: copy the `.hero` markup, CSS and script from hero-demo.html into the site, keep the file names, and replace the headline text.
