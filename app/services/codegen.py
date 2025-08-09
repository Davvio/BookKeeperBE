import re
import unicodedata
from sqlalchemy.orm import Session
from app.models.item import Item

_slug_re = re.compile(r"[^a-z0-9]+")
def _slugify(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = s.lower().strip()
    s = _slug_re.sub("_", s).strip("_")
    return s[:40] or "item"

def generate_unique_item_code(db: Session, name: str) -> str:
    base = _slugify(name)
    code = base
    i = 2
    while db.query(Item.id).filter(Item.code == code).first():
        code = f"{base}_{i}"
        i += 1
    return code
