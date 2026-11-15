#!/usr/bin/env python3
"""Build admin/index.html: a map of every page on daegansmith.me, plus links to Daegan's
private tools in Claude: What's Happening (his one daily page), the Session Board and the
Explainer Library. The to-dos live only in the "Daegan's To-Dos" Claude Doc, reached from What's Happening.

The page is NOT in this public repo. Cloudflare serves it at daegansmith.me/admin/ from the
Worker "daegansmith-admin" (KV namespace "daegansmith-admin", key index.html), behind Cloudflare
Access: only daegansmith@me.com gets in, with a code emailed to him.

Usage (from the repo root):  python3 src/admin/build.py
It writes .admin-build/index.html (git-ignored). Then upload that file to the KV key above with
the CloudFlare connector. Rerun whenever pages are added; it rescans the whole site.
"""

import datetime, html, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from footer import footer as site_footer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / ".admin-build" / "index.html"  # never committed; uploaded to Cloudflare
TODO_DOC = "https://claude.ai/artifact/J9ts9zs3NMpPzXfwC9jD93"
WHATS_HAPPENING = "https://claude.ai/artifact/YQMJrnhX17SwDTaRCBkp19"
EXPLAINERS = "https://claude.ai/artifact/RkbSiZys1GXmj5wu4NVPKd"
SESSION_BOARD = "https://claude.ai/artifact/DbWXMjjYmeCDTjt3jBJEUR"

# ---------------------------------------------------------------- site map groups
# Each group: (title, note, open?, [patterns]). A page goes in the first group whose pattern matches.
# Within a group, pages keep the order of the patterns, then sort by path.
GROUPS = [
    ("Only for Daegan", "Ideas and Library open by link only. The Masterclass lessons open with your Masterclass password.", True, [
        "invisible-funnel/masterclass/*", "ideas/index.html", "ideas/*", "library/index.html", "library/*"]),
    ("The site, as visitors see it", "Linked from the homepage.", True, [
        "index.html", "projects.html", "notes/index.html", "notes/*", "ai/index.html", "ai/*", "quotes/*", "stories/index.html", "stories/my-story/*", "stories/*",
        "testimonials/*", "invisible-funnel/index.html", "maximum-leverage/*", "work-with-me/*",
        "contact/*", "terms/*", "refunds/*", "privacy/*"]),
    ("Local AI, now", "The Nov 9 night and what's running for it.", True, [
        "2guys-site/market-domination-map-v1.html", "fishers-nov9/index.html", "fishers-nov9/*",
        "leader-outreach/*", "workshop-v16.4-offer-v12.html", "client-pages.html", "before-after.html",
        "2guys-site/scoreboard.html", "2guys-site/proof.html"]),
    ("Local AI: Jimmy", "Pages made for Jimmy.", False, [
        "jimmy/*", "jimmy-oct-27/*", "dr-mccray/*", "tools/jimmy/*"]),
    ("Local AI: 2 Guys site mockups", "The 2guysandagenie.com mockups from Nov 6 and 7.", False, [
        "2guys-site/index.html", "2guys-site/*"]),
    ("Local AI: client intake and research", "The E60 walkthrough, its consultation script, the assessment demo, the demo board.", False, [
        "intake/script.html", "intake/*", "assessment.html", "e60-mockup.html", "board/*"]),
    ("Local AI: event video", "The invitation sales video scripts and story.", False, ["event-vsl-*"]),
    ("Local AI: earlier presentation and offer versions", "Every saved workshop and offer version, newest first.", False, [
        "workshop*", "offer*"]),
    ("Local AI: the Oct 27 Fishers funnel", "Opt-in, registration and thank-you versions, and the twelve emails.", False, [
        "fishers-emails*", "fishers-episode-*", "fishers-*"]),
    ("Local AI: early planning", "", False, ["dream-version.html", "front-end-options.html"]),
    ("Adrianne's site", "Her looks, and the adrianne.yoga mockups.", False, ["kim/index.html", "kim/*"]),
    ("Redirects", "", False, ["todos.html"]),
]
SKIP = {"admin/index.html", ".admin-build/index.html"}


def match(pat, path):
    if pat.endswith("*"):
        return path.startswith(pat[:-1])
    return path == pat


def natkey(s):
    return [int(t) if t.isdigit() else t for t in re.split(r"(\d+)", s)]


def page_title(p):
    try:
        m = re.search(r"<title>(.*?)</title>", p.read_text(errors="ignore"), re.S | re.I)
    except Exception:
        m = None
    t = html.unescape(m.group(1).strip()) if m else ""
    t = re.sub(r"\s*\|\s*Daegan Smith$", "", t)
    return t or p.name


def url_of(rel):
    if rel.endswith("index.html"):
        rel = rel[: -len("index.html")]
    return "../" + rel if rel else "../"


def site_map():
    rels = [p.relative_to(ROOT) for p in ROOT.rglob("*.html")]
    pages = sorted(str(r) for r in rels if r.parts[0] not in (".git", "src"))
    pages = [p for p in pages if p not in SKIP]
    placed, out = set(), []
    for title, note, is_open, pats in GROUPS:
        items = []
        for pat in pats:
            hits = [p for p in pages if p not in placed and match(pat, p)]
            if "earlier presentation" in title:
                hits.sort(key=natkey, reverse=True)
            else:
                hits.sort(key=natkey)
            for h in hits:
                placed.add(h)
                items.append(h)
        if items:
            out.append((title, note, is_open, items))
    rest = [p for p in pages if p not in placed]
    if rest:
        out.append(("Everything else", "Pages no group above claims yet.", True, rest))
    return out, len(pages)



# ---------------------------------------------------------------- tags
# A page can carry several tags. The tag row at the top shows one thread across every group.
TAGS = [
    ("jimmy", "Jimmy", ["jimmy/", "jimmy-oct-27/", "dr-mccray/", "tools/jimmy/", "client-pages.html"]),
    ("2guys", "2 Guys", ["2guys-site/", "fishers-nov9/", "leader-outreach/", "board/", "before-after", "client-pages.html", "workshop-v16.4"]),
    ("fishers", "Fishers Funnel", ["fishers-", "event-vsl-"]),
    ("offer", "Workshop And Offer", ["workshop", "offer", "front-end-options", "dream-version", "intake/", "assessment"]),
    ("ai", "AI Log", ["ai/"]),
    ("notes", "Notes And Ideas", ["notes/", "library/", "ideas/", "quotes/", "stories/"]),
    ("mine", "My Business", ["index.html", "projects.html", "work-with-me/", "maximum-leverage/", "invisible-funnel/", "testimonials/"]),
    ("adrianne", "Adrianne", ["kim/"]),
]


def tags_of(path):
    out = []
    for key, _label, pats in TAGS:
        if any(path.startswith(pt) or (pt == "index.html" and path == pt) for pt in pats if pt != "index.html") or (path == "index.html" and "index.html" in pats):
            out.append(key)
    return out

# ---------------------------------------------------------------- page
def body_html(groups, n):
    today = datetime.date.today().strftime("%b %-d, %Y")
    parts = [f'<p class="kicker">Private &middot; updated {today}</p><h1>Admin</h1>',
             f'<p>Every page on daegansmith.me ({n} of them), hidden ones included.</p>',
             '<details class="grp" open><summary>Private tools</summary><ul class="map">'
             f'<li><a href="{WHATS_HAPPENING}">What\'s Happening</a> <span class="path">Your one daily page: today, to-dos, email, agent mail, Notion and sessions, in Claude</span></li>'
             f'<li><a href="{SESSION_BOARD}">Session Board</a> <span class="path">Every open Claude session and where it stands, in Claude</span></li>'
             f'<li><a href="{EXPLAINERS}">Explainer Library</a> <span class="path">Every narrated explainer Claude has made you, in Claude</span></li>'
             '<li><a href="https://2guysandagenie.com/library/">The Jimmy Library</a> <span class="path">Everything Jimmy sent, by week, tagged by thread, on 2guysandagenie.com</span></li>'
             '</ul></details>',
             '<div id="tagbar"><p class="note" style="margin:0 0 6px">Tap a tag to see one thread across every group. Tap it again to see everything.</p>'
             + "".join(f'<button type="button" class="tg" data-t="{k}">{html.escape(lab)}</button>' for k, lab, _ in TAGS) + '</div>']
    def lis_of(items):
        return "".join(
            f'<li data-tags="{" ".join(tags_of(p))}"><a href="{url_of(p)}">{html.escape(page_title(ROOT / p))}</a> <span class="path">/{html.escape(p.replace("index.html", ""))}</span></li>'
            for p in items)
    # Every "Local AI" group goes into one card, with a section for each.
    local = [g for g in groups if g[0].startswith("Local AI")]
    local_done = False
    for title, note, is_open, items in groups:
        if title.startswith("Local AI"):
            if local_done:
                continue
            local_done = True
            subs = []
            for t, nt, op_, its in local:
                name = re.sub(r"^Local AI[:,]\s*", "", t)
                name = name[:1].upper() + name[1:]
                note_html = f'<p class="note">{html.escape(nt)}</p>' if nt else ""
                op = " open" if op_ else ""
                subs.append(f'<details class="sub"{op}><summary>{html.escape(name)} <span class="n">{len(its)}</span></summary>{note_html}<ul class="map">{lis_of(its)}</ul></details>')
            total = sum(len(g[3]) for g in local)
            parts.append(f'<details class="grp" open><summary>Local AI <span class="n">{total}</span></summary>{"".join(subs)}</details>')
            continue
        note_html = f'<p class="note">{html.escape(note)}</p>' if note else ""
        op = " open" if is_open else ""
        parts.append(f'<details class="grp"{op}><summary>{html.escape(title)} <span class="n">{len(items)}</span></summary>{note_html}<ul class="map">{lis_of(items)}</ul></details>')
    return "\n".join(parts)


SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Admin</title>
<style>
:root{--bg:#fff;--ink:#111;--soft:#555;--rule:#ddd}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--ink:#EDEBE5;--soft:#B4B2A9;--rule:#343330}}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,Geneva,Verdana,sans-serif;font-size:18px;line-height:1.55}
.wrap{max-width:620px;margin:0 auto;padding:44px 20px 80px}
a{color:inherit}
.kicker{font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:var(--soft);margin:0 0 8px}
h1{font-size:40px;font-weight:900;line-height:1.1;margin:0 0 16px}
h2{font-size:26px;margin:0 0 14px}
h3{font-size:19px;margin:28px 0 8px}
p{margin:0 0 14px}
section{padding:34px 0 10px;border-top:1px solid var(--rule);margin-top:24px}
.jump{font-size:15px;color:var(--soft)}
.note{font-size:15px;color:var(--soft)}
details{margin:0 0 12px}
summary{cursor:pointer;font-weight:bold;padding:8px 0}
details.fold>summary{font-size:19px}
details.grp{border:2px solid var(--ink);padding:4px 14px;margin-bottom:14px}
details.sub{border-top:1px solid var(--rule);margin:0}
details.sub>summary{font-size:16px}
.n{font-weight:normal;color:var(--soft);font-size:14px;margin-left:6px}
ul.map{padding-left:18px;margin:4px 0 12px}
ul.map li{margin-bottom:8px;font-size:16px}
.path{display:block;font-size:12px;color:var(--soft);word-break:break-all}
#gate form{display:flex;gap:10px;margin-top:10px}
#gate input{flex:1;font:inherit;padding:10px 12px;border:2px solid var(--ink);background:var(--bg);color:var(--ink)}
#gate button{font:inherit;font-weight:bold;padding:10px 18px;border:2px solid var(--ink);background:var(--ink);color:var(--bg);cursor:pointer}
#err{color:#b0302a;font-size:15px;margin-top:10px}
.foot{margin-top:30px;font-size:13px;color:var(--soft)}
.tg{font:bold 12px Tahoma,Geneva,Verdana,sans-serif;letter-spacing:.3px;text-transform:uppercase;padding:4px 9px;margin:0 6px 6px 0;border:2px solid var(--ink);color:var(--ink);background:none;cursor:pointer}.tg.on{background:var(--ink);color:var(--bg)}#tagbar{margin:0 0 16px}.tghide{display:none!important}
</style></head><body><div class="wrap">
<div id="out">__BODY__</div>
</div>
__FOOT__
<script>
(function(){
var on=null;document.addEventListener("click",function(e){var bt=e.target.closest(".tg");if(!bt)return;on=on===bt.dataset.t?null:bt.dataset.t;
  document.querySelectorAll(".tg").forEach(function(x){x.classList.toggle("on",x.dataset.t===on)});
  document.querySelectorAll("#out li[data-tags]").forEach(function(li){li.classList.toggle("tghide",!!on&&li.dataset.tags.split(" ").indexOf(on)<0)});
  document.querySelectorAll("#out details").forEach(function(d){if(!d.querySelector("li[data-tags]"))return;if(on){var any=d.querySelectorAll("li[data-tags]:not(.tghide)").length;d.classList.toggle("tghide",!any);if(any)d.open=true}else{d.classList.remove("tghide")}})});
})();
</script>
</body></html>
"""


def main():
    groups, n = site_map()
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(SHELL.replace("__FOOT__", site_footer(False)).replace("__BODY__", body_html(groups, n)))
    print(f"Wrote {OUT.relative_to(ROOT)}: {n} pages mapped.")


if __name__ == "__main__":
    main()
