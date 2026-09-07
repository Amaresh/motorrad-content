#!/usr/bin/env python3
"""Working-tree SEO assertions for tymingchain.com static pages."""
from __future__ import annotations

import html as htmlmod
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://tymingchain.com"
SCRIPT_RE = re.compile(
    r'<script[^>]*type=["\']application/ld\+json["\'][^>]*>(.*?)</script>',
    re.I | re.S,
)
AI_BOTS = (
    "GPTBot",
    "ClaudeBot",
    "anthropic-ai",
    "PerplexityBot",
    "Google-Extended",
    "CCBot",
)

REQUIRED_FILES = [
    "robots.txt",
    "sitemap.xml",
    "llms.txt",
    "assets/favicon.svg",
    "assets/og-default.jpg",
    "features/index.html",
    "features/job-cards/index.html",
    "features/bay-scheduling/index.html",
    "features/inventory/index.html",
    "features/gst-billing/index.html",
    "features/whatsapp-reminders/index.html",
    "guides/index.html",
    "compare/index.html",
    "faq/index.html",
    "guides/stop-overbooking-repair-bays/index.html",
    "guides/gst-invoices-for-bike-workshops/index.html",
    ".github/workflows/check-seo.yml",
]

TITLES = {
    "index.html": "Tyming Chain | Bike Garage Management Software for India",
    "products/index.html": "Bike Garage Software Modules | Tyming Chain",
    "features/index.html": "Bike Garage Software Features | Tyming Chain",
    "features/job-cards/index.html": "Job Cards for Bike Garages | Tyming Chain",
    "features/bay-scheduling/index.html": "Repair Bay Scheduling for Bike Workshops | Tyming Chain",
    "features/inventory/index.html": "Garage Inventory Management for Bike Workshops | Tyming Chain",
    "features/gst-billing/index.html": "GST Invoicing for Bike Garages | Tyming Chain",
    "features/whatsapp-reminders/index.html": (
        "WhatsApp Service Reminders and Billing for Bike Garages | Tyming Chain"
    ),
    "compare/index.html": (
        "Paper vs Excel vs Auto ERP vs Tyming Chain: Bike Garage Software Compared"
    ),
    "faq/index.html": "Tyming Chain FAQ | GST, WhatsApp, Job Cards, Bays",
    "guides/index.html": "Bike Garage Software Guides | Tyming Chain",
    "guides/stop-overbooking-repair-bays/index.html": (
        "How to Stop Overbooking Repair Bays | Tyming Chain"
    ),
    "guides/gst-invoices-for-bike-workshops/index.html": (
        "How to Raise a GST Invoice for Bike Service: Labour + Parts | Tyming Chain"
    ),
    "about/index.html": "About Tyming Chain | Bike Garage Management Software",
    "contact/index.html": "Contact Tyming Chain | Bike Garage Software Setup",
}

SITEMAP_PATHS = [
    "/",
    "/products/",
    "/features/",
    "/features/job-cards/",
    "/features/bay-scheduling/",
    "/features/inventory/",
    "/features/gst-billing/",
    "/features/whatsapp-reminders/",
    "/compare/",
    "/faq/",
    "/guides/",
    "/guides/stop-overbooking-repair-bays/",
    "/guides/gst-invoices-for-bike-workshops/",
    "/about/",
    "/contact/",
    "/blog/",
    "/blog/ev-readiness-indian-garages-2026/",
    "/blog/why-garage-needs-crm/",
    "/blog/smart-tech-inmrc-racing/",
    "/blog/best-motorcycle-tire-brands-2026/",
    "/blog/agno-mission-control-sdk/",
    "/blog/250cc-vs-600cc-2026/",
]

CLUB_HTML = [
    "club/index.html",
    "club/privacy/index.html",
    "club/terms/index.html",
    "club/subscriptions/index.html",
    "club/delete-account/index.html",
]

MARKETING_HTML = [
    "index.html",
    "products/index.html",
    "about/index.html",
    "contact/index.html",
    "blog/index.html",
    "blog/ev-readiness-indian-garages-2026/index.html",
    "blog/why-garage-needs-crm/index.html",
    "blog/smart-tech-inmrc-racing/index.html",
    "blog/best-motorcycle-tire-brands-2026/index.html",
    "blog/agno-mission-control-sdk/index.html",
    "blog/250cc-vs-600cc-2026/index.html",
    "features/index.html",
    "features/job-cards/index.html",
    "features/bay-scheduling/index.html",
    "features/inventory/index.html",
    "features/gst-billing/index.html",
    "features/whatsapp-reminders/index.html",
    "compare/index.html",
    "faq/index.html",
    "guides/index.html",
    "guides/stop-overbooking-repair-bays/index.html",
    "guides/gst-invoices-for-bike-workshops/index.html",
]

FEATURE_PAGES = [
    "features/job-cards/index.html",
    "features/bay-scheduling/index.html",
    "features/inventory/index.html",
    "features/gst-billing/index.html",
    "features/whatsapp-reminders/index.html",
]

GUIDE_PAGES = [
    "guides/stop-overbooking-repair-bays/index.html",
    "guides/gst-invoices-for-bike-workshops/index.html",
]

NAV_SECTION_HREFS = (
    "/features/",
    "/compare/",
    "/faq/",
    "/guides/",
    "/blog/",
    "/contact/",
)
NAV_FEATURE_HREFS = (
    "/features/job-cards/",
    "/features/bay-scheduling/",
    "/features/inventory/",
    "/features/gst-billing/",
    "/features/whatsapp-reminders/",
)
PRIMARY_FORBIDDEN_HREFS = ("/", "/products/", "/about/")
FOOTER_COL_LABELS = ("Product", "Learn", "Company")
FOOTER_REQUIRED_HREFS = (
    "/products/",
    "/features/",
    *NAV_FEATURE_HREFS,
    "/compare/",
    "/faq/",
    "/guides/",
    "/blog/",
    "/about/",
    "/contact/",
)
ACTIVE_PRIMARY_BY_PAGE = {
    "index.html": None,
    "products/index.html": None,
    "about/index.html": None,
    "contact/index.html": "/contact/",
    "blog/index.html": "/blog/",
    "blog/ev-readiness-indian-garages-2026/index.html": "/blog/",
    "blog/why-garage-needs-crm/index.html": "/blog/",
    "blog/smart-tech-inmrc-racing/index.html": "/blog/",
    "blog/best-motorcycle-tire-brands-2026/index.html": "/blog/",
    "blog/agno-mission-control-sdk/index.html": "/blog/",
    "blog/250cc-vs-600cc-2026/index.html": "/blog/",
    "features/index.html": "/features/",
    "features/job-cards/index.html": "/features/",
    "features/bay-scheduling/index.html": "/features/",
    "features/inventory/index.html": "/features/",
    "features/gst-billing/index.html": "/features/",
    "features/whatsapp-reminders/index.html": "/features/",
    "compare/index.html": "/compare/",
    "faq/index.html": "/faq/",
    "guides/index.html": "/guides/",
    "guides/stop-overbooking-repair-bays/index.html": "/guides/",
    "guides/gst-invoices-for-bike-workshops/index.html": "/guides/",
}
ACTIVE_STRIP_BY_PAGE = {
    "features/job-cards/index.html": "/features/job-cards/",
    "features/bay-scheduling/index.html": "/features/bay-scheduling/",
    "features/inventory/index.html": "/features/inventory/",
    "features/gst-billing/index.html": "/features/gst-billing/",
    "features/whatsapp-reminders/index.html": "/features/whatsapp-reminders/",
}

WEBPAGE_PAGES = [
    "products/index.html",
    "about/index.html",
    "contact/index.html",
    "blog/index.html",
    "features/index.html",
    "guides/index.html",
    "compare/index.html",
    *FEATURE_PAGES,
    *GUIDE_PAGES,
]

BLOG_POSTS = [
    "blog/ev-readiness-indian-garages-2026/index.html",
    "blog/why-garage-needs-crm/index.html",
    "blog/smart-tech-inmrc-racing/index.html",
    "blog/best-motorcycle-tire-brands-2026/index.html",
    "blog/agno-mission-control-sdk/index.html",
    "blog/250cc-vs-600cc-2026/index.html",
]


def fail(msg: str) -> None:
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def title_of(html: str) -> str:
    match = re.search(r"<title>(.*?)</title>", html, re.I | re.S)
    if not match:
        fail("missing <title>")
    return re.sub(r"\s+", " ", htmlmod.unescape(match.group(1))).strip()


def meta_content(html: str, name: str) -> str:
    match = re.search(
        rf'<meta\s+name=["\']{re.escape(name)}["\']\s+content=["\'](.*?)["\']',
        html,
        re.I | re.S,
    )
    if not match:
        match = re.search(
            rf'<meta\s+content=["\'](.*?)["\']\s+name=["\']{re.escape(name)}["\']',
            html,
            re.I | re.S,
        )
    if not match:
        return ""
    return htmlmod.unescape(match.group(1)).strip()


def prop_content(html: str, prop: str) -> str:
    match = re.search(
        rf'<meta\s+property=["\']{re.escape(prop)}["\']\s+content=["\'](.*?)["\']',
        html,
        re.I | re.S,
    )
    if not match:
        match = re.search(
            rf'<meta\s+content=["\'](.*?)["\']\s+property=["\']{re.escape(prop)}["\']',
            html,
            re.I | re.S,
        )
    if not match:
        return ""
    return htmlmod.unescape(match.group(1)).strip()


def canonical_of(html: str) -> str:
    match = re.search(
        r'<link[^>]*rel=["\']canonical["\'][^>]*href=["\'](.*?)["\']',
        html,
        re.I | re.S,
    )
    if not match:
        match = re.search(
            r'<link[^>]*href=["\'](.*?)["\'][^>]*rel=["\']canonical["\']',
            html,
            re.I | re.S,
        )
    if not match:
        return ""
    return match.group(1).strip()


def url_for(rel: str) -> str:
    rel = rel.replace("\\", "/")
    if rel == "index.html":
        return f"{ORIGIN}/"
    if rel.endswith("/index.html"):
        return f"{ORIGIN}/{rel[: -len('index.html')]}"
    return f"{ORIGIN}/{rel}"


def types_in(obj: object) -> set[str]:
    found: set[str] = set()
    if isinstance(obj, dict):
        typed = obj.get("@type")
        if isinstance(typed, str):
            found.add(typed)
        elif isinstance(typed, list):
            found.update(str(item) for item in typed)
        for value in obj.values():
            found |= types_in(value)
    elif isinstance(obj, list):
        for item in obj:
            found |= types_in(item)
    return found


def parse_ld(html: str, rel: str) -> list[object]:
    blocks = SCRIPT_RE.findall(html)
    if not blocks:
        fail(f"{rel} missing JSON-LD")
    parsed: list[object] = []
    for block in blocks:
        try:
            parsed.append(json.loads(block))
        except json.JSONDecodeError as exc:
            fail(f"{rel} JSON-LD is not valid JSON: {exc}")
    return parsed


def require_types(rel: str, parsed: list[object], needed: set[str]) -> None:
    have: set[str] = set()
    for obj in parsed:
        have |= types_in(obj)
    missing = needed - have
    if missing:
        fail(f"{rel} JSON-LD missing types {sorted(missing)}")


def main_inner(html: str) -> str:
    match = re.search(r"<main\b[^>]*>(.*?)</main>", html, re.I | re.S)
    if not match:
        fail("missing <main>")
    return match.group(1)


def visible_text(markup: str) -> str:
    text = re.sub(r"<script\b[^>]*>.*?</script>", " ", markup, flags=re.I | re.S)
    text = re.sub(r"<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    return htmlmod.unescape(text)


def word_count(html: str) -> int:
    return len(re.findall(r"\S+", visible_text(main_inner(html))))


def h1s(html: str) -> list[str]:
    return [
        re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", htmlmod.unescape(chunk))).strip()
        for chunk in re.findall(r"<h1\b[^>]*>(.*?)</h1>", html, re.I | re.S)
    ]


def check_robots(robots: str) -> None:
    if "Sitemap: https://tymingchain.com/sitemap.xml" not in robots:
        fail("robots.txt must point at apex sitemap")
    if "Disallow: /content/" not in robots:
        fail("robots.txt must Disallow: /content/")
    if re.search(r"(?m)^Disallow:\s*/\s*$", robots):
        fail("robots.txt must not disallow the whole site")
    if re.search(r"(?im)^Disallow:\s*/club", robots):
        fail("robots.txt must not Disallow /club (crawlers need noindex)")
    lowered = robots.lower()
    for bot in AI_BOTS:
        pattern = re.compile(
            rf"user-agent:\s*{re.escape(bot)}\b(.*?)(?=user-agent:|\Z)",
            re.I | re.S,
        )
        match = pattern.search(robots)
        if match and re.search(r"Disallow:", match.group(1)):
            fail(f"robots.txt must not Disallow {bot}")
    if "google-extended" in lowered and "disallow" in lowered:
        # covered per-block above; keep a belt-and-braces skip
        pass


def check_internal_hrefs(rel: str, html: str) -> None:
    if 'href="#"' in html or "href='#'" in html:
        fail(f"{rel} contains href=#")
    for href in re.findall(r'href=["\']([^"\']+)["\']', html):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
            continue
        path = href.split("#")[0].split("?")[0]
        if not path.startswith("/"):
            continue
        if path == "/":
            target = ROOT / "index.html"
        elif path.endswith("/"):
            target = ROOT / path.strip("/") / "index.html"
        else:
            target = ROOT / path.lstrip("/")
            if target.is_dir():
                target = target / "index.html"
        if not target.is_file():
            fail(f"{rel} internal href {href} does not resolve ({target})")


def site_nav(html: str) -> str:
    match = re.search(r'<nav class="site-nav">(.*?)</nav>', html, re.I | re.S)
    if not match:
        fail("missing nav.site-nav")
    return match.group(1)


def site_footer(html: str) -> str:
    match = re.search(r'<footer class="site-footer">(.*?)</footer>', html, re.I | re.S)
    if not match:
        fail("missing footer.site-footer")
    return match.group(1)


def region(markup: str, cls: str) -> str:
    match = re.search(
        rf'<(?:div|nav)[^>]*class=["\'][^"\']*\b{re.escape(cls)}\b[^"\']*["\'][^>]*>(.*?)</(?:div|nav)>',
        markup,
        re.I | re.S,
    )
    if not match:
        fail(f"missing .{cls}")
    return match.group(1)


def hrefs_in(markup: str) -> set[str]:
    return set(re.findall(r'href=["\']([^"\']+)["\']', markup))


def current_hrefs(markup: str) -> set[str]:
    found: set[str] = set()
    for tag in re.findall(r"<a\b[^>]*>", markup, re.I):
        if re.search(r'\bactive\b', tag) or re.search(r'aria-current=["\']page["\']', tag, re.I):
            href = re.search(r'href=["\']([^"\']+)["\']', tag)
            if href:
                found.add(href.group(1))
    return found


def check_chrome(rel: str, html: str) -> None:
    if set(ACTIVE_PRIMARY_BY_PAGE) != set(MARKETING_HTML):
        fail("ACTIVE_PRIMARY_BY_PAGE must list every MARKETING_HTML path")
    nav = site_nav(html)
    footer = site_footer(html)
    links = region(nav, "nav-links")
    strip = region(nav, "nav-features")
    nav_hrefs = hrefs_in(nav)
    for href in NAV_SECTION_HREFS + NAV_FEATURE_HREFS:
        if href not in nav_hrefs:
            fail(f"{rel} site-nav missing {href}")
    for href in PRIMARY_FORBIDDEN_HREFS:
        if href in hrefs_in(links) or href in hrefs_in(strip):
            fail(f"{rel} header chrome must not include {href}")
    if "footer-inner footer-features" in footer or "footer-features" in footer:
        fail(f"{rel} must not use footer-features")
    if "footer-col" not in footer:
        fail(f"{rel} footer missing footer-col")
    foot_hrefs = hrefs_in(footer)
    for href in FOOTER_REQUIRED_HREFS:
        if href not in foot_hrefs:
            fail(f"{rel} footer missing {href}")
    for label in FOOTER_COL_LABELS:
        if f'aria-label="{label}"' not in footer:
            fail(f"{rel} footer missing column {label}")
    expected_primary = ACTIVE_PRIMARY_BY_PAGE[rel]
    expected_strip = ACTIVE_STRIP_BY_PAGE.get(rel)
    primary_current = current_hrefs(links)
    strip_current = current_hrefs(strip)
    if expected_primary is None:
        if primary_current:
            fail(f"{rel} nav-links should have no active link, got {sorted(primary_current)}")
    elif primary_current != {expected_primary}:
        fail(f"{rel} nav-links active {sorted(primary_current)} != {[expected_primary]}")
    if expected_strip is None:
        if strip_current:
            fail(f"{rel} nav-features should have no active link, got {sorted(strip_current)}")
    elif strip_current != {expected_strip}:
        fail(f"{rel} nav-features active {sorted(strip_current)} != {[expected_strip]}")


def faq_answers(html: str) -> list[tuple[str, str]]:
    items = re.findall(
        r'<article class="faq-item[^"]*">(.*?)</article>',
        html,
        re.I | re.S,
    )
    out: list[tuple[str, str]] = []
    for item in items:
        h2 = re.search(r"<h2\b[^>]*>(.*?)</h2>", item, re.I | re.S)
        ans = re.search(
            r'<p class="faq-answer">(.*?)</p>',
            item,
            re.I | re.S,
        )
        if not h2 or not ans:
            fail("faq item missing h2 or p.faq-answer")
        question = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", htmlmod.unescape(h2.group(1)))).strip()
        answer = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", htmlmod.unescape(ans.group(1)))).strip()
        out.append((question, answer))
    return out


def faq_ld_pairs(parsed: list[object]) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []

    def walk(obj: object) -> None:
        if isinstance(obj, dict):
            if obj.get("@type") == "Question" or (
                isinstance(obj.get("@type"), list) and "Question" in obj.get("@type")
            ):
                name = str(obj.get("name", "")).strip()
                accepted = obj.get("acceptedAnswer") or {}
                text = ""
                if isinstance(accepted, dict):
                    text = str(accepted.get("text", "")).strip()
                pairs.append((name, text))
            for value in obj.values():
                walk(value)
        elif isinstance(obj, list):
            for item in obj:
                walk(item)

    for obj in parsed:
        walk(obj)
    return pairs


def main() -> None:
    for rel in REQUIRED_FILES:
        if not (ROOT / rel).is_file():
            fail(f"missing file {rel}")

    check_robots((ROOT / "robots.txt").read_text(encoding="utf-8"))

    sitemap_text = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    try:
        root_el = ET.fromstring(sitemap_text)
    except ET.ParseError as exc:
        fail(f"sitemap.xml is not valid XML: {exc}")
    ns = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs = {el.text.strip() for el in root_el.findall(".//sm:loc", ns) if el.text}
    if not locs:
        locs = {el.text.strip() for el in root_el.findall(".//{*}loc") if el.text}
    expected = {f"{ORIGIN}{path}" for path in SITEMAP_PATHS}
    if locs != expected:
        fail(
            "sitemap loc set mismatch\n"
            f"missing {sorted(expected - locs)}\n"
            f"extra {sorted(locs - expected)}"
        )
    if any("/club" in loc for loc in locs):
        fail("sitemap must not list /club URLs")

    llms = (ROOT / "llms.txt").read_text(encoding="utf-8").lower()
    if "bike garage management software" not in llms:
        fail("llms.txt must state bike garage management software")
    if "not a manufacturer of engine timing chains" not in llms:
        fail("llms.txt must disambiguate engine timing chains")
    if "/club" in llms:
        fail("llms.txt must not point at /club")

    readme_head = "\n".join(
        (ROOT / "README.md").read_text(encoding="utf-8").splitlines()[:20]
    )
    if re.search(r"Motorrad Theory", readme_head):
        fail("README.md first 20 lines must not name Motorrad Theory as the product")

    home = (ROOT / "index.html").read_text(encoding="utf-8")
    if "Tyming Chain is bike garage management software" not in home:
        fail("homepage body must use the entity sentence")
    home_ld = parse_ld(home, "index.html")
    require_types(
        "index.html",
        home_ld,
        {"Organization", "SoftwareApplication", "WebSite"},
    )
    if "aggregateRating" in home:
        fail("do not ship fake aggregateRating")

    faq_html = (ROOT / "faq/index.html").read_text(encoding="utf-8")
    if "<blockquote" in faq_html.lower():
        fail("faq answers must not use blockquote")
    faq_ld = parse_ld(faq_html, "faq/index.html")
    require_types("faq/index.html", faq_ld, {"FAQPage", "WebPage", "BreadcrumbList"})
    visible = faq_answers(faq_html)
    encoded = faq_ld_pairs(faq_ld)
    if len(visible) != len(encoded):
        fail(f"FAQPage mainEntity count {len(encoded)} != visible h2 count {len(visible)}")
    if visible != encoded:
        fail("FAQPage questions/answers must match visible h2 + p.faq-answer")

    compare = (ROOT / "compare/index.html").read_text(encoding="utf-8")
    if "<table" not in compare.lower():
        fail("compare page needs a real HTML table")
    if "Paper" not in compare or "Excel" not in compare or "Tyming Chain" not in compare:
        fail("compare table must include Paper, Excel, Tyming Chain columns")

    products = (ROOT / "products/index.html").read_text(encoding="utf-8")
    for href in [
        "/features/job-cards/",
        "/features/bay-scheduling/",
        "/features/inventory/",
        "/features/gst-billing/",
        "/features/whatsapp-reminders/",
    ]:
        if href not in products:
            fail(f"products hub must link {href}")

    descriptions: dict[str, str] = {}
    for rel in MARKETING_HTML:
        html = (ROOT / rel).read_text(encoding="utf-8")
        expected_url = url_for(rel)
        if canonical_of(html) != expected_url:
            fail(f"{rel} canonical {canonical_of(html)!r} != {expected_url!r}")
        if prop_content(html, "og:url") != expected_url:
            fail(f"{rel} og:url {prop_content(html, 'og:url')!r} != {expected_url!r}")
        desc = meta_content(html, "description")
        if not desc:
            fail(f"{rel} missing meta description")
        if not (70 <= len(desc) <= 160):
            fail(f"{rel} description length {len(desc)} not in 70–160")
        if desc in descriptions:
            fail(f"{rel} description duplicates {descriptions[desc]}")
        descriptions[desc] = rel
        if "/assets/favicon.svg" not in html:
            fail(f"{rel} missing favicon")
        if "/assets/og-default.jpg" not in html and "og:image" not in html:
            fail(f"{rel} missing og:image")
        if not prop_content(html, "og:image"):
            fail(f"{rel} missing og:image")
        if prop_content(html, "og:locale") != "en_IN":
            fail(f"{rel} og:locale must be en_IN")
        found_h1 = h1s(html)
        if len(found_h1) != 1:
            fail(f"{rel} must have exactly one h1, got {len(found_h1)}")
        title = title_of(html)
        if re.search(r"Motorrad Theory", title) or re.search(
            r"Motorrad Theory", found_h1[0]
        ):
            fail(f"{rel} title/H1 contains Motorrad Theory")
        parsed = parse_ld(html, rel)
        for obj in parsed:
            dumped = json.dumps(obj)
            if "Motorrad Theory" in dumped:
                fail(f"{rel} JSON-LD contains Motorrad Theory")
            if "aggregateRating" in dumped:
                fail(f"{rel} JSON-LD contains aggregateRating")
        check_internal_hrefs(rel, html)
        check_chrome(rel, html)
        for href in hrefs_in(html):
            path = href.split("#")[0].split("?")[0].lower()
            if "/club" in path:
                fail(f"{rel} must not link to /club ({href})")

    for rel, expected in TITLES.items():
        got = title_of((ROOT / rel).read_text(encoding="utf-8"))
        if got != expected:
            fail(f"{rel} title {got!r} != {expected!r}")

    for rel in WEBPAGE_PAGES:
        parsed = parse_ld((ROOT / rel).read_text(encoding="utf-8"), rel)
        require_types(rel, parsed, {"WebPage", "BreadcrumbList"})

    for rel in FEATURE_PAGES:
        if word_count((ROOT / rel).read_text(encoding="utf-8")) < 300:
            fail(f"{rel} <main> must have ≥300 words")
        parsed = parse_ld((ROOT / rel).read_text(encoding="utf-8"), rel)
        require_types(rel, parsed, {"SoftwareApplication"})

    for rel in GUIDE_PAGES:
        html = (ROOT / rel).read_text(encoding="utf-8")
        if word_count(html) < 600:
            fail(f"{rel} <main> must have ≥600 words")
        parsed = parse_ld(html, rel)
        require_types(rel, parsed, {"Article", "WebPage", "BreadcrumbList"})

    for rel in BLOG_POSTS:
        parsed = parse_ld((ROOT / rel).read_text(encoding="utf-8"), rel)
        require_types(rel, parsed, {"Article"})

    notfound = (ROOT / "404.html").read_text(encoding="utf-8")
    if "noindex" not in notfound.lower():
        fail("404.html must be noindex")

    for rel in CLUB_HTML:
        html = (ROOT / rel).read_text(encoding="utf-8")
        if "noindex" not in html.lower():
            fail(f"{rel} must be noindex")

    css = (ROOT / "assets/site.css").read_text(encoding="utf-8")
    if ".article-body a.button-primary" not in css:
        fail("article-body must keep primary button label color (specificity vs .article-body a)")

    print("check-seo: ok")


if __name__ == "__main__":
    main()
