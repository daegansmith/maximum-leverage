#!/usr/bin/env python3
"""Put the standard site footer on every page of daegansmith.me.

Run from the repo root after adding or regenerating any page:  python3 src/footer.py
Safe to run again: it replaces its own footer and any older Terms/Refunds/Privacy footer.

Skipped: redirect pages, the admin page (its builder adds the footer itself),
and Adrianne's site mockups under kim/ (they show her site, not this one).
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP_PREFIX = ("kim/", "admin/", "src/", ".git/")

STYLE = ("max-width:620px;margin:60px auto 0;padding:0 24px 50px;"
         "font-family:Tahoma,Geneva,Verdana,sans-serif;font-size:14px;line-height:1.7;text-align:left;color:inherit;opacity:.65")
A = 'style="color:inherit"'


def footer(is_home):
    home = "" if is_home else f'<a href="/" {A}>Home</a> &middot; '
    return (f'<!--site-foot--><footer class="site-foot" style="{STYLE}">{home}'
            f'<a href="/terms/" {A}>Terms</a> &middot; <a href="/refunds/" {A}>Refunds</a> &middot; '
            f'<a href="/privacy/" {A}>Privacy</a> &middot; <a href="/contact/" {A}>Contact</a><br>'
            f'&copy; Daegan Smith &middot; <a href="/ai/" style="color:inherit;opacity:.6;text-decoration:none">Claude</a> &middot; <a href="https://claude.ai/artifact/DbWXMjjYmeCDTjt3jBJEUR" style="color:inherit;opacity:.6;text-decoration:none">Sessions</a> &middot; <a href="/admin/" style="color:inherit;opacity:.6;text-decoration:none">Admin</a>'
            f'</footer><!--/site-foot-->')


OURS = re.compile(r"<!--site-foot-->.*?<!--/site-foot-->\n*", re.S)
OLD = re.compile(r'<p class="foot">(?:(?!</p>).)*?/?terms/(?:(?!</p>).)*?</p>', re.S)


def main():
    changed = 0
    for p in sorted(ROOT.rglob("*.html")):
        rel = p.relative_to(ROOT).as_posix()
        if rel.startswith(SKIP_PREFIX):
            continue
        s = p.read_text(errors="ignore")
        if 'http-equiv="refresh"' in s:
            continue
        new = footer(rel == "index.html")
        t = OURS.sub("", s)
        if not rel.startswith("2guys-site/"):
            t = OLD.sub("", t)
        i = t.lower().rfind("</body>")
        t = t[:i] + new + "\n" + t[i:] if i >= 0 else t + "\n" + new + "\n"
        if t != s:
            p.write_text(t)
            changed += 1
    print(f"footer: {changed} pages updated")


if __name__ == "__main__":
    main()
