#!/usr/bin/env python3
"""Actualiza líderes Sinnoh (Diamante/Perla y Platino) desde datos curados."""
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT, "data", "trainers_db.json")

MOVE_SLUG = {
    "defense curl": "defense-curl",
    "rock throw": "rock-throw",
    "rock tomb": "rock-tomb",
    "leech seed": "leech-seed",
    "razor leaf": "razor-leaf",
    "poison sting": "poison-sting",
    "stun spore": "stun-spore",
    "magical leaf": "magical-leaf",
    "grass knot": "grass-knot",
    "shadow sneak": "shadow-sneak",
    "confuse ray": "confuse-ray",
    "night shade": "night-shade",
    "will-o-wisp": "will-o-wisp",
    "dream eater": "dream-eater",
    "shadow ball": "shadow-ball",
    "mean look": "mean-look",
    "force palm": "force-palm",
    "hidden power": "hidden-power",
    "karate chop": "karate-chop",
    "seismic toss": "seismic-toss",
    "focus energy": "focus-energy",
    "aura sphere": "aura-sphere",
    "metal claw": "metal-claw",
    "dragon rage": "dragon-rage",
    "mud shot": "mud-shot",
    "aqua jet": "aqua-jet",
    "water pulse": "water-pulse",
    "water gun": "water-gun",
    "payback": "payback",
    "astonish": "astonish",
    "shadow claw": "shadow-claw",
    "gyro ball": "gyro-ball",
    "iron tail": "iron-tail",
    "iron defense": "iron-defense",
    "ancientpower": "ancient-power",
    "ice punch": "ice-punch",
    "faint attack": "feint-attack",
    "feint attack": "feint-attack",
    "ice shard": "ice-shard",
    "wood hammer": "wood-hammer",
    "faint attack": "feint-attack",
    "double hit": "double-hit",
    "thunder fang": "thunder-fang",
    "ice fang": "ice-fang",
    "fire fang": "fire-fang",
    "bullet seed": "bullet-seed",
    "bug buzz": "bug-buzz",
    "air slash": "air-slash",
    "night slash": "night-slash",
    "attack order": "attack-order",
    "defend order": "defend-order",
    "heal order": "heal-order",
    "close combat": "close-combat",
    "poison fang": "poison-fang",
    "aqua tail": "aqua-tail",
    "hammer arm": "hammer-arm",
    "sucker punch": "sucker-punch",
    "low kick": "low-kick",
    "rock polish": "rock-polish",
    "stone edge": "stone-edge",
    "flare blitz": "flare-blitz",
    "poison jab": "poison-jab",
    "ominous wind": "ominous-wind",
    "energy ball": "energy-ball",
    "dark pulse": "dark-pulse",
    "silver wind": "silver-wind",
    "toxic spikes": "toxic-spikes",
    "dragon pulse": "dragon-pulse",
    "extreme speed": "extreme-speed",
    "mirror coat": "mirror-coat",
    "air cutter": "air-cutter",
    "baton pass": "baton-pass",
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
    "onix": ["rock", "ground"],
    "cranidos": ["rock"],
    "cherubi": ["grass"],
    "turtwig": ["grass"],
    "roserade": ["grass", "poison"],
    "duskull": ["ghost"],
    "haunter": ["ghost", "poison"],
    "mismagius": ["ghost"],
    "meditite": ["fighting", "psychic"],
    "machoke": ["fighting"],
    "lucario": ["fighting", "steel"],
    "gyarados": ["water", "flying"],
    "quagsire": ["water", "ground"],
    "floatzel": ["water"],
    "drifloon": ["ghost", "flying"],
    "bronzor": ["steel", "psychic"],
    "steelix": ["steel", "ground"],
    "bastiodon": ["rock", "steel"],
    "sneasel": ["dark", "ice"],
    "piloswine": ["ice", "ground"],
    "abomasnow": ["grass", "ice"],
    "ambipom": ["normal"],
    "raichu": ["electric"],
    "octillery": ["water"],
    "luxray": ["electric"],
    "yanmega": ["bug", "flying"],
    "beautifly": ["bug", "flying"],
    "vespiquen": ["bug", "flying"],
    "heracross": ["bug", "fighting"],
    "drapion": ["poison", "dark"],
    "sudowoodo": ["rock"],
    "hippowdon": ["ground"],
    "golem": ["rock", "ground"],
    "houndoom": ["dark", "fire"],
    "flareon": ["fire"],
    "infernape": ["fire", "fighting"],
    "drifblim": ["ghost", "flying"],
    "girafarig": ["normal", "psychic"],
    "spiritomb": ["ghost", "dark"],
    "togekiss": ["fairy", "flying"],
    "garchomp": ["dragon", "ground"],
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


DP_TEAMS = {
    "Roark": team(
        mon("geodude", 12, [("Tackle", "Normal"), ("Defense Curl", "Normal"), ("Rock Throw", "Roca")]),
        mon("onix", 12, [("Tackle", "Normal"), ("Harden", "Normal"), ("Rock Throw", "Roca"), ("Bind", "Normal")]),
        mon("cranidos", 14, [("Headbutt", "Normal"), ("Leer", "Normal"), ("Pursuit", "Siniestro"), ("Rock Tomb", "Roca")]),
    ),
    "Gardenia": team(
        mon("cherubi", 19, [("Tackle", "Normal"), ("Growth", "Planta"), ("Leech Seed", "Planta")]),
        mon("turtwig", 19, [("Razor Leaf", "Planta"), ("Withdraw", "Agua"), ("Bite", "Siniestro"), ("Curse", "Fantasma")]),
        mon("roserade", 22, [("Magical Leaf", "Planta"), ("Poison Sting", "Veneno"), ("Stun Spore", "Planta"), ("Grass Knot", "Planta")]),
    ),
    "Fantina": team(
        mon("duskull", 24, [("Shadow Sneak", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Night Shade", "Fantasma"), ("Will-O-Wisp", "Fuego")]),
        mon("haunter", 24, [("Hypnosis", "Psíquico"), ("Dream Eater", "Psíquico"), ("Shadow Ball", "Fantasma"), ("Mean Look", "Normal")]),
        mon("mismagius", 26, [("Psybeam", "Psíquico"), ("Shadow Ball", "Fantasma"), ("Confuse Ray", "Fantasma"), ("Magical Leaf", "Planta")]),
    ),
    "Maylene": team(
        mon("meditite", 27, [("Force Palm", "Lucha"), ("Confusion", "Psíquico"), ("Detect", "Lucha"), ("Hidden Power", "Variable")]),
        mon("machoke", 27, [("Karate Chop", "Lucha"), ("Foresight", "Normal"), ("Seismic Toss", "Lucha"), ("Focus Energy", "Normal")]),
        mon("lucario", 30, [("Aura Sphere", "Lucha"), ("Force Palm", "Lucha"), ("Metal Claw", "Acero"), ("Counter", "Lucha")]),
    ),
    "Crasher Wake": team(
        mon("gyarados", 27, [("Bite", "Siniestro"), ("Dragon Rage", "Dragón"), ("Twister", "Dragón"), ("Leer", "Normal")]),
        mon("quagsire", 27, [("Water Gun", "Agua"), ("Mud Shot", "Tierra"), ("Slam", "Normal"), ("Amnesia", "Psíquico")]),
        mon("floatzel", 30, [("Aqua Jet", "Agua"), ("Crunch", "Siniestro"), ("Swift", "Normal"), ("Water Pulse", "Agua")]),
    ),
    "Byron": team(
        mon("bronzor", 36, [("Confuse Ray", "Fantasma"), ("Hypnosis", "Psíquico"), ("Gyro Ball", "Acero"), ("Safeguard", "Normal")]),
        mon("steelix", 36, [("Iron Tail", "Acero"), ("Screech", "Normal"), ("Earthquake", "Tierra"), ("Crunch", "Siniestro")]),
        mon("bastiodon", 39, [("Iron Defense", "Acero"), ("Take Down", "Normal"), ("Protect", "Normal"), ("AncientPower", "Roca")]),
    ),
    "Candice": team(
        mon("sneasel", 38, [("Ice Punch", "Hielo"), ("Faint Attack", "Siniestro"), ("Quick Attack", "Normal"), ("Metal Claw", "Acero")]),
        mon("piloswine", 38, [("Ice Shard", "Hielo"), ("Earthquake", "Tierra"), ("AncientPower", "Roca"), ("Amnesia", "Psíquico")]),
        mon("abomasnow", 42, [("Ice Beam", "Hielo"), ("Wood Hammer", "Planta"), ("Blizzard", "Hielo"), ("Grass Knot", "Planta")]),
    ),
    "Volkner": team(
        mon("ambipom", 46, [("Swift", "Normal"), ("Agility", "Psíquico"), ("Shock Wave", "Eléctrico"), ("Double Hit", "Normal")]),
        mon("raichu", 46, [("Thunderbolt", "Eléctrico"), ("Light Screen", "Psíquico"), ("Thunder Wave", "Eléctrico"), ("Quick Attack", "Normal")]),
        mon("octillery", 47, [("Water Pulse", "Agua"), ("Ice Beam", "Hielo"), ("Bullet Seed", "Planta"), ("Flamethrower", "Fuego")]),
        mon("luxray", 49, [("Thunder Fang", "Eléctrico"), ("Crunch", "Siniestro"), ("Ice Fang", "Hielo"), ("Fire Fang", "Fuego")]),
    ),
    "Aaron": team(
        mon("yanmega", 53, [("Bug Buzz", "Bicho"), ("Air Slash", "Volador"), ("Double Team", "Normal"), ("Night Slash", "Siniestro")]),
        mon("beautifly", 53, [("Air Cutter", "Volador"), ("Giga Drain", "Planta"), ("Stun Spore", "Planta"), ("Whirlwind", "Normal")]),
        mon("vespiquen", 54, [("Attack Order", "Bicho"), ("Defend Order", "Bicho"), ("Heal Order", "Bicho"), ("Toxic", "Veneno")]),
        mon("heracross", 54, [("Megahorn", "Bicho"), ("Close Combat", "Lucha"), ("Night Slash", "Siniestro"), ("Earthquake", "Tierra")]),
        mon("drapion", 57, [("Crunch", "Siniestro"), ("Ice Fang", "Hielo"), ("Fire Fang", "Fuego"), ("Poison Fang", "Veneno")]),
    ),
    "Bertha": team(
        mon("quagsire", 55, [("Earthquake", "Tierra"), ("Surf", "Agua"), ("Amnesia", "Psíquico"), ("Recover", "Normal")]),
        mon("whiscash", 55, [("Earthquake", "Tierra"), ("Aqua Tail", "Agua"), ("Rest", "Psíquico"), ("Snore", "Normal")]),
        mon("sudowoodo", 56, [("Rock Slide", "Roca"), ("Hammer Arm", "Lucha"), ("Sucker Punch", "Siniestro"), ("Low Kick", "Lucha")]),
        mon("hippowdon", 59, [("Earthquake", "Tierra"), ("Crunch", "Siniestro"), ("Slack Off", "Normal"), ("Sandstorm", "Roca")]),
        mon("golem", 56, [("Explosion", "Normal"), ("Rock Polish", "Roca"), ("Earthquake", "Tierra"), ("Stone Edge", "Roca")]),
    ),
    "Flint": team(
        mon("houndoom", 58, [("Flamethrower", "Fuego"), ("Crunch", "Siniestro"), ("Sludge Bomb", "Veneno"), ("Will-O-Wisp", "Fuego")]),
        mon("flareon", 57, [("Fire Blast", "Fuego"), ("Quick Attack", "Normal"), ("Bite", "Siniestro"), ("Sand Attack", "Tierra")]),
        mon("rapidash", 58, [("Flare Blitz", "Fuego"), ("Poison Jab", "Veneno"), ("Megahorn", "Bicho"), ("Bounce", "Volador")]),
        mon("infernape", 61, [("Flare Blitz", "Fuego"), ("Close Combat", "Lucha"), ("Grass Knot", "Planta"), ("Mach Punch", "Lucha")]),
        mon("drifblim", 58, [("Shadow Ball", "Fantasma"), ("Thunderbolt", "Eléctrico"), ("Psychic", "Psíquico"), ("Ominous Wind", "Fantasma")]),
    ),
    "Lucian": team(
        mon("mr-mime", 59, [("Psychic", "Psíquico"), ("Light Screen", "Psíquico"), ("Reflect", "Psíquico"), ("Baton Pass", "Normal")]),
        mon("girafarig", 59, [("Psychic", "Psíquico"), ("Crunch", "Siniestro"), ("Agility", "Psíquico"), ("Baton Pass", "Normal")]),
        mon("alakazam", 60, [("Psychic", "Psíquico"), ("Recover", "Normal"), ("Calm Mind", "Psíquico"), ("Energy Ball", "Planta")]),
        mon("bronzong", 63, [("Gyro Ball", "Acero"), ("Earthquake", "Tierra"), ("Hypnosis", "Psíquico"), ("Psychic", "Psíquico")]),
    ),
    "Cynthia": team(
        mon("spiritomb", 61, [("Shadow Ball", "Fantasma"), ("Dark Pulse", "Siniestro"), ("Confuse Ray", "Fantasma"), ("Silver Wind", "Bicho")]),
        mon("roserade", 60, [("Sludge Bomb", "Veneno"), ("Energy Ball", "Planta"), ("Toxic Spikes", "Veneno"), ("Shadow Ball", "Fantasma")]),
        mon("togekiss", 60, [("Air Slash", "Volador"), ("Aura Sphere", "Lucha"), ("Thunder Wave", "Eléctrico"), ("Flamethrower", "Fuego")]),
        mon("lucario", 63, [("Aura Sphere", "Lucha"), ("Dragon Pulse", "Dragón"), ("Extreme Speed", "Normal"), ("Shadow Ball", "Fantasma")]),
        mon("milotic", 63, [("Surf", "Agua"), ("Ice Beam", "Hielo"), ("Recover", "Normal"), ("Mirror Coat", "Psíquico")]),
        mon("garchomp", 66, [("Dragon Claw", "Dragón"), ("Earthquake", "Tierra"), ("Stone Edge", "Roca"), ("Flamethrower", "Fuego")]),
    ),
}

UPDATE_NAMES = set(DP_TEAMS.keys())
GAME_SLUGS = ("diamond-pearl", "platinum")


def main():
    with open(DB_PATH, encoding="utf-8") as f:
        db = json.load(f)

    updated = []
    for slug in GAME_SLUGS:
        for tr in db["trainers"][slug]:
            if tr["name"] in UPDATE_NAMES:
                tr["team"] = DP_TEAMS[tr["name"]]
                updated.append(f"{slug}/{tr['name']}")

    with open(DB_PATH, "w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print("Actualizados:", ", ".join(updated))


if __name__ == "__main__":
    main()
