"""Build the Ideas and Library pages from the Markdown in src/.

Run from the repo root:  python3 src/build.py
Needs pandoc. Each src/<section>/<slug>.md becomes <section>/<slug>.html,
and each section gets an index.html listing its pages.
"""
import html
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

SECTIONS = {
    "ideas": {
        "title": "Ideas",
        "kicker": "The notebook",
        "intro": [
            "Ideas I'm thinking through, dated, with where each one came from and what I'd test.",
            "Some get tested. Some just turn into an email. Either way, they don't get lost.",
        ],
    },
    "library": {
        "title": "Library",
        "kicker": "The core tools",
        "intro": [
            "The documents I go back to again and again.",
        ],
    },
}

# Card copy for library pages, which carry no front matter of their own.
LIBRARY_META = {
    "sales-letter-template": {
        "order": 1,
        "title": "My Sales Letter Template",
        "desc": "The baseline skeleton for direct response sales copy, start to finish.",
    },
    "unstoppable-duplication": {
        "order": 2,
        "title": "How To Create Unstoppable Duplication",
        "desc": "The sales video script where Story Selling was first used on purpose.",
    },
}

CSS = """
:root{--bg:#FFFFFF;--ink:#111111;--soft:#555555;--rule:#DDDDDD}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#141414;--ink:#EDEBE5;--soft:#B4B2A9;--rule:#343330}}
:root[data-theme="dark"]{--bg:#141414;--ink:#EDEBE5;--soft:#B4B2A9;--rule:#343330}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,Geneva,Verdana,sans-serif;font-size:19px;line-height:1.6}
.wrap{max-width:620px;margin:0 auto;padding:40px 20px 80px}
.crumb{font-size:15px;font-weight:bold;margin:0 0 30px}
.crumb a{color:var(--ink);text-decoration:none;border-bottom:2px solid var(--ink)}
.kicker{font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:var(--soft);margin:0 0 10px}
h1{font-size:40px;font-weight:900;letter-spacing:-0.5px;line-height:1.15;margin:0 0 24px;text-wrap:balance}
h2{font-size:26px;font-weight:bold;line-height:1.25;margin:44px 0 16px;padding-top:30px;border-top:1px solid var(--rule)}
h3{font-size:20px;font-weight:bold;margin:30px 0 10px}
p{margin:0 0 18px}
ul,ol{margin:0 0 20px;padding-left:22px} li{margin-bottom:8px}
a{color:var(--ink)}
hr{border:none;border-top:1px solid var(--rule);margin:30px 0}
hr+h2{border-top:none;padding-top:0;margin-top:0}
em{color:var(--soft)}
.cards{display:grid;gap:12px;margin:24px 0 0}
.card{display:grid;gap:4px;padding:16px 18px;border:2px solid var(--ink);color:var(--ink);text-decoration:none}
.card:hover,.card:focus-visible{background:var(--ink);color:var(--bg);outline:none}
.card:hover .cd,.card:hover .cc,.card:focus-visible .cd,.card:focus-visible .cc{color:var(--bg)}
.ct{font-size:20px;font-weight:bold;line-height:1.3}
.cd{font-size:16px;line-height:1.5;color:var(--soft)}
.cc{font-size:13px;font-weight:bold;letter-spacing:.5px;text-transform:uppercase;color:var(--soft);margin-top:4px}
.foot{margin-top:60px;font-size:14px;color:var(--soft);border-top:1px solid var(--rule);padding-top:16px}
"""


def page(title, body, crumbs):
    crumb_html = " &nbsp;/&nbsp; ".join(
        f'<a href="{href}">{html.escape(label)}</a>' for label, href in crumbs
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(title)} | Daegan Smith</title>
<style>{CSS}</style>
</head><body><div class="wrap">
<p class="crumb">{crumb_html}</p>
{body}
<p class="foot">Daegan Smith &middot; <a href="/">daegansmith.me</a></p>
</div></body></html>
"""


def front_matter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return {}, text
    meta = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[m.end():]


def to_html(md):
    return subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html", "--wrap=none"],
        input=md, capture_output=True, text=True, check=True,
    ).stdout


def build_section(name, cfg):
    out_dir = ROOT / name
    out_dir.mkdir(exist_ok=True)
    entries = []
    for src in sorted((SRC / name).glob("*.md")):
        slug = src.stem
        meta, body_md = front_matter(src.read_text())
        if name == "library":
            meta = {**LIBRARY_META.get(slug, {}), **meta}
        title = meta.get("title") or slug.replace("-", " ").title()
        body = to_html(body_md)
        crumbs = [("Home", "/"), (cfg["title"], f"/{name}/")]
        (out_dir / f"{slug}.html").write_text(page(title, body, crumbs))
        entries.append((slug, title, meta))

    if name == "ideas":
        entries.sort(key=lambda e: e[2].get("date", ""), reverse=True)
    else:
        entries.sort(key=lambda e: e[2].get("order", 99))

    cards = []
    for slug, title, meta in entries:
        if name == "ideas":
            sub = " &middot; ".join(
                x for x in [meta.get("date", ""), meta.get("status", "")] if x
            )
            cards.append(
                f'<a class="card" href="{slug}.html"><span class="ct">{html.escape(title)}</span>'
                f'<span class="cc">{sub}</span></a>'
            )
        else:
            cards.append(
                f'<a class="card" href="{slug}.html"><span class="ct">{html.escape(title)}</span>'
                f'<span class="cd">{html.escape(meta.get("desc", ""))}</span></a>'
            )
    intro = "".join(f"<p>{html.escape(p)}</p>" for p in cfg["intro"])
    body = (
        f'<p class="kicker">{cfg["kicker"]}</p><h1>{cfg["title"]}</h1>{intro}'
        f'<div class="cards">{"".join(cards)}</div>'
    )
    (out_dir / "index.html").write_text(page(cfg["title"], body, [("Home", "/")]))
    return len(entries)


def build_quotes():
    """quotes/index.html lists every quote; quotes/daily.json feeds the home page."""
    import json

    quotes = json.loads((SRC / "quotes.json").read_text())
    out_dir = ROOT / "quotes"
    out_dir.mkdir(exist_ok=True)

    items = []
    for q in quotes:
        if q.get("list"):
            lines = "".join(f"<li>{html.escape(l)}</li>" for l in q["text"].split("\n"))
            text = f"<ol>{lines}</ol>"
        else:
            text = f"<p>{html.escape(q['text'])}</p>"
        by = f'<p class="by">{html.escape(q["by"])}</p>' if q["by"] else ""
        items.append(f'<blockquote class="q">{text}{by}</blockquote>')

    body = (
        '<p class="kicker">The master list</p><h1>Quotes</h1>'
        + "".join(items)
    )
    extra_css = (
        "<style>.q{margin:0;padding:22px 0;border-top:1px solid var(--rule)}"
        ".q p{margin:0 0 8px}.q .by{font-size:15px;font-weight:bold;color:var(--soft)}"
        ".q .by::before{content:'\\2014\\00a0'}</style>"
    )
    (out_dir / "index.html").write_text(
        page("Quotes", body, [("Home", "/")]).replace("</head>", extra_css + "</head>")
    )

    # The home page shows one a day: short, attributed, and fit for a front page.
    daily = [
        {"text": q["text"], "by": q["by"]}
        for q in quotes
        if q["by"] and not q.get("list") and len(q["text"].split()) <= 30
        and "fuck" not in q["text"].lower()
    ]
    (out_dir / "daily.json").write_text(json.dumps(daily, ensure_ascii=False))
    return len(quotes), len(daily)


if __name__ == "__main__":
    for name, cfg in SECTIONS.items():
        print(name, build_section(name, cfg), "pages")
    print("quotes", *build_quotes())
