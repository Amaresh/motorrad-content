# Tyming Chain

Tyming Chain is bike garage management software for Indian two-wheeler workshops. This public repository is the GitHub Pages source for [tymingchain.com](https://tymingchain.com/).

## Product

Tyming Chain runs bookings, job cards, repair bays, parts inventory, GST invoices, and WhatsApp follow-up on one job card record. It is workshop software — not an engine-part brand.

## Local SEO check

```bash
python3 scripts/check-seo.py
```

GitHub Actions is disabled on this repository, so that command is the gate. `.github/workflows/check-seo.yml` is dormant unless Actions is turned back on.

## After a production merge (human)

1. Google Search Console: DNS TXT verify the apex domain if needed, submit `https://tymingchain.com/sitemap.xml`, then URL Inspection → request indexing for new `/features/`, `/guides/`, `/faq/`, and `/compare/` URLs.
2. Bing Webmaster Tools: import the Search Console property and submit the same sitemap (ChatGPT/Copilot/DuckDuckGo draw from Bing).
3. Confirm `http://tymingchain.com/` 301s to `https://` and `https://www.tymingchain.com/` 301s to the apex.
4. Validate JSON-LD at https://validator.schema.org/ on home, one feature, FAQ, and one blog post. FAQPage will not appear in Google’s Rich Results Test — that restriction is expected (FAQ rich results are limited to government/health sites).

## Content pipeline (authors)

Drafts, research, reddit scouts, and social packs live under `content/` and are disallowed in `robots.txt`. Do not publish those files as product pages.

## Club legal

Play Store legal pages for Motorrad Club stay under `/club/` for in-app links. They are `noindex` and are not in the sitemap.
