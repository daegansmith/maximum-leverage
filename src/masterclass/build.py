#!/usr/bin/env python3
"""Build invisible-funnel/masterclass/index.html: the private access space for the
Invisible Funnel Masterclass. Everything a member sees is encrypted inside the page
(AES-GCM, key from the password via PBKDF2-SHA256), the same way the admin page is.

This repo is public, so the lesson text is never stored here. It is read at build time
from the private claude-library repo and only the encrypted page is written.

Usage (from the repo root):
  MASTERCLASS_PASSWORD=... MASTERCLASS_SRC=/path/to/claude-library/marketing/own-work/invisible-funnel python3 src/masterclass/build.py
"""
import base64, html, json, os, re, sys
from pathlib import Path
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from footer import footer as site_footer

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "invisible-funnel" / "masterclass" / "index.html"
ITER = 600000
# (file in MASTERCLASS_SRC, id, one line under the title). Order is the order members see.
LESSONS = [
    ("story-selling-email-story-selling.md", "story-selling", "How to tell a story that sells without selling, in emails, pages, videos and webinars."),
    ("creating-content-that-sells.md", "content-that-sells", "The ideal buying state, the logical chain of beliefs, and over-delivering on purpose."),
    ("irresistible-offer-creation.md", "irresistible-offer", "What people pay high-ticket prices for, and how to build the offer everything else points at."),
    ("reverse-selling-funnel-creation-process.md", "reverse-selling-funnel", "How to get them to sell you: the points, the application and the homework."),
    ("reverse-selling-secret-sauce-script-writing.md", "after-the-application", "The reverse selling conversation, from state of mind to the invitation."),
]
LINK = re.compile(r"\[([^\]]+)\]\((https?://[^)]+)\)")


def esc(s):
    """Escape text, turn [text](url) into a link, and bold words written in capitals."""
    out, pos = [], 0
    for m in LINK.finditer(s):
        out.append(html.escape(s[pos:m.start()]))
        out.append(f'<a href="{html.escape(m.group(2))}" target="_blank" rel="noopener">{html.escape(m.group(1))}</a>')
        pos = m.end()
    out.append(html.escape(s[pos:]))
    return "".join(out)


def parse(path):
    """A 4-space indented outline. First line is the source line and is skipped."""
    title, root, stack = None, [], [(-1, None)]
    stack[0] = (-1, root)
    for ln in path.read_text().split("\n")[1:]:
        if not ln.strip():
            continue
        depth = (len(ln) - len(ln.lstrip(" "))) // 4
        text = re.sub(r"\s+", " ", ln.strip())
        if title is None:
            title = text
            continue
        node = {"t": text, "k": []}
        while stack[-1][0] >= depth:
            stack.pop()
        stack[-1][1].append(node)
        stack.append((depth, node["k"]))
    return title, root


def render(nodes):
    o = []
    for n in nodes:
        if n["k"]:
            o.append(f'<li><details><summary class="row">{esc(n["t"])}</summary><ul>{render(n["k"])}</ul></details></li>')
        else:
            o.append(f'<li><span class="row">{esc(n["t"])}</span></li>')
    return "".join(o)


def body_html(src):
    cards, lessons = [], []
    for fname, lid, desc in LESSONS:
        title, tree = parse(src / fname)
        cards.append(f'<a class="card" href="#{lid}" data-go="{lid}"><span class="ct">{html.escape(title)}</span><span class="cd">{html.escape(desc)}</span></a>')
        lessons.append(
            f'<div class="lesson" id="{lid}" hidden><p><a class="back" href="#home" data-go="home">&larr; All lessons</a></p>'
            f'<p class="kicker">Invisible Funnel Masterclass</p><h1>{html.escape(title)}</h1>'
            '<div class="tools"><button data-all="1">Open all</button><button data-all="0">Close all</button></div>'
            f'<ul class="ol">{render(tree)}</ul></div>')
    home = ('<div class="lesson" id="home"><p class="kicker">Members only</p><h1>Invisible Funnel Masterclass</h1>'
            '<p>Your lessons. Tap one to open it.</p><div class="cards">' + "".join(cards) + "</div></div>")
    return home + "".join(lessons)


def encrypt(password, payload):
    salt, iv = os.urandom(16), os.urandom(12)
    key = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=ITER).derive(password.encode())
    ct = AESGCM(key).encrypt(iv, json.dumps(payload).encode(), None)
    b = lambda x: base64.b64encode(x).decode()
    return {"salt": b(salt), "iv": b(iv), "ct": b(ct), "iter": ITER}


SHELL = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>Invisible Funnel Masterclass</title>
<style>
:root{--bg:#fff;--ink:#111;--soft:#555;--rule:#ddd}
@media (prefers-color-scheme:dark){:root{--bg:#141414;--ink:#EDEBE5;--soft:#B4B2A9;--rule:#343330}}
*,*::before,*::after{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:Tahoma,Geneva,Verdana,sans-serif;font-size:19px;line-height:1.6}
.wrap{max-width:620px;margin:0 auto;padding:56px 20px 80px}
a{color:var(--ink)}
.kicker{font-size:12px;font-weight:bold;letter-spacing:1px;text-transform:uppercase;color:var(--soft);margin:0 0 10px}
h1{font-size:40px;font-weight:900;letter-spacing:-0.5px;line-height:1.1;margin:0 0 24px}
p{margin:0 0 18px}
.cards{display:grid;gap:12px}
.card{display:grid;gap:4px;padding:16px 18px;border:2px solid var(--ink);color:var(--ink);text-decoration:none}
.card:hover,.card:focus-visible{background:var(--ink);color:var(--bg);outline:none}
.card:hover .cd,.card:focus-visible .cd{color:var(--bg)}
.ct{font-size:20px;font-weight:bold;line-height:1.3}
.cd{font-size:16px;line-height:1.5;color:var(--soft)}
.back{font-size:15px;font-weight:bold;text-decoration:none;border-bottom:2px solid var(--ink)}
.tools{display:flex;gap:16px;margin:0 0 20px;font-size:14px}
.tools button{font:inherit;font-weight:bold;background:none;border:none;border-bottom:2px solid var(--ink);color:var(--ink);padding:0;cursor:pointer}
.ol,.ol ul{list-style:none;margin:0;padding:0}
.ol ul{padding-left:22px;border-left:1px solid var(--rule);margin-left:6px}
.row{display:block;position:relative;padding:5px 0 5px 22px;line-height:1.5;overflow-wrap:anywhere}
.row::before{content:"";position:absolute;left:4px;top:calc(5px + .75em - 3.5px);width:7px;height:7px;border-radius:50%;background:var(--ink)}
details>summary{list-style:none;cursor:pointer}
details>summary::-webkit-details-marker{display:none}
details:not([open])>summary.row::before{box-shadow:0 0 0 4px var(--rule)}
.ol>li>details>summary,.ol>li>.row{font-weight:bold;font-size:20px}
.ol>li{padding:6px 0;border-bottom:1px solid var(--rule)}
.ol ul .row{font-size:17px}
.ol ul ul .row{color:var(--soft)}
#gate form{display:flex;gap:10px;margin-top:10px}
#gate input{flex:1;min-width:0;font:inherit;padding:10px 12px;border:2px solid var(--ink);background:var(--bg);color:var(--ink)}
#gate button{font:inherit;font-weight:bold;padding:10px 18px;border:2px solid var(--ink);background:var(--ink);color:var(--bg);cursor:pointer}
#err{color:#b0302a;font-size:15px;margin-top:10px}
.foot{margin-top:30px;font-size:13px;color:var(--soft)}
</style></head><body><div class="wrap">
<div id="gate"><p class="kicker">Members only</p><h1>Invisible Funnel Masterclass</h1><p>Enter your access phrase.</p>
<form id="f"><input id="pw" type="password" autocomplete="current-password" aria-label="Access phrase"><button>Open</button></form>
<p id="err" hidden>That's not it.</p></div>
<div id="out" hidden></div>
<p class="foot" id="lock" hidden><a href="#" id="lockl">Lock this page on this device</a></p>
</div>
__FOOT__
<script id="vault" type="application/json">__VAULT__</script>
<script>
(function(){
var V=JSON.parse(document.getElementById("vault").textContent),K="if_masterclass_pw",out=document.getElementById("out");
function b(s){return Uint8Array.from(atob(s),function(c){return c.charCodeAt(0)});}
function show(id){var L=out.querySelectorAll(".lesson"),hit=false;
  L.forEach(function(d){var on=d.id===id;d.hidden=!on;if(on)hit=true;});
  if(!hit&&L.length)L[0].hidden=false;window.scrollTo(0,0);}
async function open(pw){
  var base=await crypto.subtle.importKey("raw",new TextEncoder().encode(pw),"PBKDF2",false,["deriveKey"]);
  var key=await crypto.subtle.deriveKey({name:"PBKDF2",salt:b(V.salt),iterations:V.iter,hash:"SHA-256"},base,{name:"AES-GCM",length:256},false,["decrypt"]);
  var pt=await crypto.subtle.decrypt({name:"AES-GCM",iv:b(V.iv)},key,b(V.ct));
  out.innerHTML=JSON.parse(new TextDecoder().decode(pt)).html;out.hidden=false;
  document.getElementById("gate").hidden=true;document.getElementById("lock").hidden=false;
  try{localStorage.setItem(K,pw);}catch(e){}
  show((location.hash||"#home").slice(1));
}
out.addEventListener("click",function(e){
  var g=e.target.closest("[data-go]");
  if(g){e.preventDefault();history.replaceState(null,"","#"+g.dataset.go);show(g.dataset.go);return;}
  var a=e.target.closest("[data-all]");
  if(a){a.closest(".lesson").querySelectorAll("details").forEach(function(d){d.open=a.dataset.all==="1";});}
});
document.getElementById("f").addEventListener("submit",function(e){e.preventDefault();
  document.getElementById("err").hidden=true;
  open(document.getElementById("pw").value.trim()).catch(function(){document.getElementById("err").hidden=false;});});
document.getElementById("lockl").addEventListener("click",function(e){e.preventDefault();
  try{localStorage.removeItem(K);}catch(x){}location.reload();});
var saved=null;try{saved=localStorage.getItem(K);}catch(e){}
if(saved)open(saved).catch(function(){try{localStorage.removeItem(K);}catch(x){}});
})();
</script></body></html>
"""


def main():
    pw, src = os.environ.get("MASTERCLASS_PASSWORD"), os.environ.get("MASTERCLASS_SRC")
    if not pw or not src:
        sys.exit("Set MASTERCLASS_PASSWORD and MASTERCLASS_SRC.")
    if len(pw) < 16:
        sys.exit("Use an access phrase of at least 16 characters. This repo is public, so a short one can be guessed.")
    inner = body_html(Path(src))
    if os.environ.get("MASTERCLASS_PREVIEW"):
        Path(os.environ["MASTERCLASS_PREVIEW"]).write_text(inner)
    vault = json.dumps(encrypt(pw, {"html": inner}))
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(SHELL.replace("__FOOT__", site_footer(False)).replace("__VAULT__", vault))
    print(f"Wrote {OUT.relative_to(ROOT)}: {len(LESSONS)} lessons, {len(inner)//1024} KB before encryption.")


if __name__ == "__main__":
    main()
