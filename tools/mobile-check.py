#!/usr/bin/env python3
"""Phone check for daegansmith.me.

Opens every public page at phone widths and reports anything that makes the
page wider than the screen (sideways scrolling), plus pages with no phone
viewport tag. Run it from the repo root after changing pages:

    python3 tools/mobile-check.py            # all pages
    python3 tools/mobile-check.py notes/     # only pages under notes/

Needs Python Playwright and a Chrome or Chromium. It serves the repo on a
local port, so it tests the files as they are now, before pushing.
Exit code 1 if any page fails.
"""
import asyncio, http.server, os, pathlib, re, socketserver, sys, threading

ROOT = pathlib.Path(__file__).resolve().parent.parent
SKIP_DIRS = {".git", "kim", ".admin-build", "node_modules"}
WIDTHS = [320, 390]
PORT = 8799


def pages(prefix=""):
    out = []
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or not str(rel).startswith(prefix):
            continue
        head = p.read_text(errors="ignore")[:3000].lower()
        if 'http-equiv="refresh"' in head:
            continue  # redirect page
        out.append(rel)
    return out


def serve():
    os.chdir(ROOT)
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *a, **k):
            super().__init__(*a, directory=str(ROOT), **k)
        def log_message(self, *a):
            pass
    socketserver.TCPServer.allow_reuse_address = True
    httpd = socketserver.ThreadingTCPServer(("127.0.0.1", PORT), Quiet)
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd


FIND_WIDE = """(w)=>{
  const out=[];
  for(const el of document.querySelectorAll('body *')){
    const r=el.getBoundingClientRect();
    if(r.width===0||r.height===0)continue;
    const cs=getComputedStyle(el);
    if(cs.position==='fixed')continue;
    if(r.right>w+1){
      let p=el.parentElement,clipped=false;
      while(p&&p!==document.body){const o=getComputedStyle(p).overflowX;if(o==='auto'||o==='scroll'||o==='hidden'){clipped=true;break;}p=p.parentElement;}
      if(!clipped)out.push((el.tagName.toLowerCase())+(el.id?'#'+el.id:'')+(el.className&&typeof el.className==='string'?'.'+el.className.trim().split(/\\s+/).join('.'):'')+' '+Math.round(r.right)+'px');
    }
  }
  return out.slice(0,5);
}"""


async def main(prefix):
    from playwright.async_api import async_playwright
    exe = next((c for c in ["/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"] if os.path.exists(c)), None)
    todo = pages(prefix)
    bad = []
    httpd = serve()
    async with async_playwright() as p:
        b = await p.chromium.launch(executable_path=exe, args=["--no-sandbox"]) if exe else await p.chromium.launch()
        for w in WIDTHS:
            ctx = await b.new_context(viewport={"width": w, "height": 800}, is_mobile=True, has_touch=True)
            await ctx.route(re.compile(r"^https?://(?!127\.0\.0\.1).*"), lambda r: r.abort())
            pg = await ctx.new_page()
            for rel in todo:
                url = f"http://127.0.0.1:{PORT}/{rel.as_posix()}"
                try:
                    await pg.goto(url, wait_until="load", timeout=20000)
                    await pg.wait_for_timeout(150)
                except Exception as e:
                    bad.append((str(rel), w, f"did not load: {e.__class__.__name__}"))
                    continue
                has_vp = await pg.evaluate("!!document.querySelector('meta[name=viewport]')")
                sw = await pg.evaluate("document.documentElement.scrollWidth")
                if not has_vp:
                    bad.append((str(rel), w, "no phone viewport tag"))
                if sw > w + 1:
                    wide = await pg.evaluate(FIND_WIDE, w)
                    bad.append((str(rel), w, f"{sw}px wide: " + "; ".join(wide)))
            await ctx.close()
        await b.close()
    httpd.shutdown()
    print(f"Checked {len(todo)} pages at {', '.join(map(str, WIDTHS))}px.")
    for rel, w, why in bad:
        print(f"FAIL {rel} @{w}: {why}")
    if not bad:
        print("All pages fit a phone.")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "")))
