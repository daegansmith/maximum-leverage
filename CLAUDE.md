# daegansmith.me

Served by GitHub Pages from this repo (main branch). Push site changes here directly.

## Every page gets the site footer

Terms · Refunds · Privacy · Contact, © Daegan Smith · Admin. After adding or regenerating any page, run:

    python3 src/footer.py

It is safe to run repeatedly. It skips redirect pages, `admin/` (its builder adds the footer) and Adrianne's mockups under `kim/`.

## Admin page (/admin/)

Private, password-gated (Daegan has the password; never commit it). A map of every page on the site, plus a link to the "Daegan's To-Dos" Claude Doc. The to-dos live only in that doc; never copy them onto the site.

    ADMIN_PASSWORD=... python3 src/admin/build.py

Rerun it whenever pages are added so the site map stays complete. New pages land under "Everything else" until a group in `src/admin/build.py` claims them.
