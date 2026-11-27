# daegansmith.me

Served by GitHub Pages from this repo (main branch). Push site changes here directly.

## Every page gets the site footer

Terms · Refunds · Privacy · Contact, © Daegan Smith · Admin. After adding or regenerating any page, run:

    python3 src/footer.py

It is safe to run repeatedly. It skips redirect pages, `admin/` (its builder adds the footer) and Adrianne's mockups under `kim/`.

## Every page must fit a phone

`src/footer.py` also puts a small "phone guard" style in each page's head (long words and links wrap; pictures, videos and frames never get wider than the screen). After adding or changing pages, run both, in this order, and fix anything the check reports before pushing:

    python3 src/footer.py
    python3 tools/mobile-check.py

The check opens every page at 320px and 390px wide and fails any page that scrolls sideways or lacks the phone viewport tag. Grids use `minmax(min(300px,100%),1fr)`, never a bare `minmax(300px,1fr)`, so they shrink on small phones. The whole site stays white with black text (`data-theme="light"` on every page); don't add dark-mode styles back.

## Admin page (/admin/)

Private. It is NOT in this repo (the repo is public). Cloudflare serves it at daegansmith.me/admin/ through the Worker `daegansmith-admin`, reading KV namespace `daegansmith-admin`, key `index.html`. Cloudflare Access locks it: only daegansmith@me.com gets in, with a code emailed to him. Never commit the Admin page or its list to this repo.

In this order: Private tools (What's Happening, his one daily page; the Session Board; the Explainer Library; the Jimmy Library), Only for Daegan, the site as visitors see it (a site map), then one Local AI card with a section per group. The to-dos live only in the "Daegan's To-Dos" Claude Doc, reached from What's Happening; never copy them onto the site.

    python3 src/admin/build.py

That writes `.admin-build/index.html` (git-ignored). Upload it to the KV key above with the CloudFlare connector (PUT /accounts/3f44a6ff3ef329448333af7623605a72/storage/kv/namespaces/3daea43cbbb142f8b93bcf23971b87b0/values/index.html). Rerun whenever pages are added so the site map stays complete. New pages land under "Everything else" until a group in `src/admin/build.py` claims them.

Cloudflare is in front of the whole site (DNS proxied, SSL Full, Always HTTPS). GitHub Pages still serves every other page.
