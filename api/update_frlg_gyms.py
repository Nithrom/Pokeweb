#!/usr/bin/env python3
"""Actualiza equipos Rojo Fuego / Verde Hoja desde datos curados."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "trainers_db.json")

MOVE_SLUG = {
    "sonicboom": "sonic-boom",
    "selfdestruct": "self-destruct",
    "defense curl": "defense-curl",
    "rock throw": "rock-throw",
    "water gun": "water-gun",
    "rapid spin": "rapid-spin",
    "thunderbolt": "thunderbolt",
    "thunder wave": "thunder-wave",
    "quick attack": "quick-attack",
    "double team": "double-team",
    "light screen": "light-screen",
    "razor leaf": "razor-leaf",
    "sleep powder": "sleep-powder",
    "sweet scent": "sweet-scent",
    "mega drain": "mega-drain",
    "stun spore": "stun-spore",
    "petal dance": "petal-dance",
    "smokescreen": "smoke-screen",
    "sludge bomb": "sludge-bomb",
    "acid armor": "acid-armor",
    "fire spin": "fire-spin",
    "fire blast": "fire-blast",
    "fury attack": "fury-attack",
    "extremespeed": "extreme-speed",
    "extreme speed": "extreme-speed",
    "calm mind": "calm-mind",
    "future sight": "future-sight",
    "scary face": "scary-face",
    "horn attack": "horn-attack",
    "sand attack": "sand-attack",
    "double kick": "double-kick",
    "megahorn": "megahorn",
    "ice beam": "ice-beam",
    "aurora beam": "aurora-beam",
    "spike cannon": "spike-cannon",
    "slack off": "slack-off",
    "lovely kiss": "lovely-kiss",
    "ice punch": "ice-punch",
    "double slap": "double-slap",
    "doubleslap": "double-slap",
    "thunderpunch": "thunder-punch",
    "fire punch": "fire-punch",
    "high jump kick": "high-jump-kick",
    "hi jump kick": "high-jump-kick",
    "focus energy": "focus-energy",
    "mega kick": "mega-kick",
    "cross chop": "cross-chop",
    "bulk up": "bulk-up",
    "rock slide": "rock-slide",
    "shadow ball": "shadow-ball",
    "dream eater": "dream-eater",
    "mean look": "mean-look",
    "poison fang": "poison-fang",
    "leech life": "leech-life",
    "wing attack": "wing-attack",
    "dragon dance": "dragon-dance",
    "dragon claw": "dragon-claw",
    "hydro pump": "hydro-pump",
    "hyper beam": "hyper-beam",
    "solarbeam": "solar-beam",
    "solar beam": "solar-beam",
    "giga drain": "giga-drain",
    "mirror move": "mirror-move",
    "sandstorm": "sandstorm",
    "horn drill": "horn-drill",
}

POKE_TYPES = {
    "geodude": ["rock", "ground"],
    "onix": ["rock", "ground"],
    "staryu": ["water"],
    "starmie": ["water", "psychic"],
    "voltorb": ["electric"],
    "pikachu": ["electric"],
    "raichu": ["electric"],
    "victreebel": ["grass", "poison"],
    "tangela": ["grass"],
    "vileplume": ["grass", "poison"],
    "koffing": ["poison"],
    "muk": ["poison"],
    "weezing": ["poison"],
    "growlithe": ["fire"],
    "ponyta": ["fire"],
    "rapidash": ["fire"],
    "arcanine": ["fire"],
    "mr-mime": ["psychic", "fairy"],
    "kadabra": ["psychic"],
    "alakazam": ["psychic"],
    "rhyhorn": ["ground", "rock"],
    "dugtrio": ["ground"],
    "nidoqueen": ["poison", "ground"],
    "nidoking": ["poison", "ground"],
    "dewgong": ["water", "ice"],
    "cloyster": ["water", "ice"],
    "slowbro": ["water", "psychic"],
    "jynx": ["ice", "psychic"],
    "lapras": ["water", "ice"],
    "hitmonchan": ["fighting"],
    "hitmonlee": ["fighting"],
    "machamp": ["fighting"],
    "gengar": ["ghost", "poison"],
    "golbat": ["poison", "flying"],
    "haunter": ["ghost", "poison"],
    "arbok": ["poison"],
    "gyarados": ["water", "flying"],
    "dragonair": ["dragon"],
    "aerodactyl": ["rock", "flying"],
    "dragonite": ["dragon", "flying"],
    "pidgeot": ["normal", "flying"],
    "rhydon": ["ground", "rock"],
    "exeggutor": ["grass", "psychic"],
}


def slug_move(name: str) -> str:
    key = name.strip().lower()
    if key in MOVE_SLUG:
        return MOVE_SLUG[key]
    key2 = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return MOVE_SLUG.get(key2, key2)


def mon(name: str, level: int, moves: list[tuple[str, str]]) -> dict:
    return {
        "name": name,
        "name_display": name.replace("-", " ").title(),
        "level": level,
        "types": POKE_TYPES.get(name, ["normal"]),
        "moves": [{"name": slug_move(d), "name_display": d} for d, _ in moves],
    }


def team(*mons) -> list:
    return list(mons)


FRLG_TEAMS = {
    "Brock": team(
        mon("geodude", 12, [("Tackle", "Normal"), ("Defense Curl", "Normal")]),
        mon("geodude", 12, [("Tackle", "Normal"), ("Defense Curl", "Normal")]),
        mon("onix", 14, [("Rock Throw", "Roca"), ("Bind", "Normal"), ("Harden", "Normal"), ("Screech", "Normal")]),
    ),
    "Misty": team(
        mon("staryu", 18, [("Tackle", "Normal"), ("Water Gun", "Agua"), ("Rapid Spin", "Normal")]),
        mon("starmie", 21, [("Tackle", "Normal"), ("Water Gun", "Agua"), ("Swift", "Normal"), ("Recover", "Normal")]),
    ),
    "Lt. Surge": team(
        mon("voltorb", 21, [("SonicBoom", "Normal"), ("Selfdestruct", "Normal"), ("Swift", "Normal"), ("Light Screen", "Psíquico")]),
        mon("pikachu", 18, [("Thunderbolt", "Eléctrico"), ("Quick Attack", "Normal"), ("Double Team", "Normal"), ("Thunder Wave", "Eléctrico")]),
        mon("raichu", 24, [("Thunderbolt", "Eléctrico"), ("Thunder Wave", "Eléctrico"), ("Quick Attack", "Normal"), ("Double Team", "Normal")]),
    ),
    "Erika": team(
        mon("victreebel", 29, [("Razor Leaf", "Planta"), ("Sleep Powder", "Planta"), ("Acid", "Veneno"), ("Sweet Scent", "Normal")]),
        mon("tangela", 24, [("Constrict", "Normal"), ("Sleep Powder", "Planta"), ("Bind", "Normal"), ("Mega Drain", "Planta")]),
        mon("vileplume", 29, [("Acid", "Veneno"), ("Stun Spore", "Planta"), ("Petal Dance", "Planta"), ("Sleep Powder", "Planta")]),
    ),
    "Koga": team(
        mon("koffing", 37, [("Smokescreen", "Normal"), ("Sludge", "Veneno"), ("Selfdestruct", "Normal"), ("Toxic", "Veneno")]),
        mon("muk", 39, [("Minimize", "Normal"), ("Sludge", "Veneno"), ("Toxic", "Veneno"), ("Acid Armor", "Veneno")]),
        mon("koffing", 37, [("Smokescreen", "Normal"), ("Sludge", "Veneno"), ("Selfdestruct", "Normal"), ("Toxic", "Veneno")]),
        mon("weezing", 43, [("Sludge Bomb", "Veneno"), ("Toxic", "Veneno"), ("Smokescreen", "Normal"), ("Explosion", "Normal")]),
    ),
    "Blaine": team(
        mon("growlithe", 42, [("Flamethrower", "Fuego"), ("Agility", "Psíquico"), ("Take Down", "Normal"), ("Roar", "Normal")]),
        mon("ponyta", 40, [("Fire Spin", "Fuego"), ("Stomp", "Normal"), ("Agility", "Psíquico"), ("Fury Attack", "Normal")]),
        mon("rapidash", 42, [("Fire Blast", "Fuego"), ("Stomp", "Normal"), ("Agility", "Psíquico"), ("Bounce", "Volador")]),
        mon("arcanine", 47, [("ExtremeSpeed", "Normal"), ("Flamethrower", "Fuego"), ("Roar", "Normal"), ("Take Down", "Normal")]),
    ),
    "Sabrina": team(
        mon("mr-mime", 38, [("Psychic", "Psíquico"), ("Reflect", "Psíquico"), ("Light Screen", "Psíquico"), ("Barrier", "Psíquico")]),
        mon("kadabra", 38, [("Psychic", "Psíquico"), ("Recover", "Normal"), ("Reflect", "Psíquico"), ("Disable", "Normal")]),
        mon("alakazam", 43, [("Psychic", "Psíquico"), ("Recover", "Normal"), ("Calm Mind", "Psíquico"), ("Future Sight", "Psíquico")]),
    ),
    "Giovanni": team(
        mon("rhyhorn", 45, [("Earthquake", "Tierra"), ("Fury Attack", "Normal"), ("Scary Face", "Normal"), ("Horn Attack", "Normal")]),
        mon("dugtrio", 42, [("Dig", "Tierra"), ("Sand Attack", "Tierra"), ("Slash", "Normal"), ("Earthquake", "Tierra")]),
        mon("nidoqueen", 44, [("Earthquake", "Tierra"), ("Body Slam", "Normal"), ("Toxic", "Veneno"), ("Double Kick", "Lucha")]),
        mon("nidoking", 45, [("Earthquake", "Tierra"), ("Megahorn", "Bicho"), ("Thunderbolt", "Eléctrico"), ("Flamethrower", "Fuego")]),
    ),
    "Lorelei": team(
        mon("dewgong", 52, [("Ice Beam", "Hielo"), ("Surf", "Agua"), ("Rest", "Psíquico"), ("Aurora Beam", "Hielo")]),
        mon("cloyster", 51, [("Ice Beam", "Hielo"), ("Spike Cannon", "Normal"), ("Protect", "Normal"), ("Clamp", "Agua")]),
        mon("slowbro", 52, [("Psychic", "Psíquico"), ("Surf", "Agua"), ("Amnesia", "Psíquico"), ("Slack Off", "Normal")]),
        mon("jynx", 54, [("Lovely Kiss", "Normal"), ("Ice Punch", "Hielo"), ("Psychic", "Psíquico"), ("Double Slap", "Normal")]),
        mon("lapras", 56, [("Ice Beam", "Hielo"), ("Surf", "Agua"), ("Thunderbolt", "Eléctrico"), ("Psychic", "Psíquico")]),
    ),
    "Bruno": team(
        mon("onix", 51, [("Rock Slide", "Roca"), ("Earthquake", "Tierra"), ("Sandstorm", "Roca"), ("Screech", "Normal")]),
        mon("hitmonchan", 53, [("ThunderPunch", "Eléctrico"), ("Ice Punch", "Hielo"), ("Fire Punch", "Fuego"), ("Counter", "Lucha")]),
        mon("hitmonlee", 53, [("High Jump Kick", "Lucha"), ("Double Kick", "Lucha"), ("Focus Energy", "Normal"), ("Mega Kick", "Normal")]),
        mon("machamp", 56, [("Rock Slide", "Roca"), ("Earthquake", "Tierra"), ("Cross Chop", "Lucha"), ("Bulk Up", "Lucha")]),
    ),
    "Agatha": team(
        mon("gengar", 54, [("Shadow Ball", "Fantasma"), ("Hypnosis", "Psíquico"), ("Dream Eater", "Psíquico"), ("Curse", "Fantasma")]),
        mon("golbat", 54, [("Confuse Ray", "Fantasma"), ("Wing Attack", "Volador"), ("Poison Fang", "Veneno"), ("Leech Life", "Bicho")]),
        mon("haunter", 53, [("Shadow Ball", "Fantasma"), ("Hypnosis", "Psíquico"), ("Mean Look", "Normal"), ("Curse", "Fantasma")]),
        mon("arbok", 56, [("Glare", "Normal"), ("Crunch", "Siniestro"), ("Earthquake", "Tierra"), ("Screech", "Normal")]),
    ),
    "Lance": team(
        mon("gyarados", 58, [("Hyper Beam", "Normal"), ("Surf", "Agua"), ("Dragon Dance", "Dragón"), ("Earthquake", "Tierra")]),
        mon("dragonair", 56, [("Thunder Wave", "Eléctrico"), ("Dragon Dance", "Dragón"), ("Surf", "Agua"), ("Ice Beam", "Hielo")]),
        mon("dragonair", 56, [("Thunder Wave", "Eléctrico"), ("Dragon Dance", "Dragón"), ("Thunderbolt", "Eléctrico"), ("Flamethrower", "Fuego")]),
        mon("aerodactyl", 58, [("Rock Slide", "Roca"), ("Wing Attack", "Volador"), ("Earthquake", "Tierra"), ("Hyper Beam", "Normal")]),
        mon("dragonite", 60, [("Dragon Claw", "Dragón"), ("Fire Blast", "Fuego"), ("Blizzard", "Hielo"), ("Thunder", "Eléctrico")]),
    ),
    "Blue": team(
        mon("pidgeot", 59, [("Wing Attack", "Volador"), ("Quick Attack", "Normal"), ("Whirlwind", "Normal"), ("Mirror Move", "Volador")]),
        mon("alakazam", 57, [("Psychic", "Psíquico"), ("Recover", "Normal"), ("Calm Mind", "Psíquico"), ("Future Sight", "Psíquico")]),
        mon("rhydon", 59, [("Earthquake", "Tierra"), ("Rock Slide", "Roca"), ("Horn Drill", "Normal"), ("Fury Attack", "Normal")]),
        mon("gyarados", 61, [("Hydro Pump", "Agua"), ("Dragon Dance", "Dragón"), ("Hyper Beam", "Normal"), ("Earthquake", "Tierra")]),
        mon("exeggutor", 59, [("SolarBeam", "Planta"), ("Psychic", "Psíquico"), ("Sleep Powder", "Planta"), ("Giga Drain", "Planta")]),
        mon("arcanine", 59, [("Flamethrower", "Fuego"), ("ExtremeSpeed", "Normal"), ("Take Down", "Normal"), ("Roar", "Normal")]),
    ),
}

UPDATE_NAMES = set(FRLG_TEAMS.keys())


def main():
    with open(DB_PATH, encoding="utf-8") as f:
        db = json.load(f)

    updated = []
    for tr in db["trainers"]["firered-leafgreen"]:
        if tr["name"] in UPDATE_NAMES:
            tr["team"] = FRLG_TEAMS[tr["name"]]
            updated.append(tr["name"])

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Actualizados:", ", ".join(updated))


if __name__ == "__main__":
    main()
