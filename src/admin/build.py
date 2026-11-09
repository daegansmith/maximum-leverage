#!/usr/bin/env python3
"""Build admin/index.html: Daegan's private to-dos plus a map of every page on daegansmith.me.

The page is encrypted (AES-GCM, key from the password via PBKDF2-SHA256), so neither the
to-dos nor the map can be read in the page source without the password.

Usage (from the repo root):
  ADMIN_PASSWORD=...... python3 src/admin/build.py                 # rescan the site, keep the current to-dos
  ADMIN_PASSWORD=...... python3 src/admin/build.py --todos FILE.md # rescan and replace the to-dos
  ADMIN_PASSWORD=...... python3 src/admin/build.py --dump-todos    # print the current to-dos markdown

To-dos markdown: "## Section", then "- [ ] **Title** rest", "- [x] ..." for done,
"- ..." for a plain bullet, two spaces of indent per nesting level, [text](url) links.
The working copy of the to-dos is the "Daegan's To-Dos" Claude Doc; this page mirrors it.
"""
import argparse, base64, datetime, html, json, os, re, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "admin" / "index.html"
ITER = 250000
TODO_DOC = "https://claude.ai/artifact/J9ts9zs3NMpPzXfwC9jD93"

# ---------------------------------------------------------------- site map groups
# Each group: (title, note, open?, [patterns]). A page goes in the first group whose pattern matches.
# Within a group, pages keep the order of the patterns, then sort by path.
GROUPS = [
    ("The site, as visitors see it", "Linked from the homepage.", True, [
        "index.html", "projects.html", "notes/index.html", "notes/*", "ideas/index.html", "ideas/*",
        "library/index.html", "library/*", "quotes/*", "stories/index.html", "stories/my-story/*", "stories/*",
        "testimonials/*", "invisible-funnel/*", "maximum-leverage/*", "work-with-me/*",
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
    ("How I use Claude", "", False, ["ai/index.html", "ai/*"]),
    ("Adrianne's site", "Her looks, and the adrianne.yoga mockups.", False, ["kim/index.html", "kim/*"]),
    ("Redirects", "", False, ["todos.html"]),
]
SKIP = {"admin/index.html"}


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


# ---------------------------------------------------------------- to-dos markdown -> html
def inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
    s = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r'<a href="\2">\1</a>', s)
    return s


def todos_html(md):
    out, stack = [], []  # stack of open <ul> depths
    def close_to(depth):
        while len(stack) > depth:
            out.append("</li></ul>")
            stack.pop()
    section_open = False
    for line in md.splitlines():
        if not line.strip():
            continue
        if line.startswith("## "):
            close_to(0)
            if section_open:
                out.append("</details>" if done_section else "")
            name = line[3:].strip()
            done_section = name.lower() in ("done", "let go")
            if done_section:
                out.append(f'<details class="fold"><summary>{inline(name)}</summary>')
            else:
                out.append(f"<h3>{inline(name)}</h3>")
            section_open = True
            continue
        m = re.match(r"^( *)- (\[( |x)\] )?(.*)$", line)
        if not m:
            continue
        depth = len(m.group(1)) // 2 + 1
        state = m.group(3)
        cls = "done" if state == "x" else ("task" if state == " " else "plain")
        if len(stack) < depth:
            out.append('<ul class="todo">')
            stack.append(depth)
        else:
            close_to(depth)
            out.append("</li>")
        out.append(f'<li class="{cls}">{inline(m.group(4))}')
    close_to(0)
    if section_open and done_section:
        out.append("</details>")
    return "\n".join(x for x in out if x)


# ---------------------------------------------------------------- page
def body_html(todos_md, groups, n):
    today = datetime.date.today().strftime("%b %-d, %Y")
    parts = [f'<p class="kicker">Private &middot; updated {today}</p><h1>Admin</h1>',
             f'<p>Your to-dos, then every page on daegansmith.me ({n} of them), hidden ones included.</p>',
             '<nav class="jump"><a href="#todos">To-dos</a> &middot; <a href="#map">Site map</a></nav>',
             '<section id="todos"><h2>To-Dos</h2>',
             f'<p class="note">The working copy is the <a href="{TODO_DOC}">Daegan\'s To-Dos</a> doc. This page mirrors it.</p>',
             todos_html(todos_md), "</section>",
             '<section id="map"><h2>Site Map</h2>']
    for title, note, is_open, items in groups:
        lis = "".join(
            f'<li><a href="{url_of(p)}">{html.escape(page_title(ROOT / p))}</a> <span class="path">/{html.escape(p.replace("index.html", ""))}</span></li>'
            for p in items)
        note_html = f'<p class="note">{html.escape(note)}</p>' if note else ""
        op = " open" if is_open else ""
        parts.append(f'<details class="grp"{op}><summary>{html.escape(title)} <span class="n">{len(items)}</span></summary>{note_html}<ul class="map">{lis}</ul></details>')
    parts.append("</section>")
    return "\n".join(parts)


def encrypt(password, payload):
    salt, iv = os.urandom(16), os.urandom(12)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER)
    key = kdf.derive(password.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(payload).encode(), None)
    b = lambda x: base64.b64encode(x).decode()
    return {"salt": b(salt), "iv": b(iv), "ct": b(ct), "iter": ITER}


def decrypt(password, blob):
    d = lambda x: base64.b64decode(x)
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=d(blob["salt"]), iterations=blob["iter"])
    key = kdf.derive(password.encode())
    return json.loads(AESGCM(key).decrypt(d(blob["iv"]), d(blob["ct"]), None))


def current_payload(password):
    if not OUT.exists():
        return None
    m = re.search(r'<script id="vault" type="application/json">(.*?)</script>', OUT.read_text(), re.S)
    return decrypt(password, json.loads(m.group(1))) if m else None


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
ul.todo{list-style:none;padding:0;margin:0 0 10px}
ul.todo ul.todo{margin:8px 0 0 22px}
ul.todo li{position:relative;padding-left:28px;margin-bottom:12px;font-size:16px}
ul.todo li::before{content:"";position:absolute;left:0;top:5px;width:14px;height:14px;border:2px solid var(--ink)}
ul.todo li.plain::before{border:0;width:6px;height:6px;top:10px;left:4px;background:var(--soft)}
ul.todo li.done{color:var(--soft)}
ul.todo li.done::before{background:var(--soft);border-color:var(--soft)}
details{margin:0 0 12px}
summary{cursor:pointer;font-weight:bold;padding:8px 0}
details.fold>summary{font-size:19px}
details.grp{border:2px solid var(--ink);padding:4px 14px;margin-bottom:14px}
.n{font-weight:normal;color:var(--soft);font-size:14px;margin-left:6px}
ul.map{padding-left:18px;margin:4px 0 12px}
ul.map li{margin-bottom:8px;font-size:16px}
.path{display:block;font-size:12px;color:var(--soft);word-break:break-all}
#gate form{display:flex;gap:10px;margin-top:10px}
#gate input{flex:1;font:inherit;padding:10px 12px;border:2px solid var(--ink);background:var(--bg);color:var(--ink)}
#gate button{font:inherit;font-weight:bold;padding:10px 18px;border:2px solid var(--ink);background:var(--ink);color:var(--bg);cursor:pointer}
#err{color:#b0302a;font-size:15px;margin-top:10px}
.foot{margin-top:30px;font-size:13px;color:var(--soft)}
</style></head><body><div class="wrap">
<div id="gate"><p class="kicker">Private</p><h1>Admin</h1><p>Password, please.</p>
<form id="f"><input id="pw" type="password" inputmode="numeric" autocomplete="current-password" aria-label="Password"><button>Open</button></form>
<p id="err" hidden>That's not it.</p></div>
<div id="out" hidden></div>
<p class="foot" id="lock" hidden><a href="#" id="lockl">Lock this page on this device</a> &middot; <a href="../">Home</a></p>
</div>
<script id="vault" type="application/json">__VAULT__</script>
<script>
(function(){
var V=JSON.parse(document.getElementById("vault").textContent),K="ml_admin_pw";
function b(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)});}
async function open(pw){
  var base=await crypto.subtle.importKey("raw",new TextEncoder().encode(pw),"PBKDF2",false,["deriveKey"]);
  var key=await crypto.subtle.deriveKey({name:"PBKDF2",salt:b(V.salt),iterations:V.iter,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["decrypt"]);
  var pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b(V.iv)},key,b(V.ct));
  var data=JSON.parse(new TextDecoder().decode(pt));
  var out=document.getElementById("out");out.innerHTML=data.html;out.hidden=false;
  document.getElementById("gate").hidden=true;document.getElementById("lock").hidden=false;
  try{localStorage.setItem(K,pw);}catch(e){}
  if(location.hash){var t=document.querySelector(location.hash);if(t)t.scrollIntoView();}
}
document.getElementById("f").addEventListener("submit",function(e){e.preventDefault();
  document.getElementById("err").hidden=true;
  open(document.getElementById("pw").value).catch(function(){document.getElementById("err").hidden=false;});});
document.getElementById("lockl").addEventListener("click",function(e){e.preventDefault();try{localStorage.removeItem(K);}catch(x){}location.reload();});
var saved=null;try{saved=localStorage.getItem(K);}catch(e){}
if(saved){open(saved).catch(function(){try{localStorage.removeItem(K);}catch(e){}});}
})();
</script>
</body></html>
"""


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todos", help="markdown file with the to-dos (replaces the current ones)")
    ap.add_argument("--dump-todos", action="store_true")
    a = ap.parse_args()
    pw = os.environ.get("ADMIN_PASSWORD")
    if not pw:
        sys.exit("Set ADMIN_PASSWORD.")
    cur = current_payload(pw)
    if a.dump_todos:
        print(cur["todos_md"] if cur else "")
        return
    if a.todos:
        todos_md = Path(a.todos).read_text()
    elif cur:
        todos_md = cur["todos_md"]
    else:
        sys.exit("No current admin page; pass --todos FILE.md.")
    groups, n = site_map()
    payload = {"todos_md": todos_md, "html": body_html(todos_md, groups, n)}
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(SHELL.replace("__VAULT__", json.dumps(encrypt(pw, payload))))
    print(f"Wrote {OUT.relative_to(ROOT)}: {n} pages mapped.")


if __name__ == "__main__":
    main()
