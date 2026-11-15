# daegansmith.me

Served by GitHub Pages from this repo (main branch). Push site changes here directly.

## Every page gets the site footer

Terms · Refunds · Privacy · Contact, © Daegan Smith · Admin. After adding or regenerating any page, run:

    python3 src/footer.py

It is safe to run repeatedly. It skips redirect pages, `admin/` (its builder adds the footer) and Adrianne's mockups under `kim/`.

## Admin page (/admin/)

Private, password-gated (Daegan has the password; never commit it). In this order: Private tools (What's Happening, his one daily page; the Session Board; the Explainer Library), Only for Daegan, the site as visitors see it (a site map), then one Local AI card with a section per group. The to-dos live only in the "Daegan's To-Dos" Claude Doc, reached from What's Happening; never copy them onto the site.

    python3 src/admin/build.py

No password needed to rebuild. Like the 2 Guys admin, the list is plain HTML behind a password screen; the gate checks the typed password against the sealed blob in `src/admin/gate.json` (never replace that file without Daegan's password). The same saved password opens the Invisible Funnel Masterclass.

Rerun it whenever pages are added so the site map stays complete. New pages land under "Everything else" until a group in `src/admin/build.py` claims them.
