#!/usr/bin/env python3
"""Build the finding pages under /ai/<slug>/ from src/ai/findings/<slug>.md.

A finding is one change to how I work with Claude, told as a story at the top
(frames from src/ai/strips/specs.json sit in it at [[1]] ... [[6]]), with the record in drop-downs under it.
Run from the repo root:  python3 src/ai/findings.py && python3 src/footer.py
"""
import html
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build as B  # noqa: E402  (the stage-page helpers: head, page, md, inline, title_case)

ROOT = B.ROOT
FINDINGS = {
    "belief-chain": {
        "kicker": "My Skills &middot; November 12, 2026 &middot; Checked and updated November 13 &middot; A simulation, not a live test",
        "skill_pair": "belief-chain-skill",
        "desc": "I cut my belief chain to three steps in a simulation. It sold the same. What moved sales, and how my belief-chain skill changed.",
    },
}

B.EXTRA_CSS += """
.pair{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin:4px 0 24px}
.pair img{width:100%;height:auto;display:block}
@media(max-width:560px){.pair{grid-template-columns:1fr}.pair img{max-width:440px}}
.story p.upd{border-left:4px solid #c8372d;background:#faf6f0;padding:10px 14px;margin:0 0 10px;font-size:17px}
.story p.upd+p:not(.upd){margin-top:26px}
"""


def build(slug, cfg):
    text = (B.ROOT / "src/ai/findings" / f"{slug}.md").read_text().strip()
    assert "—" not in text, "em dash in " + slug
    parts = re.split(r"^## (.+)$", text, flags=re.M)
    story_md, record = parts[0].strip(), [(parts[i].strip(), parts[i + 1]) for i in range(1, len(parts), 2)]
    sl = [x.strip() for x in story_md.split("\n\n") if x.strip()]
    assert sl[0].startswith("# ")
    title = sl[0][2:]
    strip = B.STRIPS[slug]
    pair = B.STRIPS.get(cfg.get("skill_pair"))

    def para(x):
        m = re.fullmatch(r"\[\[(\d|skill)\]\]", x)
        if not m:
            if x.startswith("!! "):  # a dated update, set apart from the story as it was first written
                return f'<p class="upd">{B.inline(x[3:])}</p>'
            return f"<p>{B.inline(x)}</p>"
        if m.group(1) == "skill":
            imgs = "".join(
                f'<img src="../{cfg["skill_pair"]}/f{i + 1}.png" alt="{html.escape(" ".join(f["cap"]), quote=True)}" loading="lazy">'
                for i, f in enumerate(pair["frames"]))
            return f'<div class="pair">{imgs}</div>'
        f = strip["frames"][int(m.group(1)) - 1]
        alt = html.escape(" ".join(f["cap"]), quote=True)
        return f'<img class="frame" src="f{m.group(1)}.png" alt="{alt}" loading="lazy">'

    story = "".join(para(x) for x in sl[1:])
    items = "".join(
        f'<li><details><summary class="row">{html.escape(B.title_case(t))}</summary>'
        f'<div class="sec">{re.sub(r"(<table>.*?</table>)", r"<div class=tw>\1</div>", B.md(b), flags=re.S)}</div></details></li>\n'
        for t, b in record)
    body = (
        '<p><a class="back" href="../">&larr; The Evolution</a></p>\n'
        f'<p class="kicker">{cfg["kicker"]}</p>\n'
        f'<h2 class="shead">{html.escape(title)}</h2>\n'
        f'<img class="arcimg" src="arc.png" alt="{html.escape(strip["title"], quote=True)}: how it went, in six points">\n'
        f'<div class="story">{story}</div>\n'
        f'<p class="small arcfoot">{html.escape(strip["foot"])}</p>\n'
        '<p class="kicker rec">The Record</p>\n'
        '<div class="tools"><button onclick="tg(true)">Open all</button><button onclick="tg(false)">Close all</button></div>\n'
        f'<ul class="ol">\n{items}</ul>\n'
        '<p class="small" style="margin-top:28px">From the record: the project doc Belief Chain Compression / Chain Walk Results (Nov 12), '
        'the skill as saved in my library on Nov 10 and as it runs now, and my Ideas note The Three-Belief Chain (Oct 19).</p>\n'
        '<div class="nav"><a href="../skills/">&larr; Every Skill I Work With</a><span></span></div>')
    script = "<script>function tg(o){document.querySelectorAll('.ol details').forEach(function(d){d.open=o;});}</script>"
    d = ROOT / "ai" / slug
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(B.page(title, cfg["desc"], body, script))
    print("finding:", slug)


if __name__ == "__main__":
    for s, c in FINDINGS.items():
        build(s, c)
