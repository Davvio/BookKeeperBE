from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.item_category import ItemCategory
from app.models.item import Item
from app.models.structure_settings import StructureSettings

CATEGORIES = [
    ("ore","Ore"),("ingot","Ingot"),("gem","Gem"),("crop","Crop"),
    ("food","Food"),("material","Material"),("tool","Tool"),
    ("weapon","Weapon"),("armor","Armor"),("potion","Potion"),
    ("mob_drop","Mob Drop"),("block","Block"),("misc","Misc"),
]

CORE_ITEMS = [
    ("Iron Ingot","ingot"),
    ("Gold Ingot","ingot"),
    ("Diamond","gem"),
    ("Emerald","gem"),
    ("Coal","ore"),
    ("Copper Ingot","ingot"),
    ("Redstone","ore"),
    ("Lapis Lazuli","gem"),
]

def seed_minimal(db: Session, admin_user_id: int | None = None):
    # categories
    for code, name in CATEGORIES:
        if not db.query(ItemCategory.id).filter(ItemCategory.code == code).first():
            db.add(ItemCategory(code=code, name=name))
    db.commit()

    # core items
    from app.services.codegen import generate_unique_item_code
    for name, cat in CORE_ITEMS:
        exists = db.query(Item).filter(func.lower(Item.name) == name.lower()).first()
        if not exists:
            code = generate_unique_item_code(db, name)
            db.add(Item(
                name=name, code=code, category=cat, stack_size=64, is_active=True,
                created_by_user_id=admin_user_id or 1
            ))
    db.commit()

    # default currency per existing structure: iron_ingot if present
    iron = db.query(Item).filter(Item.code == "iron_ingot").first()
    if not iron:
        return
    # find all distinct structure_ids from users
    from app.models.user import User
    structs = [r[0] for r in db.query(User.structure_id).distinct().all()]
    for sid in structs:
        ss = db.query(StructureSettings).get(sid)
        if not ss:
            ss = StructureSettings(structure_id=sid, currency_item_id=iron.id)
            db.add(ss)
        elif ss.currency_item_id is None:
            ss.currency_item_id = iron.id
    db.commit()
