# What is left for you to do

Everything in this list needs an account, a password or a decision that is
yours. Nothing here can be done from the code.

---

## 1. Before the site goes live

**Force-push the attribution scrub.** Still pending from earlier. The history
is already cleaned locally in both repositories; the push was blocked and has
to come from you:

```bash
cd ~/victoria-banco.github.io && git push --force-with-lease origin main
```

```bash
cd ~/ldv && git push --force-with-lease origin main
```

**Decide how the site publishes.** The rebuild lives on the branch
`rebuild-2026` and has never been pushed. Two options:

- *Commit the built `_site` folder.* Simplest, works with GitHub Pages as it is
  set up today. The downside is that every change produces a large diff.
- *Build with a GitHub Action.* Cleaner history, one-time setup, and the
  published site can never drift from the source.

Either way, `CNAME` is now generated into the build, so the domain keeps
working. Without it the domain would have stopped resolving on the first
deploy.

---

## 2. Search engines

**Google Search Console** — https://search.google.com/search-console

1. Add `victoriaswart.com` as a *domain* property, not a URL prefix.
2. Verify with the DNS TXT record IONOS asks for.
3. Submit `https://victoriaswart.com/sitemap.xml`.
4. Under Settings, check the international targeting report once the four
   languages have been crawled, to confirm the hreflang tags are reciprocal.

**Bing Webmaster Tools** — https://www.bing.com/webmasters
Import directly from Search Console, which takes about a minute. Worth doing:
Bing feeds ChatGPT's web results.

**Google Business Profile** — https://business.google.com
You sell local services in Rome and you have real reviews. A profile is the
single highest-return item on this list. Add the website, the service areas and
the languages you work in.

---

## 3. Analytics

The site currently has none, which is why it needs no cookie banner.

If you want numbers, use something cookieless and server-side. **Plausible**
(paid, EU-hosted), **Umami** (free if self-hosted) or **Cloudflare Web
Analytics** (free) all work without consent under the GDPR because they set no
cookie and store no personal data.

Avoid Google Analytics. It requires a consent banner, and a banner on a site
this quiet costs more in feel than the data is worth.

Whichever you pick, tell me and I will add it to the Content-Security-Policy.
Without that the script will be blocked, by design.

---

## 4. GDPR, and what changes when the freebie launches

**Today the site is clean.** No cookies, no analytics, no third-party requests,
fonts served from your own server, a consent checkbox on the contact form, and
an Impressum with your Italian P.IVA and no German address.

**The lead magnet changes that.** Collecting an email in order to send a PDF is
fine on legitimate interest. Emailing those people afterwards is marketing, and
that needs its own permission:

- A **second checkbox**, unticked by default, with its own wording. It cannot
  be bundled with the download. "Send me the PDF" and "send me occasional
  emails" are two different consents.
- **Record** the date, time and wording each person agreed to. Most email tools
  do this; check that yours does.
- A **processor agreement** with whatever sends the emails. Mailchimp, Brevo,
  ConvertKit all publish one. If the provider is outside the EU you also need
  the standard contractual clauses, which they will have.
- **Unsubscribe link** in every email, working, one click.
- Update the privacy page to name the provider and say how long you keep the
  address.
- **Do not ask for a phone number.** It roughly halves downloads and you do not
  have a lawful basis to call people who only wanted a PDF.

Germans do check this. The first question a German lawyer asks is whether the
two consents were separate.

---

## 5. Security, and the one thing GitHub Pages cannot do

Content-Security-Policy and Referrer-Policy are set in the pages themselves.
Two protections can only be sent as real HTTP headers, which GitHub Pages does
not allow: `X-Frame-Options` (stops another site putting yours in an invisible
frame) and `X-Content-Type-Options`.

If that matters to you, moving the site behind **Cloudflare** (free) or hosting
on **Netlify** (free) solves it in about ten minutes and changes nothing else.
Not urgent for a brochure site with no login.

---

## 6. Content I am still waiting on

- **Case study screenshots.** All six currently share one placeholder image.
- **The six sample lesson PDFs.** The section is built and hidden behind a
  flag; it appears the moment the files exist.
- **The MC video** from the Inception Roadshow. You said you would tell me
  where it goes.
- **Leana's surname**, if she is happy to give it. A full name and title makes
  a testimonial measurably more credible.
- **A quote from your own writing** to replace the one I wrote. Point me at a
  Substack essay and I will pull candidates.

---

## 7. Decisions still open in the code

These are flags set to `false` in `src/_data/flags.json`. Each one turns on a
piece of content that is already written:

| Flag | What it reveals |
|---|---|
| `case_eqm_named` | Names EQM Sellier instead of "Italian artisan saddlery" |
| `case_graziano_named` | Names Graziano Tumbarello |
| `web_testimonial_marco` | Marco Manca's quote, once he writes one |
| `seabreeze_own_domain` | Links Seabreeze once it moves to its own domain |
| `lesson_samples` | The sample PDF downloads |
| `show_est_year` | "Est. 2016" in the footer |
| `google_profile_url` | Links your Google Business Profile |
| `street_address` | A street address in the Impressum |

For the named ones: ask the client first. It costs one message and it is the
difference between a case study and a problem.
