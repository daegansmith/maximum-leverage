"""Private 'From Jimmy' links page. Same lock as the to-do page.
  TODO_PW=... python3 -I tools/jimmy/jimmy.py decrypt   -> writes tools/jimmy/.content.html (gitignored)
  TODO_PW=... python3 -I tools/jimmy/jimmy.py encrypt   -> rebuilds jimmy/index.html from .content.html
Never commit .content.html or the password."""
import os, sys, re, json, base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(os.path.dirname(HERE))
PAGE, SRC, TPL = os.path.join(ROOT, "jimmy", "index.html"), os.path.join(HERE, ".content.html"), os.path.join(HERE, "template.html")
pw = os.environ["TODO_PW"].encode()
kdf = lambda salt, it: PBKDF2HMAC(hashes.SHA256(), 32, salt, it).derive(pw)
if sys.argv[1] == "decrypt":
    P = json.loads(re.search(r"const P = (\{.*?\});", open(PAGE).read()).group(1))
    d = lambda k: base64.b64decode(P[k])
    open(SRC, "wb").write(AESGCM(kdf(d("salt"), P["iter"])).decrypt(d("iv"), d("ct"), None)); print("decrypted ->", SRC)
else:
    salt, iv, it = os.urandom(16), os.urandom(12), 600000
    ct = AESGCM(kdf(salt, it)).encrypt(iv, open(SRC, "rb").read(), None)
    e = lambda b: base64.b64encode(b).decode()
    os.makedirs(os.path.dirname(PAGE), exist_ok=True)
    open(PAGE, "w").write(open(TPL).read().replace("__PAYLOAD__", json.dumps({"salt": e(salt), "iv": e(iv), "iter": it, "ct": e(ct)})))
    print("encrypted ->", PAGE)
