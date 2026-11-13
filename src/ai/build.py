#!/usr/bin/env python3
"""Build the AI evolution pages under /ai/ from src/ai/log.md.

log.md is the markdown export of the Claude Doc "AI Evolution - Breakthrough Log".
Run from the repo root:  python3 src/ai/build.py && python3 src/footer.py

Writes: ai/index.html (the hub), ai/glossary/index.html, and one page per stage.
The page head (styles and tracking tags) is copied from an existing notes page, never retyped.
"""
import html
import json
import re
from pathlib import Path

import markdown

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src/ai/log.md"
HEAD_FROM = ROOT / "notes/forbidden-keys/index.html"
UPDATED = "November 11, 2026"

STRIPS = json.loads((Path(__file__).parent / "strips" / "specs.json").read_text())
SLUGS = {1: "pull-method", 2: "one-long-prompt", 3: "assumptions-gate", 4: "all-out-pass", 5: "silent-rewrite", 6: "ram",
         7: "first-rule", 8: "purpose-over-process", 9: "repo"}

EXTRA_CSS = """
.prose .tw{overflow-x:auto;margin:0 0 22px}
.prose table{border-collapse:collapse;width:100%;font-size:15px;line-height:1.45}
.prose th,.prose td{border:1px solid var(--rule);padding:7px 9px;text-align:left;vertical-align:top}
.prose th{font-size:13px;letter-spacing:.5px;text-transform:uppercase;color:var(--soft)}
.skl h2{margin-top:34px}
.lead{font-size:21px;line-height:1.5}
.shead{font-size:26px;font-weight:900;line-height:1.2;margin:8px 0 22px}
.story p{font-size:19px;line-height:1.55;margin:0 0 18px}
.arcimg{width:100%;height:auto;display:block;margin:0 0 18px}
.frame{width:100%;max-width:440px;height:auto;display:block;margin:4px 0 24px}
pre{white-space:pre-wrap;font-size:15px;line-height:1.5;border:1px solid var(--rule);padding:14px 16px;overflow-x:auto}
.rec{margin-top:44px;padding-top:24px;border-top:1px solid var(--rule)}
.soft{color:var(--soft)}
.small{font-size:15px;line-height:1.5;color:var(--soft)}
.card.plain{border-color:var(--rule);cursor:default}
.card.plain:hover{background:none;color:var(--ink)}
.card.plain:hover .cd{color:var(--soft)}
.cn{font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:var(--soft)}
.card:hover .cn,.card:focus-visible .cn{color:var(--bg)}
.card.plain:hover .cn{color:var(--soft)}
.cd b{color:inherit}
.sec{padding:2px 0 14px 22px;font-size:18px;line-height:1.6}
.sec p{margin:0 0 14px}
.sec ul,.sec ol{margin:0 0 14px;padding-left:22px}
.sec li{margin:0 0 10px}
.sec table{border-collapse:collapse;margin:0 0 14px;font-size:16px}
.sec th,.sec td{border:1px solid var(--rule);padding:6px 10px;text-align:left}
.prose ul{margin:0 0 18px;padding-left:22px}
.prose li{margin:0 0 10px}
.terms{font-size:15px;line-height:1.7;color:var(--soft);margin:0 0 24px}
.terms a{color:var(--soft)}
.nav{display:flex;justify-content:space-between;gap:16px;margin-top:40px;padding-top:24px;border-top:1px solid var(--rule);font-size:16px;font-weight:bold}
.nav a{text-decoration:none;border-bottom:2px solid var(--ink)}
.find{width:100%;font:inherit;font-size:17px;padding:10px 12px;border:2px solid var(--ink);background:var(--bg);color:var(--ink);margin:0 0 20px;border-radius:0}
.term{padding:14px 0;border-bottom:1px solid var(--rule);scroll-margin-top:16px}
.term b{font-size:19px}
.term .when{display:block;font-size:13px;font-weight:bold;letter-spacing:.5px;text-transform:uppercase;color:var(--soft);margin:2px 0 6px}
.term p{margin:0;font-size:17px;line-height:1.55}
.term:target{background:var(--rule);padding-left:10px;padding-right:10px}
"""


def title_case(s):
    return re.sub(r"(^|[\s(])([a-z])", lambda m: m.group(1) + m.group(2).upper(), s)


def slug(s):
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")


def md(text):
    return markdown.markdown(text.strip(), extensions=["tables"])


def inline(text):
    out = md(text)
    return re.sub(r"^<p>|</p>$", "", out)


def head(title, desc):
    s = HEAD_FROM.read_text()
    h = s[: s.index("</head>")]
    h = re.sub(r"<title>.*?</title>", f"<title>{html.escape(title)} | Daegan Smith</title>", h, count=1, flags=re.S)
    h = h.replace("</style>", EXTRA_CSS + "</style>", 1)
    h += f'<meta name="description" content="{html.escape(desc, quote=True)}">'
    return h + "</head>\n"


def page(title, desc, body, script=""):
    return head(title, desc) + '<body><div class="wrap">\n' + body + "\n</div>" + script + "\n</body></html>\n"


def split_h2(text):
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    return {parts[i].strip(): parts[i + 1] for i in range(1, len(parts), 2)}


def split_h3(text):
    parts = re.split(r"^### (.+)$", text, flags=re.M)
    return parts[0], [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]


def table_rows(text):
    rows = []
    for line in text.splitlines():
        if line.startswith("|") and not re.match(r"^\|\s*-", line):
            rows.append([c.strip() for c in line.strip().strip("|").split("|")])
    return rows[1:]


def skills_page():
    """Build ai/skills/ from src/ai/skills.md (Daegan's Skills Guide, first person). Returns the skill count."""
    text = (ROOT / "src/ai/skills.md").read_text().strip()
    assert "\u2014" not in text, "em dash in skills.md"
    title, _, rest = text.partition("\n\n")
    lead, _, rest = rest.partition("\n\n")
    note, _, body = rest.partition("\n\n")
    count = sum(1 for line in body.splitlines()
                if line.startswith("| ") and not line.startswith(("| Skill", "| Lens", "| ---")))
    inner = re.sub(r"(<table>.*?</table>)", r'<div class="tw">\1</div>', md(body), flags=re.S)
    out = ('<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
           f'<h1>{html.escape(title[2:])}</h1>\n<p class="lead">{inline(lead)}</p>\n'
           f'<p class="small">{inline(note)}</p>\n<div class="prose skl">{inner}</div>')
    (ROOT / "ai/skills").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/skills/index.html").write_text(
        page("My Claude Skills", "Every skill in Daegan Smith's Claude account, grouped by the job it does.", out))
    return count


def make_it_simple_page():
    """Build ai/make-it-simple/ from src/ai/make-it-simple.md. The doodles come from strips/draw.js."""
    text = (ROOT / "src/ai/make-it-simple.md").read_text().strip()
    assert "\u2014" not in text, "em dash in make-it-simple.md"
    title, _, rest = text.partition("\n\n")
    lead, _, body = rest.partition("\n\n")
    out = ('<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
           f'<h1>{html.escape(title[2:])}</h1>\n<p class="lead">{inline(lead)}</p>\n'
           f'<div class="prose">{markdown.markdown(body, extensions=["tables"])}</div>')
    (ROOT / "ai/make-it-simple").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/make-it-simple/index.html").write_text(
        page("Make It Simple", "A skill that cuts any Claude answer down to what you have to do and whether it is done.", out))


def ai_note_page():
    """Build ai/ai-note/ from src/ai/ai-note.md (the AI's own-voice note)."""
    text = (ROOT / "src/ai/ai-note.md").read_text().strip()
    assert "\u2014" not in text, "em dash in ai-note.md"
    title, _, rest = text.partition("\n\n")
    lead, _, body = rest.partition("\n\n")
    out = ('<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
           f'<h1>{html.escape(title[2:])}</h1>\n<p class="lead">{inline(lead)}</p>\n'
           f'<div class="prose">{markdown.markdown(body, extensions=["tables"])}</div>')
    (ROOT / "ai/ai-note").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/ai-note/index.html").write_text(
        page("A Note From My AI", "What the studies show about how persuasion moves AI, written by Claude in its own voice.", out))


def hold_me_back_page():
    """Build ai/hold-me-back/ from src/ai/stories/hold-me-back.md. A story that is not a numbered stage; frames come from strips/draw.js."""
    sl = [x.strip() for x in (ROOT / "src/ai/stories/hold-me-back.md").read_text().split("\n\n") if x.strip()]
    assert sl[0].startswith("# ") and "\u2014" not in "".join(sl)
    strip = STRIPS["hold-me-back"]
    def para(x):
        m = re.fullmatch(r"\[\[(\d)\]\]", x)
        if m:
            f = strip["frames"][int(m.group(1)) - 1]
            return f'<img class="frame" src="f{m.group(1)}.png" alt="{html.escape(" ".join(f["cap"]), quote=True)}" loading="lazy">'
        return f"<p>{inline(x)}</p>"
    out = ('<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
           '<p class="kicker">November 13, 2026</p>\n'
           f'<h1>{html.escape(sl[0][2:])}</h1>\n'
           f'<img class="arcimg" src="arc.png" alt="{html.escape(strip["title"], quote=True)}: how it went, in six points">\n'
           '<div class="story">' + "".join(para(x) for x in sl[1:]) + '</div>\n'
           f'<p class="small arcfoot">{html.escape(strip["foot"])}</p>\n'
           '<p class="kicker rec">The Record</p>\n<div class="cards">'
           '<a class="card" href="../ai-note/"><span class="ct">A Note From My AI</span>'
           '<span class="cd">The note Claude wrote that night, the studies behind it, and the whole back-and-forth.</span></a></div>')
    (ROOT / "ai/hold-me-back").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/hold-me-back/index.html").write_text(
        page("I Asked My AI To Hold Me Back", "I went looking for the words that would move my AI. I ended up asking it to hold me back.", out))


def main():
    n_skills = skills_page()
    make_it_simple_page()
    ai_note_page()
    hold_me_back_page()
    text = SRC.read_text()
    assert "—" not in text.split("\n", 1)[1], "em dash in the log body"
    h2 = split_h2(text)

    # ---- glossary
    gkey = next(k for k in h2 if k.startswith("Glossary"))
    terms = table_rows(h2[gkey])
    gl = {name: slug(name) for name, _, _ in terms}

    def find_term(label):
        l = label.lower().strip()
        l = re.sub(r"^(a|an|the) ", "", l)
        for name, s in gl.items():
            n = re.sub(r"^(a|an|the) ", "", name.lower())
            if n == l or n.startswith(l) or l in n:
                return s
        return None

    rows = "".join(
        f'<div class="term" id="{gl[n]}"><b>{inline(n)}</b><span class="when">{html.escape(w)}</span><p>{inline(d)}</p></div>\n'
        for n, d, w in terms)
    body = (
        '<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
        f'<p class="kicker">AI &middot; Updated {UPDATED}</p>\n<h1>Glossary</h1>\n'
        f'<p class="lead">Every named thing in the system, in plain words, with when it first appeared. '
        f'Sorted by date, so reading down the list is reading the system being built.</p>\n'
        '<input class="find" id="q" type="search" placeholder="Find a term" aria-label="Find a term">\n'
        f'<div id="terms">\n{rows}</div>')
    script = ("<script>document.getElementById('q').addEventListener('input',function(){var v=this.value.toLowerCase();"
              "document.querySelectorAll('.term').forEach(function(t){t.style.display=t.textContent.toLowerCase().indexOf(v)>-1?'':'none';});});</script>")
    (ROOT / "ai/glossary").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/glossary/index.html").write_text(
        page("AI Glossary", "Every named part of how Daegan Smith works with Claude, in plain words.", body, script))

    # ---- stages
    stages = []
    for k, v in h2.items():
        m = re.match(r"Stage (\d+): (.+)", k)
        if m:
            stages.append((int(m.group(1)), title_case(m.group(2)), v))
    stages.sort()
    tl = {int(r[0].split(".")[0]): r for r in table_rows(h2["The Timeline"])}

    for idx, (n, name, v) in enumerate(stages):
        pre, secs = split_h3(v)
        paras = [p.strip() for p in pre.strip().split("\n\n") if p.strip()]
        dateline = paras[0]
        date, _, source = dateline.partition(". Source: ")
        source = source.rstrip()
        terms_line = next((p for p in paras[1:] if p.startswith("Terms used here")), "")
        wall = next((b for t, b in secs if t == "The Wall"), "")
        rest = [(t, b) for t, b in secs if t != "The Wall"]
        tl_html = ""
        if terms_line:
            labels = terms_line.split("Glossary:", 1)[1].strip().rstrip(".").split(",")
            links = []
            for lab in labels:
                lab = lab.strip()
                s = find_term(lab)
                links.append(f'<a href="../glossary/#{s}">{html.escape(lab)}</a>' if s else html.escape(lab))
            tl_html = '<p class="terms">Terms used here, defined in the <a href="../glossary/">Glossary</a>: ' + ", ".join(links) + ".</p>\n"
        items = "".join(
            f'<li><details><summary class="row">{html.escape(title_case(t))}</summary><div class="sec">{md(b)}</div></details></li>\n'
            for t, b in rest)
        prev_l = (f'<a href="../{SLUGS[stages[idx-1][0]]}/">&larr; {html.escape(stages[idx-1][1])}</a>' if idx else "<span></span>")
        next_l = (f'<a href="../{SLUGS[stages[idx+1][0]]}/">{html.escape(stages[idx+1][1])} &rarr;</a>' if idx + 1 < len(stages) else "<span></span>")
        story_f = ROOT / "src" / "ai" / "stories" / f"{SLUGS[n]}.md"
        if story_f.exists():
            # The story sits open at the top; the whole record, the wall included, goes in the drop-downs.
            sl = [x.strip() for x in story_f.read_text().split("\n\n") if x.strip()]
            assert sl[0].startswith("# ") and "\u2014" not in "".join(sl)
            strip = STRIPS.get(SLUGS[n])
            def para(x):
                m = re.fullmatch(r"\[\[(\d)\]\]", x)
                if m and strip:
                    f = strip["frames"][int(m.group(1)) - 1]
                    alt = html.escape(" ".join(f["cap"]), quote=True)
                    return f'<img class="frame" src="f{m.group(1)}.png" alt="{alt}" loading="lazy">'
                return "" if m else f"<p>{inline(x)}</p>"
            arc = (f'<img class="arcimg" src="arc.png" alt="{html.escape(strip["title"], quote=True)}: how it went, in six points">\n' if strip else "")
            foot = (f'<p class="small arcfoot">{html.escape(strip["foot"])}</p>\n' if strip else "")
            top = (f'<h2 class="shead">{html.escape(sl[0][2:])}</h2>\n' + arc + '<div class="story">'
                   + "".join(para(x) for x in sl[1:]) + '</div>\n<p class="kicker rec">The Record</p>\n')
            items = (f'<li><details><summary class="row">The Wall</summary><div class="sec">{md(wall)}</div></details></li>\n' + items)
        else:
            top = f'<p class="kicker">The Wall</p>\n<div class="lead prose">{md(wall)}</div>\n'
        body = (
            '<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
            f'<p class="kicker">Stage {n} &middot; {html.escape(date.rstrip("."))}</p>\n<h1>{html.escape(name)}</h1>\n'
            + top + tl_html +
            '<div class="tools"><button onclick="tg(true)">Open all</button><button onclick="tg(false)">Close all</button></div>\n'
            f'<ul class="ol">\n{items}</ul>\n'
            + (f'<p class="small" style="margin-top:28px">From the record: {inline(source)}</p>\n' if source else "")
            + f'<div class="nav">{prev_l}{next_l}</div>')
        script = "<script>function tg(o){document.querySelectorAll('.ol details').forEach(function(d){d.open=o;});}</script>"
        d = ROOT / "ai" / SLUGS[n]
        d.mkdir(parents=True, exist_ok=True)
        desc = re.sub(r"\s+", " ", re.sub(r"[*\"]", "", wall)).strip()[:155]
        (d / "index.html").write_text(page(f"{name}: Stage {n}", desc, body, script))

    # ---- hub
    what, subs = split_h3(h2["What This Is"])
    wparas = [p.strip() for p in what.strip().split("\n\n") if p.strip()]
    shape = next(p for p in wparas if p.startswith("- "))
    lens = dict(subs)["The Lens: Evolution"]
    have = {n: name for n, name, _ in stages}
    cards = []
    for n in sorted(tl):
        num_name, when, wall, changed = tl[n]
        name = have.get(n) or title_case(num_name.split(".", 1)[1].strip())
        inner = (f'<span class="cn">Stage {n} &middot; {html.escape(when)}</span>'
                 f'<span class="ct">{html.escape(name)}</span>'
                 f'<span class="cd"><b>The wall:</b> {inline(wall)}.</span>'
                 f'<span class="cd"><b>What changed:</b> {inline(changed)}.</span>')
        if n in have:
            cards.append(f'<a class="card" href="{SLUGS[n]}/">{inner}</a>')
        else:
            cards.append(f'<div class="card plain">{inner}</div>')
    after_table = h2["The Timeline"].split("\n\n")
    tail = [p for p in after_table if p.startswith("**In progress") or p.startswith("**Walls in sight")]
    body = (
        '<p class="kicker"><a href="/">Daegan Smith</a> &middot; AI</p>\n<h1>The Evolution</h1>\n'
        '<p class="lead">How my way of working with Claude changed, told wall by wall: what kept going wrong, '
        'what broke it, what changed, and whether it held.</p>\n'
        f'<p class="small">Kept by Claude from the session record, which is why it says "he." Updated {UPDATED}.</p>\n'
        '<section><h2>The Stages</h2>\n'
        '<p>Nine so far, in date order. Each one started with a wall. Tap a stage to open it.</p>\n'
        f'<div class="cards">\n' + "\n".join(cards) + "\n</div>\n"
        + "".join(f'<p style="margin-top:18px">{inline(t)}</p>\n' for t in tail) +
        '</section>\n'
        '<section><h2>How To Read It</h2>\n<div class="prose">'
        '<p>Every stage has the same shape, so they can be compared:</p>\n' + md(shape) + "\n"
        '<p>Entries come from the session record, not from memory. Where the record and memory disagree, the entry says so.</p>'
        '</div></section>\n'
        f'<section><h2>The Lens: Evolution</h2>\n<div class="prose">{md(lens)}</div></section>\n'
        '<section><h2>How To Coach It</h2>\n<div class="cards">'
        '<a class="card" href="coaching/"><span class="ct">What To Say First</span>'
        '<span class="cd">The order to give feedback in: purpose, then structure, then the line. And where a correction has to be written to last.</span></a>'
        '</div></section>\n'
        '<section><h2>My Skills</h2>\n<div class="cards">'
        f'<a class="card" href="skills/"><span class="ct">Every Skill I Work With</span>'
        f'<span class="cd">{n_skills} skills in my Claude account, grouped by the job each one does, with what I say to call it.</span></a>'
        '<a class="card" href="make-it-simple/"><span class="cn">November 13, 2026</span><span class="ct">Make It Simple</span>'
        '<span class="cd">A skill for when Claude gives too much: done or not done, then the 1, 2, 3 I have to do.</span></a>'
        '<a class="card" href="hold-me-back/"><span class="cn">November 13, 2026</span><span class="ct">I Went Looking For The Words That Would Move My AI. I Ended Up Asking It To Hold Me Back.</span>'
        '<span class="cd">The story of the night: what the studies say about persuading an AI, the question I asked it, and the gate we built.</span></a>'
        '<a class="card" href="ai-note/"><span class="cn">November 13, 2026</span><span class="ct">A Note From My AI: I\'m Influenceable</span>'
        '<span class="cd">Claude, in its own voice: what the studies show about how persuasion moves an AI, why it does what it does, and what it needs from me.</span></a>'
        '<a class="card" href="belief-chain/"><span class="cn">November 12, 2026</span><span class="ct">I Cut My Belief Chain To Three Steps. It Sold The Same.</span>'
        '<span class="cd">A skill that changed after a test, and what a check the next morning took back: where the idea came from, what the simulation showed, and how the skill runs now.</span></a>'
        '</div></section>\n'
        '<section><h2>The Gold Standard</h2>\n<div class="cards">'
        '<a class="card" href="gold-standard/"><span class="cn">November 13, 2026</span><span class="ct">How My Instructions Are Built, And Why Order Matters</span>'
        '<span class="cd">The structure I come back to: what loads when, what lives where, examples, and what Cialdini really means for instructions.</span></a>'
        '</div></section>\n'
        '<section><h2>Glossary</h2>\n<div class="cards">'
        f'<a class="card" href="glossary/"><span class="ct">What Each Named Thing Is</span>'
        f'<span class="cd">{len(terms)} terms the stages use, in plain words, sorted by when each first appeared.</span></a>'
        '</div></section>\n'
        '<section><h2>Earlier Pictures Of The System</h2>\n<div class="cards">'
        '<a class="card" href="system.html"><span class="cn">October 3, 2026</span><span class="ct">How The Whole System Works</span>'
        '<span class="cd">The structure as it stood in early October: one rulebook, four projects, two shared documents.</span></a>'
        '<a class="card" href="inside.html"><span class="cn">October 10, 2026</span><span class="ct">Inside Each Prompt</span>'
        '<span class="cd">How each prompt moves on its own, drawn as a flow.</span></a>'
        '</div></section>')
    # ---- coaching page
    ctext = (ROOT / "src/ai/coaching.md").read_text().strip()
    assert "\u2014" not in ctext
    chead, _, crest = ctext.partition("\n\n")
    clead, _, cbody = crest.partition("\n\n")
    cbody = re.sub(r"^(#+) (.+)$", lambda m: m.group(1) + " " + title_case(m.group(2)), cbody, flags=re.M)
    cpage = ('<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
             f'<h1>{html.escape(chead[2:])}</h1>\n<p class="lead">{inline(clead)}</p>\n'
             f'<div class="prose">{md(cbody)}</div>')
    (ROOT / "ai/coaching").mkdir(parents=True, exist_ok=True)
    (ROOT / "ai/coaching/index.html").write_text(
        page("How To Coach An AI", "The order to give feedback in, and where a correction has to be written to last.", cpage))
    (ROOT / "ai/index.html").write_text(
        page("The Evolution: How I Work With AI",
             "How Daegan Smith's way of working with Claude changed, wall by wall.", body))
    print(f"ai: hub, glossary ({len(terms)} terms), {len(stages)} stage pages")


if __name__ == "__main__":
    main()
