#!/usr/bin/env python3
"""Actualiza equipos Rubí / Zafiro (Hoenn) desde datos curados."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "trainers_db.json")

MOVE_SLUG = {
    "sonicboom": "sonic-boom",
    "thundershock": "thunder-shock",
    "selfdestruct": "self-destruct",
    "defense curl": "defense-curl",
    "rock tomb": "rock-tomb",
    "rock throw": "rock-throw",
    "focus energy": "focus-energy",
    "karate chop": "karate-chop",
    "sand attack": "sand-attack",
    "arm thrust": "arm-thrust",
    "bulk up": "bulk-up",
    "thunder wave": "thunder-wave",
    "shock wave": "shock-wave",
    "light screen": "light-screen",
    "body slam": "body-slam",
    "teeter dance": "teeter-dance",
    "belly drum": "belly-drum",
    "faint attack": "feint-attack",
    "feint attack": "feint-attack",
    "slack off": "slack-off",
    "aerial ace": "aerial-ace",
    "double team": "double-team",
    "quick attack": "quick-attack",
    "steel wing": "steel-wing",
    "dragonbreath": "dragon-breath",
    "dragon breath": "dragon-breath",
    "dragon dance": "dragon-dance",
    "ancientpower": "ancient-power",
    "calm mind": "calm-mind",
    "sunny day": "sunny-day",
    "confuse ray": "confuse-ray",
    "solarbeam": "solar-beam",
    "solar beam": "solar-beam",
    "rock slide": "rock-slide",
    "sweet kiss": "sweet-kiss",
    "water pulse": "water-pulse",
    "rain dance": "rain-dance",
    "aurora beam": "aurora-beam",
    "horn attack": "horn-attack",
    "take down": "take-down",
    "fake out": "fake-out",
    "needle arm": "needle-arm",
    "cotton spore": "cotton-spore",
    "swords dance": "swords-dance",
    "future sight": "future-sight",
    "shadow punch": "shadow-punch",
    "shadow ball": "shadow-ball",
    "skill swap": "skill-swap",
    "will-o-wisp": "will-o-wisp",
    "ice beam": "ice-beam",
    "ice ball": "ice-ball",
    "sheer cold": "sheer-cold",
    "scary face": "scary-face",
    "dragon claw": "dragon-claw",
    "sandstorm": "sandstorm",
    "meteor mash": "meteor-mash",
    "double edge": "double-edge",
    "giga drain": "giga-drain",
    "hyper beam": "hyper-beam",
    "overheat": "overheat",
    "extrasensory": "extrasensory",
}

TYPE_MAP = {
    "normal": "normal",
    "tierra": "ground",
    "volador": "flying",
    "bicho": "bug",
    "veneno": "poison",
    "psíquico": "psychic",
    "psiquico": "psychic",
    "fantasma": "ghost",
    "lucha": "fighting",
    "agua": "water",
    "fuego": "fire",
    "eléctrico": "electric",
    "electrico": "electric",
    "roca": "rock",
    "acero": "steel",
    "hielo": "ice",
    "planta": "grass",
    "dragón": "dragon",
    "dragon": "dragon",
    "siniestro": "dark",
}

POKE_TYPES = {
    "geodude": ["rock", "ground"],
    "nosepass": ["rock"],
    "machop": ["fighting"],
    "makuhita": ["fighting"],
    "magnemite": ["electric", "steel"],
    "voltorb": ["electric"],
    "magneton": ["electric", "steel"],
    "slugma": ["fire"],
    "torkoal": ["fire"],
    "spinda": ["normal"],
    "vigoroth": ["normal"],
    "linoone": ["normal"],
    "slaking": ["normal"],
    "swellow": ["normal", "flying"],
    "pelipper": ["water", "flying"],
    "skarmory": ["steel", "flying"],
    "altaria": ["dragon", "flying"],
    "claydol": ["ground", "psychic"],
    "xatu": ["psychic", "flying"],
    "lunatone": ["rock", "psychic"],
    "solrock": ["rock", "psychic"],
    "luvdisc": ["water"],
    "whiscash": ["water", "ground"],
    "sealeo": ["ice", "water"],
    "seaking": ["water"],
    "milotic": ["water"],
    "mightyena": ["dark"],
    "shiftry": ["grass", "dark"],
    "cacturne": ["grass", "dark"],
    "sharpedo": ["water", "dark"],
    "absol": ["dark"],
    "dusclops": ["ghost"],
    "banette": ["ghost"],
    "sableye": ["dark", "ghost"],
    "glalie": ["ice"],
    "walrein": ["ice", "water"],
    "shelgon": ["dragon"],
    "flygon": ["ground", "dragon"],
    "salamence": ["dragon", "flying"],
    "skarmory": ["steel", "flying"],
    "aggron": ["steel", "rock"],
    "cradily": ["rock", "grass"],
    "armaldo": ["rock", "bug"],
    "metagross": ["steel", "psychic"],
}


def slug_move(name: str) -> str:
    key = name.strip().lower()
    if key in MOVE_SLUG:
        return MOVE_SLUG[key]
    key2 = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return MOVE_SLUG.get(key2, key2)


def m(display: str, move_type: str | None = None) -> dict:
    slug = slug_move(display)
    return {
        "name": slug,
        "name_display": display,
        **({"move_type": move_type} if move_type else {}),
    }


def mon(name: str, level: int, moves: list[tuple[str, str]]) -> dict:
    types = POKE_TYPES.get(name, ["normal"])
    return {
        "name": name,
        "name_display": name.replace("-", " ").title(),
        "level": level,
        "types": types,
        "moves": [m(d, TYPE_MAP.get(t.lower(), t.lower())) for d, t in moves],
    }


def team(*mons) -> list:
    return list(mons)


RS_TEAMS = {
    "Roxanne": team(
        mon("geodude", 14, [("Tackle", "Normal"), ("Defense Curl", "Normal")]),
        mon("nosepass", 15, [("Tackle", "Normal"), ("Harden", "Normal"), ("Rock Tomb", "Roca"), ("Block", "Normal")]),
    ),
    "Brawly": team(
        mon("machop", 17, [("Leer", "Normal"), ("Focus Energy", "Normal"), ("Karate Chop", "Lucha")]),
        mon("makuhita", 18, [("Sand Attack", "Tierra"), ("Arm Thrust", "Lucha"), ("Bulk Up", "Lucha")]),
    ),
    "Wattson": team(
        mon("magnemite", 22, [("Supersonic", "Normal"), ("SonicBoom", "Normal"), ("Thunder Wave", "Eléctrico"), ("Shock Wave", "Eléctrico")]),
        mon("voltorb", 20, [("Rollout", "Roca"), ("Spark", "Eléctrico"), ("Selfdestruct", "Normal")]),
        mon("magneton", 23, [("Supersonic", "Normal"), ("SonicBoom", "Normal"), ("Thunder Wave", "Eléctrico"), ("Shock Wave", "Eléctrico")]),
    ),
    "Flannery": team(
        mon("slugma", 24, [("Smog", "Veneno"), ("Ember", "Fuego"), ("Rock Throw", "Roca"), ("Light Screen", "Psíquico")]),
        mon("slugma", 24, [("Smog", "Veneno"), ("Ember", "Fuego"), ("Rock Throw", "Roca"), ("Light Screen", "Psíquico")]),
        mon("torkoal", 29, [("Body Slam", "Normal"), ("Attract", "Normal"), ("Overheat", "Fuego")]),
    ),
    "Norman": team(
        mon("spinda", 27, [("Teeter Dance", "Normal"), ("Psybeam", "Psíquico"), ("Facade", "Normal")]),
        mon("vigoroth", 27, [("Encore", "Normal"), ("Slash", "Normal"), ("Facade", "Normal")]),
        mon("linoone", 29, [("Belly Drum", "Normal"), ("Headbutt", "Normal"), ("Facade", "Normal")]),
        mon("slaking", 31, [("Yawn", "Normal"), ("Facade", "Normal"), ("Faint Attack", "Siniestro"), ("Slack Off", "Normal")]),
    ),
    "Winona": team(
        mon("swellow", 31, [("Aerial Ace", "Volador"), ("Double Team", "Normal"), ("Endeavor", "Normal"), ("Quick Attack", "Normal")]),
        mon("pelipper", 30, [("Protect", "Normal"), ("Supersonic", "Normal"), ("Wing Attack", "Volador"), ("Mist", "Hielo")]),
        mon("skarmory", 32, [("Sand Attack", "Tierra"), ("Fury Attack", "Normal"), ("Steel Wing", "Acero"), ("Aerial Ace", "Volador")]),
        mon("altaria", 33, [("DragonBreath", "Dragón"), ("Earthquake", "Tierra"), ("Aerial Ace", "Volador"), ("Dragon Dance", "Dragón")]),
    ),
    "Tate & Liza": team(
        mon("claydol", 41, [("Earthquake", "Tierra"), ("AncientPower", "Roca"), ("Light Screen", "Psíquico"), ("Reflect", "Psíquico")]),
        mon("xatu", 41, [("Psychic", "Psíquico"), ("Calm Mind", "Psíquico"), ("Sunny Day", "Fuego"), ("Confuse Ray", "Fantasma")]),
        mon("lunatone", 42, [("Psychic", "Psíquico"), ("Hypnosis", "Psíquico"), ("Calm Mind", "Psíquico"), ("Rock Slide", "Roca")]),
        mon("solrock", 42, [("Psychic", "Psíquico"), ("Sunny Day", "Fuego"), ("SolarBeam", "Planta"), ("Rock Slide", "Roca")]),
    ),
    "Wallace": team(
        mon("luvdisc", 40, [("Attract", "Normal"), ("Sweet Kiss", "Normal"), ("Water Pulse", "Agua"), ("Flail", "Normal")]),
        mon("whiscash", 42, [("Amnesia", "Psíquico"), ("Water Pulse", "Agua"), ("Earthquake", "Tierra"), ("Rain Dance", "Agua")]),
        mon("sealeo", 40, [("Aurora Beam", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo"), ("Water Pulse", "Agua")]),
        mon("seaking", 42, [("Horn Attack", "Normal"), ("Supersonic", "Normal"), ("Water Pulse", "Agua"), ("Rain Dance", "Agua")]),
        mon("milotic", 43, [("Recover", "Normal"), ("Attract", "Normal"), ("Water Pulse", "Agua"), ("Refresh", "Normal")]),
    ),
    "Sidney": team(
        mon("mightyena", 46, [("Sand Attack", "Tierra"), ("Take Down", "Normal"), ("Crunch", "Siniestro"), ("Roar", "Normal")]),
        mon("shiftry", 48, [("Double Team", "Normal"), ("Swagger", "Normal"), ("Extrasensory", "Psíquico"), ("Fake Out", "Normal")]),
        mon("cacturne", 46, [("Needle Arm", "Planta"), ("Cotton Spore", "Planta"), ("Feint Attack", "Siniestro"), ("Sand Attack", "Tierra")]),
        mon("sharpedo", 48, [("Surf", "Agua"), ("Crunch", "Siniestro"), ("Swagger", "Normal"), ("Screech", "Normal")]),
        mon("absol", 49, [("Slash", "Normal"), ("Swords Dance", "Normal"), ("Aerial Ace", "Volador"), ("Future Sight", "Psíquico")]),
    ),
    "Phoebe": team(
        mon("dusclops", 48, [("Shadow Punch", "Fantasma"), ("Curse", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Protect", "Normal")]),
        mon("banette", 49, [("Shadow Ball", "Fantasma"), ("Skill Swap", "Psíquico"), ("Thunderbolt", "Eléctrico"), ("Psychic", "Psíquico")]),
        mon("banette", 49, [("Shadow Ball", "Fantasma"), ("Grudge", "Fantasma"), ("Will-O-Wisp", "Fuego"), ("Faint Attack", "Siniestro")]),
        mon("sableye", 50, [("Shadow Ball", "Fantasma"), ("Fake Out", "Normal"), ("Attract", "Normal"), ("Faint Attack", "Siniestro")]),
        mon("dusclops", 51, [("Shadow Punch", "Fantasma"), ("Curse", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Ice Beam", "Hielo")]),
    ),
    "Glacia": team(
        mon("glalie", 50, [("Ice Beam", "Hielo"), ("Light Screen", "Psíquico"), ("Crunch", "Siniestro"), ("Hail", "Hielo")]),
        mon("sealeo", 50, [("Ice Ball", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo"), ("Rest", "Psíquico")]),
        mon("sealeo", 52, [("Ice Ball", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo"), ("Rest", "Psíquico")]),
        mon("glalie", 52, [("Ice Beam", "Hielo"), ("Crunch", "Siniestro"), ("Light Screen", "Psíquico"), ("Hail", "Hielo")]),
        mon("walrein", 53, [("Surf", "Agua"), ("Body Slam", "Normal"), ("Ice Beam", "Hielo"), ("Sheer Cold", "Hielo")]),
    ),
    "Drake": team(
        mon("shelgon", 52, [("Rock Tomb", "Roca"), ("DragonBreath", "Dragón"), ("Protect", "Normal"), ("Scary Face", "Normal")]),
        mon("altaria", 54, [("DragonBreath", "Dragón"), ("Aerial Ace", "Volador"), ("Dragon Dance", "Dragón"), ("Earthquake", "Tierra")]),
        mon("flygon", 53, [("Flamethrower", "Fuego"), ("DragonBreath", "Dragón"), ("Crunch", "Siniestro"), ("Fly", "Volador")]),
        mon("flygon", 53, [("DragonBreath", "Dragón"), ("Sandstorm", "Roca"), ("Earthquake", "Tierra"), ("Fly", "Volador")]),
        mon("salamence", 55, [("Dragon Claw", "Dragón"), ("Flamethrower", "Fuego"), ("Fly", "Volador"), ("Crunch", "Siniestro")]),
    ),
    "Steven": team(
        mon("skarmory", 57, [("Toxic", "Veneno"), ("Aerial Ace", "Volador"), ("Protect", "Normal"), ("Steel Wing", "Acero")]),
        mon("claydol", 55, [("Earthquake", "Tierra"), ("AncientPower", "Roca"), ("Psychic", "Psíquico"), ("Reflect", "Psíquico")]),
        mon("aggron", 56, [("Double Edge", "Normal"), ("Earthquake", "Tierra"), ("Aerial Ace", "Volador"), ("Dragon Claw", "Dragón")]),
        mon("cradily", 56, [("Giga Drain", "Planta"), ("AncientPower", "Roca"), ("Confuse Ray", "Fantasma"), ("Recover", "Normal")]),
        mon("armaldo", 56, [("Slash", "Normal"), ("AncientPower", "Roca"), ("Aerial Ace", "Volador"), ("Water Pulse", "Agua")]),
        mon("metagross", 58, [("Meteor Mash", "Acero"), ("Psychic", "Psíquico"), ("Earthquake", "Tierra"), ("Hyper Beam", "Normal")]),
    ),
}

UPDATE_NAMES = set(RS_TEAMS.keys())
GAME_SLUGS = ("ruby-sapphire",)


def strip_move_type(moves: list[dict]) -> list[dict]:
    out = []
    for mv in moves:
        out.append({"name": mv["name"], "name_display": mv["name_display"]})
    return out


def apply_team(trainer: dict, new_team: list[dict]) -> None:
    cleaned = []
    for poke in new_team:
        p = {**poke, "moves": strip_move_type(poke["moves"])}
        cleaned.append(p)
    trainer["team"] = cleaned


def main():
    with open(DB_PATH, encoding="utf-8") as f:
        db = json.load(f)

    updated = []
    for slug in GAME_SLUGS:
        for tr in db["trainers"][slug]:
            if tr["name"] in UPDATE_NAMES:
                apply_team(tr, RS_TEAMS[tr["name"]])
                updated.append(f"{slug}/{tr['name']}")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Actualizados:", ", ".join(updated))


if __name__ == "__main__":
    main()
