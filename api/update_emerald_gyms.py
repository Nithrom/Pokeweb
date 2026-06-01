#!/usr/bin/env python3
"""Actualiza equipos Esmeralda desde datos curados."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "trainers_db.json")

MOVE_SLUG = {
    "sonicboom": "sonic-boom",
    "selfdestruct": "self-destruct",
    "defense curl": "defense-curl",
    "rock tomb": "rock-tomb",
    "bulk up": "bulk-up",
    "karate chop": "karate-chop",
    "seismic toss": "seismic-toss",
    "focus punch": "focus-punch",
    "hidden power": "hidden-power",
    "light screen": "light-screen",
    "arm thrust": "arm-thrust",
    "sand attack": "sand-attack",
    "vital throw": "vital-throw",
    "shock wave": "shock-wave",
    "thunder wave": "thunder-wave",
    "quick attack": "quick-attack",
    "thundershock": "thunder-shock",
    "magnitude": "magnitude",
    "sunny day": "sunny-day",
    "flamethrower": "flamethrower",
    "rock slide": "rock-slide",
    "body slam": "body-slam",
    "overheat": "overheat",
    "teeter dance": "teeter-dance",
    "facade": "facade",
    "belly drum": "belly-drum",
    "faint attack": "feint-attack",
    "feint attack": "feint-attack",
    "aerial ace": "aerial-ace",
    "double team": "double-team",
    "water gun": "water-gun",
    "steel wing": "steel-wing",
    "dragonbreath": "dragon-breath",
    "dragon breath": "dragon-breath",
    "dragondance": "dragon-dance",
    "dragon dance": "dragon-dance",
    "ancientpower": "ancient-power",
    "calm mind": "calm-mind",
    "confuse ray": "confuse-ray",
    "solarbeam": "solar-beam",
    "solar beam": "solar-beam",
    "water pulse": "water-pulse",
    "sweet kiss": "sweet-kiss",
    "rain dance": "rain-dance",
    "aurora beam": "aurora-beam",
    "crabhammer": "crabhammer",
    "smokescreen": "smoke-screen",
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
    "water spout": "water-spout",
    "sludge bomb": "sludge-bomb",
    "giga drain": "giga-drain",
    "leech seed": "leech-seed",
    "hydro pump": "hydro-pump",
    "hyper beam": "hyper-beam",
    "extrasensory": "extrasensory",
}

TYPE_MAP = {
    "normal": "normal",
    "tierra": "ground",
    "volador": "flying",
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
    "variable": "normal",
}

POKE_TYPES = {
    "geodude": ["rock", "ground"],
    "nosepass": ["rock"],
    "machop": ["fighting"],
    "meditite": ["fighting", "psychic"],
    "makuhita": ["fighting"],
    "magnemite": ["electric", "steel"],
    "voltorb": ["electric"],
    "electrike": ["electric"],
    "magneton": ["electric", "steel"],
    "manectric": ["electric"],
    "numel": ["fire", "ground"],
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
    "crawdaunt": ["water", "dark"],
    "kingdra": ["water", "dragon"],
    "mightyena": ["dark"],
    "cacturne": ["grass", "dark"],
    "shiftry": ["grass", "dark"],
    "absol": ["dark"],
    "dusclops": ["ghost"],
    "banette": ["ghost"],
    "sableye": ["dark", "ghost"],
    "glalie": ["ice"],
    "walrein": ["ice", "water"],
    "shelgon": ["dragon"],
    "flygon": ["ground", "dragon"],
    "salamence": ["dragon", "flying"],
    "wailord": ["water"],
    "tentacruel": ["water", "poison"],
    "ludicolo": ["water", "grass"],
    "gyarados": ["water", "flying"],
    "milotic": ["water"],
}


def slug_move(name: str) -> str:
    key = name.strip().lower()
    if key in MOVE_SLUG:
        return MOVE_SLUG[key]
    key2 = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return MOVE_SLUG.get(key2, key2)


def m(display: str, move_type: str | None = None) -> dict:
    slug = slug_move(display)
    return {"name": slug, "name_display": display}


def mon(name: str, level: int, moves: list[tuple[str, str]]) -> dict:
    types = POKE_TYPES.get(name, ["normal"])
    return {
        "name": name,
        "name_display": name.replace("-", " ").title(),
        "level": level,
        "types": types,
        "moves": [m(d) for d, t in moves],
    }


def team(*mons) -> list:
    return list(mons)


EMERALD_TEAMS = {
    "Roxanne": team(
        mon("geodude", 12, [("Tackle", "Normal"), ("Defense Curl", "Normal")]),
        mon("geodude", 12, [("Tackle", "Normal"), ("Defense Curl", "Normal")]),
        mon("nosepass", 15, [("Rock Tomb", "Roca"), ("Tackle", "Normal"), ("Harden", "Normal"), ("Block", "Normal")]),
    ),
    "Brawly": team(
        mon("machop", 16, [("Bulk Up", "Lucha"), ("Karate Chop", "Lucha"), ("Seismic Toss", "Lucha"), ("Leer", "Normal")]),
        mon("meditite", 16, [("Focus Punch", "Lucha"), ("Detect", "Lucha"), ("Hidden Power", "Variable"), ("Light Screen", "Psíquico")]),
        mon("makuhita", 19, [("Bulk Up", "Lucha"), ("Arm Thrust", "Lucha"), ("Sand Attack", "Tierra"), ("Vital Throw", "Lucha")]),
    ),
    "Wattson": team(
        mon("magnemite", 20, [("Shock Wave", "Eléctrico"), ("SonicBoom", "Normal"), ("Thunder Wave", "Eléctrico"), ("Supersonic", "Normal")]),
        mon("voltorb", 20, [("Spark", "Eléctrico"), ("Rollout", "Roca"), ("Selfdestruct", "Normal"), ("Shock Wave", "Eléctrico")]),
        mon("electrike", 20, [("Quick Attack", "Normal"), ("Howl", "Normal"), ("Shock Wave", "Eléctrico"), ("Thunder Wave", "Eléctrico")]),
        mon("magneton", 22, [("Shock Wave", "Eléctrico"), ("Supersonic", "Normal"), ("SonicBoom", "Normal"), ("Thunder Wave", "Eléctrico")]),
        mon("manectric", 24, [("Quick Attack", "Normal"), ("Howl", "Normal"), ("Thunder Wave", "Eléctrico"), ("Shock Wave", "Eléctrico")]),
    ),
    "Flannery": team(
        mon("numel", 24, [("Magnitude", "Tierra"), ("Tackle", "Normal"), ("Sunny Day", "Fuego"), ("Ember", "Fuego")]),
        mon("slugma", 24, [("Light Screen", "Psíquico"), ("Sunny Day", "Fuego"), ("Flamethrower", "Fuego"), ("Rock Slide", "Roca")]),
        mon("slugma", 24, [("Light Screen", "Psíquico"), ("Sunny Day", "Fuego"), ("Flamethrower", "Fuego"), ("Rock Slide", "Roca")]),
        mon("torkoal", 29, [("Body Slam", "Normal"), ("Overheat", "Fuego"), ("Sunny Day", "Fuego"), ("Attract", "Normal")]),
    ),
    "Norman": team(
        mon("spinda", 27, [("Teeter Dance", "Normal"), ("Facade", "Normal"), ("Psybeam", "Psíquico"), ("Hypnosis", "Psíquico")]),
        mon("vigoroth", 27, [("Facade", "Normal"), ("Slash", "Normal"), ("Encore", "Normal"), ("Yawn", "Normal")]),
        mon("linoone", 29, [("Belly Drum", "Normal"), ("Facade", "Normal"), ("Headbutt", "Normal"), ("Sand Attack", "Tierra")]),
        mon("slaking", 31, [("Facade", "Normal"), ("Counter", "Lucha"), ("Yawn", "Normal"), ("Faint Attack", "Siniestro")]),
    ),
    "Winona": team(
        mon("swellow", 31, [("Aerial Ace", "Volador"), ("Double Team", "Normal"), ("Endeavor", "Normal"), ("Quick Attack", "Normal")]),
        mon("pelipper", 32, [("Protect", "Normal"), ("Aerial Ace", "Volador"), ("Water Gun", "Agua"), ("Supersonic", "Normal")]),
        mon("skarmory", 32, [("Steel Wing", "Acero"), ("Aerial Ace", "Volador"), ("Sand Attack", "Tierra"), ("Fury Attack", "Normal")]),
        mon("altaria", 33, [("Dragon Dance", "Dragón"), ("Earthquake", "Tierra"), ("DragonBreath", "Dragón"), ("Aerial Ace", "Volador")]),
    ),
    "Tate & Liza": team(
        mon("claydol", 41, [("Earthquake", "Tierra"), ("AncientPower", "Roca"), ("Light Screen", "Psíquico"), ("Reflect", "Psíquico")]),
        mon("xatu", 41, [("Psychic", "Psíquico"), ("Confuse Ray", "Fantasma"), ("Calm Mind", "Psíquico"), ("Sunny Day", "Fuego")]),
        mon("lunatone", 42, [("Psychic", "Psíquico"), ("Hypnosis", "Psíquico"), ("Calm Mind", "Psíquico"), ("Rock Slide", "Roca")]),
        mon("solrock", 42, [("Psychic", "Psíquico"), ("Sunny Day", "Fuego"), ("SolarBeam", "Planta"), ("Rock Slide", "Roca")]),
    ),
    "Juan": team(
        mon("luvdisc", 41, [("Water Pulse", "Agua"), ("Attract", "Normal"), ("Sweet Kiss", "Normal"), ("Charm", "Normal")]),
        mon("whiscash", 41, [("Water Pulse", "Agua"), ("Amnesia", "Psíquico"), ("Earthquake", "Tierra"), ("Rain Dance", "Agua")]),
        mon("sealeo", 43, [("Water Pulse", "Agua"), ("Aurora Beam", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo")]),
        mon("crawdaunt", 43, [("Crabhammer", "Agua"), ("Protect", "Normal"), ("Double Team", "Normal"), ("Taunt", "Siniestro")]),
        mon("kingdra", 46, [("Double Team", "Normal"), ("SmokeScreen", "Normal"), ("Rest", "Psíquico"), ("Water Pulse", "Agua")]),
    ),
    "Sidney": team(
        mon("mightyena", 46, [("Sand Attack", "Tierra"), ("Take Down", "Normal"), ("Crunch", "Siniestro"), ("Roar", "Normal")]),
        mon("cacturne", 46, [("Needle Arm", "Planta"), ("Cotton Spore", "Planta"), ("Feint Attack", "Siniestro"), ("Sand Attack", "Tierra")]),
        mon("shiftry", 48, [("Fake Out", "Normal"), ("Swagger", "Normal"), ("Extrasensory", "Psíquico"), ("Double Team", "Normal")]),
        mon("crawdaunt", 48, [("Crabhammer", "Agua"), ("Protect", "Normal"), ("Double Team", "Normal"), ("Taunt", "Siniestro")]),
        mon("absol", 49, [("Slash", "Normal"), ("Swords Dance", "Normal"), ("Aerial Ace", "Volador"), ("Future Sight", "Psíquico")]),
    ),
    "Phoebe": team(
        mon("dusclops", 48, [("Shadow Punch", "Fantasma"), ("Curse", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Protect", "Normal")]),
        mon("banette", 49, [("Shadow Ball", "Fantasma"), ("Skill Swap", "Psíquico"), ("Thunderbolt", "Eléctrico"), ("Psychic", "Psíquico")]),
        mon("sableye", 50, [("Shadow Ball", "Fantasma"), ("Fake Out", "Normal"), ("Attract", "Normal"), ("Faint Attack", "Siniestro")]),
        mon("dusclops", 51, [("Shadow Punch", "Fantasma"), ("Curse", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Ice Beam", "Hielo")]),
        mon("banette", 49, [("Shadow Ball", "Fantasma"), ("Grudge", "Fantasma"), ("Will-O-Wisp", "Fuego"), ("Faint Attack", "Siniestro")]),
    ),
    "Glacia": team(
        mon("sealeo", 50, [("Ice Ball", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo"), ("Rest", "Psíquico")]),
        mon("sealeo", 52, [("Ice Ball", "Hielo"), ("Body Slam", "Normal"), ("Hail", "Hielo"), ("Rest", "Psíquico")]),
        mon("glalie", 50, [("Ice Beam", "Hielo"), ("Light Screen", "Psíquico"), ("Crunch", "Siniestro"), ("Hail", "Hielo")]),
        mon("glalie", 52, [("Ice Beam", "Hielo"), ("Crunch", "Siniestro"), ("Light Screen", "Psíquico"), ("Hail", "Hielo")]),
        mon("walrein", 53, [("Surf", "Agua"), ("Body Slam", "Normal"), ("Ice Beam", "Hielo"), ("Sheer Cold", "Hielo")]),
    ),
    "Drake": team(
        mon("shelgon", 52, [("Rock Tomb", "Roca"), ("DragonBreath", "Dragón"), ("Protect", "Normal"), ("Scary Face", "Normal")]),
        mon("altaria", 54, [("DragonDance", "Dragón"), ("Earthquake", "Tierra"), ("DragonBreath", "Dragón"), ("Aerial Ace", "Volador")]),
        mon("flygon", 53, [("Flamethrower", "Fuego"), ("DragonBreath", "Dragón"), ("Crunch", "Siniestro"), ("Fly", "Volador")]),
        mon("flygon", 53, [("Earthquake", "Tierra"), ("Sandstorm", "Roca"), ("DragonBreath", "Dragón"), ("Fly", "Volador")]),
        mon("salamence", 55, [("Dragon Claw", "Dragón"), ("Flamethrower", "Fuego"), ("Fly", "Volador"), ("Crunch", "Siniestro")]),
    ),
    "Wallace": team(
        mon("wailord", 57, [("Water Spout", "Agua"), ("Amnesia", "Psíquico"), ("Rest", "Psíquico"), ("Body Slam", "Normal")]),
        mon("tentacruel", 55, [("Sludge Bomb", "Veneno"), ("Toxic", "Veneno"), ("Barrier", "Psíquico"), ("Surf", "Agua")]),
        mon("ludicolo", 56, [("Giga Drain", "Planta"), ("Surf", "Agua"), ("Rain Dance", "Agua"), ("Leech Seed", "Planta")]),
        mon("whiscash", 56, [("Earthquake", "Tierra"), ("Water Pulse", "Agua"), ("Amnesia", "Psíquico"), ("Rain Dance", "Agua")]),
        mon("gyarados", 56, [("Dragon Dance", "Dragón"), ("Earthquake", "Tierra"), ("Hydro Pump", "Agua"), ("Hyper Beam", "Normal")]),
        mon("milotic", 58, [("Recover", "Normal"), ("Surf", "Agua"), ("Ice Beam", "Hielo"), ("Attract", "Normal")]),
    ),
}

UPDATE_NAMES = set(EMERALD_TEAMS.keys())


def apply_team(trainer: dict, new_team: list[dict]) -> None:
    trainer["team"] = new_team


def main():
    with open(DB_PATH, encoding="utf-8") as f:
        db = json.load(f)

    updated = []
    for tr in db["trainers"]["emerald"]:
        if tr["name"] in UPDATE_NAMES:
            apply_team(tr, EMERALD_TEAMS[tr["name"]])
            updated.append(tr["name"])

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Actualizados:", ", ".join(updated))


if __name__ == "__main__":
    main()
