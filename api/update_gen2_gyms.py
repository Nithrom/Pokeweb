#!/usr/bin/env python3
"""Actualiza equipos Gen 2 (Oro/Plata + Cristal) desde datos curados."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "trainers_db.json")

MOVE_SLUG = {
    "doubleslap": "double-slap",
    "double slap": "double-slap",
    "dynamicpunch": "dynamic-punch",
    "sonicboom": "sonic-boom",
    "thundershock": "thunder-shock",
    "sand-attack": "sand-attack",
    "faint attack": "feint-attack",
    "curse": "curse",
    "hijumpkick": "high-jump-kick",
    "hi jump kick": "high-jump-kick",
    "thunderpunch": "thunder-punch",
    "ice punch": "ice-punch",
    "fire punch": "fire-punch",
    "dragonbreath": "dragon-breath",
    "smokescreen": "smoke-screen",
    "ancientpower": "ancient-power",
    "stringshot": "string-shot",
    "string shot": "string-shot",
    "mean look": "mean-look",
    "milk drink": "milk-drink",
    "icy wind": "icy-wind",
    "rain dance": "rain-dance",
    "sand attack": "sand-attack",
    "feint attack": "feint-attack",
    "shadow ball": "shadow-ball",
    "mind reader": "mind-reader",
    "sunny day": "sunny-day",
    "iron tail": "iron-tail",
    "sludge bomb": "sludge-bomb",
    "giga drain": "giga-drain",
    "baton pass": "baton-pass",
    "spider web": "spider-web",
    "future sight": "future-sight",
    "egg bomb": "egg-bomb",
    "rapid spin": "rapid-spin",
    "cross chop": "cross-chop",
    "vital throw": "vital-throw",
    "mach punch": "mach-punch",
    "rock slide": "rock-slide",
    "wing attack": "wing-attack",
    "hyper beam": "hyper-beam",
    "lovely kiss": "lovely-kiss",
    "night shade": "night-shade",
    "dream eater": "dream-eater",
    "leech seed": "leech-seed",
    "stun spore": "stun-spore",
    "petal dance": "petal-dance",
    "poison sting": "poison-sting",
    "fury cutter": "fury-cutter",
    "mud-slap": "mud-slap",
    "acid armor": "acid-armor",
    "destiny bond": "destiny-bond",
    "confuse ray": "confuse-ray",
    "light screen": "light-screen",
    "psych up": "psych-up",
    "perish song": "perish-song",
    "zap cannon": "zap-cannon",
    "lock-on": "lock-on",
    "lock on": "lock-on",
    "solarbeam": "solar-beam",
    "solar beam": "solar-beam",
    "extremespeed": "extreme-speed",
    "extreme speed": "extreme-speed",
    "selfdestruct": "self-destruct",
    "cotton spore": "cotton-spore",
    "scary face": "scary-face",
    "spike cannon": "spike-cannon",
    "defense curl": "defense-curl",
    "horn drill": "horn-drill",
    "sandstorm": "sandstorm",
    "amnesia": "amnesia",
    "disable": "disable",
    "foresight": "foresight",
    "protect": "protect",
    "endure": "endure",
    "synthesis": "synthesis",
    "razor leaf": "razor-leaf",
    "sleep powder": "sleep-powder",
    "fire spin": "fire-spin",
    "fire blast": "fire-blast",
    "flamethrower": "flamethrower",
    "hydro pump": "hydro-pump",
    "twister": "twister",
    "mirror move": "mirror-move",
    "egg bomb": "egg-bomb",
    "night shade": "night-shade",
    "smog": "smog",
    "toxic": "toxic",
    "surf": "surf",
    "blizzard": "blizzard",
    "earthquake": "earthquake",
    "explosion": "explosion",
    "rollout": "rollout",
    "headbutt": "headbutt",
    "barrier": "barrier",
    "reflect": "reflect",
    "recover": "recover",
    "psychic": "psychic",
    "swift": "swift",
    "roar": "roar",
    "slash": "slash",
    "bind": "bind",
    "acid": "acid",
    "vine whip": "vine-whip",
    "disable": "disable",
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
    "???": "ghost",
    "???*": "ghost",
}

POKE_TYPES = {
    "pidgey": ["normal", "flying"],
    "pidgeotto": ["normal", "flying"],
    "metapod": ["bug"],
    "kakuna": ["bug", "poison"],
    "scyther": ["bug", "flying"],
    "clefairy": ["fairy"],
    "miltank": ["normal"],
    "gastly": ["ghost", "poison"],
    "haunter": ["ghost", "poison"],
    "gengar": ["ghost", "poison"],
    "primeape": ["fighting"],
    "poliwrath": ["water", "fighting"],
    "magnemite": ["electric", "steel"],
    "steelix": ["steel", "ground"],
    "seel": ["water"],
    "dewgong": ["water", "ice"],
    "piloswine": ["ice", "ground"],
    "dragonair": ["dragon"],
    "kingdra": ["water", "dragon"],
    "xatu": ["psychic", "flying"],
    "jynx": ["ice", "psychic"],
    "slowbro": ["water", "psychic"],
    "exeggutor": ["grass", "psychic"],
    "ariados": ["bug", "poison"],
    "venomoth": ["bug", "poison"],
    "muk": ["poison"],
    "forretress": ["bug", "steel"],
    "crobat": ["poison", "flying"],
    "hitmontop": ["fighting"],
    "hitmonlee": ["fighting"],
    "hitmonchan": ["fighting"],
    "onix": ["rock", "ground"],
    "machamp": ["fighting"],
    "umbreon": ["dark"],
    "vileplume": ["grass", "poison"],
    "murkrow": ["dark", "flying"],
    "houndoom": ["dark", "fire"],
    "gyarados": ["water", "flying"],
    "dragonite": ["dragon", "flying"],
    "charizard": ["fire", "flying"],
    "aerodactyl": ["rock", "flying"],
    "raichu": ["electric"],
    "electrode": ["electric"],
    "electabuzz": ["electric"],
    "magneton": ["electric", "steel"],
    "espeon": ["psychic"],
    "mr-mime": ["psychic", "fairy"],
    "tangela": ["grass"],
    "jumpluff": ["grass", "flying"],
    "victreebel": ["grass", "poison"],
    "bellossom": ["grass"],
    "weezing": ["poison"],
    "golduck": ["water"],
    "quagsire": ["water", "ground"],
    "lapras": ["water", "ice"],
    "starmie": ["water", "psychic"],
    "graveler": ["rock", "ground"],
    "rhyhorn": ["ground", "rock"],
    "omastar": ["rock", "water"],
    "kabutops": ["rock", "water"],
    "magcargo": ["fire", "rock"],
    "magmar": ["fire"],
    "rapidash": ["fire"],
    "pidgeot": ["normal", "flying"],
    "rhydon": ["ground", "rock"],
    "arcanine": ["fire"],
    "alakazam": ["psychic"],
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


# (display, type_es) por movimiento
def T(s: str) -> tuple[str, str]:
    parts = s.rsplit(" ", 1)
    if len(parts) == 2 and parts[1].startswith("("):
        return parts[0].strip(), parts[1].strip("()")
    return s, "Normal"


def parse_moves(lines: list[str]) -> list[tuple[str, str]]:
    out = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("Pokémon") or "___" in line:
            continue
        if " Nv." in line or line.endswith(")"):
            continue
        if "(" in line and ")" in line:
            disp, typ = line.rsplit("(", 1)
            out.append((disp.strip(), typ.strip(")")))
        else:
            out.append((line, "Normal"))
    return out


GEN2_TEAMS = {
    "Falkner": team(
        mon("pidgey", 7, [("Tackle", "Normal"), ("Mud-Slap", "Tierra")]),
        mon("pidgeotto", 9, [("Tackle", "Normal"), ("Gust", "Volador"), ("Mud-Slap", "Tierra")]),
    ),
    "Bugsy": team(
        mon("metapod", 14, [("Tackle", "Normal"), ("String Shot", "Bicho"), ("Harden", "Normal")]),
        mon("kakuna", 14, [("Poison Sting", "Veneno"), ("String Shot", "Bicho"), ("Harden", "Normal")]),
        mon("scyther", 16, [("Quick Attack", "Normal"), ("Leer", "Normal"), ("Fury Cutter", "Bicho")]),
    ),
    "Whitney": team(
        mon("clefairy", 18, [("Encore", "Normal"), ("Mimic", "Normal"), ("DoubleSlap", "Normal"), ("Metronome", "Normal")]),
        mon("miltank", 20, [("Rollout", "Roca"), ("Stomp", "Normal"), ("Attract", "Normal"), ("Milk Drink", "Normal")]),
    ),
    "Morty": team(
        mon("gastly", 21, [("Lick", "Fantasma"), ("Spite", "Fantasma"), ("Mean Look", "Normal"), ("Curse", "???")]),
        mon("haunter", 21, [("Hypnosis", "Psíquico"), ("Mean Look", "Normal"), ("Curse", "???"), ("Night Shade", "Fantasma")]),
        mon("haunter", 23, [("Hypnosis", "Psíquico"), ("Mimic", "Normal"), ("Curse", "???"), ("Night Shade", "Fantasma")]),
        mon("gengar", 25, [("Hypnosis", "Psíquico"), ("Shadow Ball", "Fantasma"), ("Mean Look", "Normal"), ("Dream Eater", "Psíquico")]),
    ),
    "Chuck": team(
        mon("primeape", 27, [("Leer", "Normal"), ("Rage", "Normal"), ("Karate Chop", "Lucha"), ("Fury Swipes", "Normal")]),
        mon("poliwrath", 30, [("Hypnosis", "Psíquico"), ("Mind Reader", "Normal"), ("Surf", "Agua"), ("DynamicPunch", "Lucha")]),
    ),
    "Jasmine": team(
        mon("magnemite", 30, [("Tackle", "Normal"), ("Supersonic", "Normal"), ("SonicBoom", "Normal"), ("ThunderShock", "Eléctrico")]),
        mon("magnemite", 30, [("Tackle", "Normal"), ("Supersonic", "Normal"), ("SonicBoom", "Normal"), ("ThunderShock", "Eléctrico")]),
        mon("steelix", 35, [("Screech", "Normal"), ("Sunny Day", "Fuego"), ("Rock Throw", "Roca"), ("Iron Tail", "Acero")]),
    ),
    "Pryce": team(
        mon("seel", 27, [("Headbutt", "Normal"), ("Icy Wind", "Hielo"), ("Aurora Beam", "Hielo"), ("Rest", "Psíquico")]),
        mon("dewgong", 29, [("Headbutt", "Normal"), ("Icy Wind", "Hielo"), ("Aurora Beam", "Hielo"), ("Rest", "Psíquico")]),
        mon("piloswine", 31, [("Fury Attack", "Normal"), ("Mist", "Hielo"), ("Blizzard", "Hielo"), ("Icy Wind", "Hielo")]),
    ),
    "Clair": team(
        mon("dragonair", 37, [("Thunder Wave", "Eléctrico"), ("Surf", "Agua"), ("Slam", "Normal"), ("DragonBreath", "Dragón")]),
        mon("dragonair", 37, [("Thunder Wave", "Eléctrico"), ("Thunderbolt", "Eléctrico"), ("Slam", "Normal"), ("DragonBreath", "Dragón")]),
        mon("dragonair", 37, [("Thunder Wave", "Eléctrico"), ("Ice Beam", "Hielo"), ("Slam", "Normal"), ("DragonBreath", "Dragón")]),
        mon("kingdra", 40, [("Smoke Screen", "Normal"), ("Surf", "Agua"), ("Hyper Beam", "Normal"), ("DragonBreath", "Dragón")]),
    ),
    "Will": team(
        mon("xatu", 40, [("Psychic", "Psíquico"), ("Night Shade", "Fantasma"), ("Curse", "???"), ("Confuse Ray", "Fantasma")]),
        mon("jynx", 41, [("Lovely Kiss", "Normal"), ("Ice Punch", "Hielo"), ("Psychic", "Psíquico"), ("DoubleSlap", "Normal")]),
        mon("slowbro", 41, [("Curse", "???"), ("Amnesia", "Psíquico"), ("Psychic", "Psíquico"), ("Water Gun", "Agua")]),
        mon("exeggutor", 41, [("Reflect", "Psíquico"), ("Leech Seed", "Planta"), ("Egg Bomb", "Normal"), ("Psychic", "Psíquico")]),
        mon("xatu", 42, [("Psychic", "Psíquico"), ("Future Sight", "Psíquico"), ("Confuse Ray", "Fantasma"), ("Fly", "Volador")]),
    ),
    "Koga": team(
        mon("ariados", 40, [("Double Team", "Normal"), ("Spider Web", "Bicho"), ("Baton Pass", "Normal"), ("Giga Drain", "Planta")]),
        mon("venomoth", 41, [("Supersonic", "Normal"), ("Gust", "Volador"), ("Psychic", "Psíquico"), ("Toxic", "Veneno")]),
        mon("muk", 42, [("Minimize", "Normal"), ("Acid Armor", "Veneno"), ("Sludge Bomb", "Veneno"), ("Toxic", "Veneno")]),
        mon("forretress", 43, [("Protect", "Normal"), ("Swift", "Normal"), ("Explosion", "Normal"), ("Toxic", "Veneno")]),
        mon("crobat", 44, [("Double Team", "Normal"), ("Quick Attack", "Normal"), ("Wing Attack", "Volador"), ("Toxic", "Veneno")]),
    ),
    "Bruno": team(
        mon("hitmontop", 42, [("Dig", "Tierra"), ("Quick Attack", "Normal"), ("Rapid Spin", "Normal"), ("Detect", "Lucha")]),
        mon("hitmonlee", 42, [("Swagger", "Normal"), ("Double Kick", "Lucha"), ("Hi Jump Kick", "Lucha"), ("Foresight", "Normal")]),
        mon("hitmonchan", 42, [("ThunderPunch", "Eléctrico"), ("Ice Punch", "Hielo"), ("Fire Punch", "Fuego"), ("Mach Punch", "Lucha")]),
        mon("onix", 43, [("Sandstorm", "Roca"), ("Rock Slide", "Roca"), ("Slam", "Normal"), ("DragonBreath", "Dragón")]),
        mon("machamp", 46, [("Rock Slide", "Roca"), ("Foresight", "Normal"), ("Vital Throw", "Lucha"), ("Cross Chop", "Lucha")]),
    ),
    "Karen": team(
        mon("umbreon", 42, [("Sand-Attack", "Tierra"), ("Confuse Ray", "Fantasma"), ("Mean Look", "Normal"), ("Faint Attack", "Siniestro")]),
        mon("vileplume", 42, [("Stun Spore", "Planta"), ("Acid", "Veneno"), ("Moonlight", "Normal"), ("Petal Dance", "Planta")]),
        mon("murkrow", 44, [("Quick Attack", "Normal"), ("Whirlwind", "Normal"), ("Pursuit", "Siniestro"), ("Faint Attack", "Siniestro")]),
        mon("gengar", 45, [("Lick", "Fantasma"), ("Spite", "Fantasma"), ("Curse", "???"), ("Destiny Bond", "Fantasma")]),
        mon("houndoom", 47, [("Roar", "Normal"), ("Pursuit", "Siniestro"), ("Flamethrower", "Fuego"), ("Crunch", "Siniestro")]),
    ),
    "Lance": team(
        mon("gyarados", 44, [("Flail", "Normal"), ("Rain Dance", "Agua"), ("Surf", "Agua"), ("Hyper Beam", "Normal")]),
        mon("dragonite", 47, [("Thunder Wave", "Eléctrico"), ("Twister", "Dragón"), ("Thunder", "Eléctrico"), ("Hyper Beam", "Normal")]),
        mon("charizard", 46, [("Flamethrower", "Fuego"), ("Wing Attack", "Volador"), ("Slash", "Normal"), ("Hyper Beam", "Normal")]),
        mon("aerodactyl", 46, [("Wing Attack", "Volador"), ("AncientPower", "Roca"), ("Rock Slide", "Roca"), ("Hyper Beam", "Normal")]),
        mon("dragonite", 47, [("Thunder Wave", "Eléctrico"), ("Twister", "Dragón"), ("Blizzard", "Hielo"), ("Hyper Beam", "Normal")]),
        mon("dragonite", 50, [("Fire Blast", "Fuego"), ("Safeguard", "Normal"), ("Outrage", "Dragón"), ("Hyper Beam", "Normal")]),
    ),
    # Revancha Kanto en Johto (Oro/Plata / Cristal)
    "Lt. Surge": team(
        mon("raichu", 44, [("Thunder Wave", "Eléctrico"), ("Quick Attack", "Normal"), ("Thunderbolt", "Eléctrico"), ("Thunder", "Eléctrico")]),
        mon("electrode", 40, [("Screech", "Normal"), ("SonicBoom", "Normal"), ("Rollout", "Roca"), ("Light Screen", "Psíquico")]),
        mon("magneton", 40, [("Lock-On", "Normal"), ("Swift", "Normal"), ("Screech", "Normal"), ("Zap Cannon", "Eléctrico")]),
        mon("electabuzz", 46, [("Quick Attack", "Normal"), ("ThunderPunch", "Eléctrico"), ("Light Screen", "Psíquico"), ("Thunder", "Eléctrico")]),
    ),
    "Sabrina": team(
        mon("espeon", 46, [("Sand-Attack", "Tierra"), ("Quick Attack", "Normal"), ("Swift", "Normal"), ("Psychic", "Psíquico")]),
        mon("mr-mime", 46, [("Barrier", "Psíquico"), ("Reflect", "Psíquico"), ("Baton Pass", "Normal"), ("Psychic", "Psíquico")]),
        mon("alakazam", 48, [("Recover", "Normal"), ("Future Sight", "Psíquico"), ("Psychic", "Psíquico"), ("Reflect", "Psíquico")]),
    ),
    "Erika": team(
        mon("tangela", 42, [("Vine Whip", "Planta"), ("Bind", "Normal"), ("Giga Drain", "Planta"), ("Sleep Powder", "Planta")]),
        mon("jumpluff", 41, [("Mega Drain", "Planta"), ("Leech Seed", "Planta"), ("Cotton Spore", "Planta"), ("Giga Drain", "Planta")]),
        mon("victreebel", 46, [("Sunny Day", "Fuego"), ("Synthesis", "Planta"), ("Acid", "Veneno"), ("Razor Leaf", "Planta")]),
        mon("bellossom", 46, [("Sunny Day", "Fuego"), ("Synthesis", "Planta"), ("Petal Dance", "Planta"), ("SolarBeam", "Planta")]),
    ),
    "Janine": team(
        mon("crobat", 36, [("Screech", "Normal"), ("Supersonic", "Normal"), ("Wing Attack", "Volador"), ("Toxic", "Veneno")]),
        mon("weezing", 36, [("Smog", "Veneno"), ("Sludge Bomb", "Veneno"), ("Smokescreen", "Normal"), ("Toxic", "Veneno")]),
        mon("weezing", 36, [("Smog", "Veneno"), ("Sludge Bomb", "Veneno"), ("Smokescreen", "Normal"), ("Toxic", "Veneno")]),
        mon("ariados", 33, [("Spider Web", "Bicho"), ("Double Team", "Normal"), ("Giga Drain", "Planta"), ("Night Shade", "Fantasma")]),
        mon("venomoth", 39, [("Foresight", "Normal"), ("Gust", "Volador"), ("Psychic", "Psíquico"), ("Toxic", "Veneno")]),
    ),
    "Misty": team(
        mon("golduck", 42, [("Surf", "Agua"), ("Disable", "Normal"), ("Psych Up", "Normal"), ("Psychic", "Psíquico")]),
        mon("quagsire", 42, [("Surf", "Agua"), ("Amnesia", "Psíquico"), ("Earthquake", "Tierra"), ("Rain Dance", "Agua")]),
        mon("lapras", 44, [("Surf", "Agua"), ("Perish Song", "Normal"), ("Blizzard", "Hielo"), ("Rain Dance", "Agua")]),
        mon("starmie", 47, [("Surf", "Agua"), ("Recover", "Normal"), ("Confuse Ray", "Fantasma"), ("Psychic", "Psíquico")]),
    ),
    "Brock": team(
        mon("graveler", 41, [("Defense Curl", "Normal"), ("Rollout", "Roca"), ("Earthquake", "Tierra"), ("Selfdestruct", "Normal")]),
        mon("rhyhorn", 41, [("Fury Attack", "Normal"), ("Scary Face", "Normal"), ("Earthquake", "Tierra"), ("Horn Drill", "Normal")]),
        mon("omastar", 42, [("Surf", "Agua"), ("Protect", "Normal"), ("Rain Dance", "Agua"), ("Spike Cannon", "Normal")]),
        mon("onix", 44, [("Sandstorm", "Roca"), ("Slam", "Normal"), ("Rock Slide", "Roca"), ("DragonBreath", "Dragón")]),
        mon("kabutops", 42, [("Slash", "Normal"), ("Surf", "Agua"), ("Endure", "Normal"), ("Giga Drain", "Planta")]),
    ),
    "Blaine": team(
        mon("magcargo", 45, [("Sunny Day", "Fuego"), ("Smog", "Veneno"), ("Flamethrower", "Fuego"), ("Rock Slide", "Roca")]),
        mon("magmar", 45, [("ThunderPunch", "Eléctrico"), ("Fire Punch", "Fuego"), ("Sunny Day", "Fuego"), ("Confuse Ray", "Fantasma")]),
        mon("rapidash", 50, [("Quick Attack", "Normal"), ("Fire Spin", "Fuego"), ("Fury Attack", "Normal"), ("Fire Blast", "Fuego")]),
    ),
    "Blue": team(
        mon("pidgeot", 56, [("Quick Attack", "Normal"), ("Whirlwind", "Normal"), ("Wing Attack", "Volador"), ("Mirror Move", "Volador")]),
        mon("alakazam", 54, [("Recover", "Normal"), ("Psychic", "Psíquico"), ("Reflect", "Psíquico"), ("Future Sight", "Psíquico")]),
        mon("rhydon", 56, [("Fury Attack", "Normal"), ("Sandstorm", "Roca"), ("Earthquake", "Tierra"), ("Horn Drill", "Normal")]),
        mon("gyarados", 58, [("Twister", "Dragón"), ("Hydro Pump", "Agua"), ("Rain Dance", "Agua"), ("Hyper Beam", "Normal")]),
        mon("exeggutor", 58, [("Sunny Day", "Fuego"), ("Leech Seed", "Planta"), ("Egg Bomb", "Normal"), ("SolarBeam", "Planta")]),
        mon("arcanine", 58, [("Roar", "Normal"), ("Swift", "Normal"), ("Flamethrower", "Fuego"), ("ExtremeSpeed", "Normal")]),
    ),
}

UPDATE_NAMES = set(GEN2_TEAMS.keys())


def strip_move_type(moves: list[dict]) -> list[dict]:
    """Quita move_type auxiliar del script."""
    out = []
    for mv in moves:
        entry = {"name": mv["name"], "name_display": mv["name_display"]}
        out.append(entry)
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
    for slug in ("gold-silver", "crystal"):
        for tr in db["trainers"][slug]:
            if tr["name"] in UPDATE_NAMES:
                apply_team(tr, GEN2_TEAMS[tr["name"]])
                updated.append(f"{slug}/{tr['name']}")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Actualizados:", ", ".join(updated))


if __name__ == "__main__":
    main()
