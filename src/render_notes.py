import html,re,sys,os
REPO="/home/claude/maximum-leverage"
STYLE=open(REPO+"/index.html").read().split("<style>")[1].split("</style>")[0]
EXTRA="""
.foot a{color:inherit;margin-right:14px}
.back{font-size:15px;font-weight:bold;text-decoration:none;border-bottom:2px solid var(--ink)}
.tools{display:flex;gap:16px;margin:0 0 20px;font-size:14px}
.tools button{font:inherit;font-weight:bold;background:none;border:none;border-bottom:2px solid var(--ink);color:var(--ink);padding:0;cursor:pointer}
.ol,.ol ul{list-style:none;margin:0;padding:0}
.ol ul{padding-left:22px;border-left:1px solid var(--rule);margin-left:6px}
.ol li{position:relative;margin:0}
.row{display:block;position:relative;padding:5px 0 5px 22px;line-height:1.5}
.row::before{content:"";position:absolute;left:4px;top:calc(5px + .75em - 3.5px);width:7px;height:7px;border-radius:50%;background:var(--ink)}
details>summary{list-style:none;cursor:pointer}
details>summary::-webkit-details-marker{display:none}
details:not([open])>summary.row::before{box-shadow:0 0 0 4px var(--rule)}
details>summary.row:hover{opacity:.75}
.ol>li>details>summary,.ol>li>.row{font-weight:bold;font-size:20px}
.ol>li{padding:6px 0;border-bottom:1px solid var(--rule)}
.ol ul .row{font-size:17px}
.ol ul ul .row{color:var(--soft)}
"""
def esc(s):
    s=html.escape(s)
    return re.sub(r"\b([A-Z]{3,}(?:\s+[A-Z]{2,})*)\b",r"<strong>\1</strong>",s)
def parse(src):
    title=by="";root=[];stack=[(-1,root)]
    for ln in open(src).read().splitlines():
        if not ln.strip():continue
        if ln.startswith("# "):title=ln[2:].strip();continue
        if ln.startswith("@ "):by=ln[2:].strip();continue
        if ln.startswith("## "):d=0;txt=ln[3:].strip()
        else:
            m=re.match(r"( *)- (.*)",ln);txt=m.group(2)
            d=len(m.group(1))//2+(1 if any(l.startswith("## ") for l in open(src)) else 0)
        node={"t":txt,"k":[]}
        while stack[-1][0]>=d:stack.pop()
        stack[-1][1].append(node);stack.append((d,node["k"]))
    return title,by,root
def r(nodes):
    o=[]
    for n in nodes:
        if n["k"]:o.append(f'<li><details><summary class="row">{esc(n["t"])}</summary><ul>{r(n["k"])}</ul></details></li>')
        else:o.append(f'<li><span class="row">{esc(n["t"])}</span></li>')
    return "".join(o)
JS="""<script>function tg(o){document.querySelectorAll('.ol details').forEach(function(d){d.open=o;});}</script>"""
def page(title,by,body):
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{html.escape(title)} | Daegan Smith</title><style>{STYLE}{EXTRA}</style></head><body><div class="wrap">
<p><a class="back" href="../">&larr; Notes</a></p>
<p class="kicker">{html.escape(by)}</p>
<h1>{html.escape(title)}</h1>
<div class="tools"><button onclick="tg(true)">Open all</button><button onclick="tg(false)">Close all</button></div>
<ul class="ol">{body}</ul>
<p class="foot"><a href="/invisible-funnel/">Course</a><a href="/terms/">Terms</a><a href="/refunds/">Refunds</a><a href="/privacy/">Privacy</a><a href="/contact/">Contact</a><br>&copy; Daegan Smith</p></div>{JS}</body></html>"""
for slug in sys.argv[1:]:
    t,b,tree=parse(f"{REPO}/src/notes/{slug}.md")
    os.makedirs(f"{REPO}/notes/{slug}",exist_ok=True)
    open(f"{REPO}/notes/{slug}/index.html","w").write(page(t,b,r(tree)))
    print("built",slug)
