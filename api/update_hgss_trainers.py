#!/usr/bin/env python3
"""Actualiza equipos HeartGold/SoulSilver en trainers_db.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "data" / "trainers_db.json"
GAME = "heartgold-soulsilver"

MOVE_ALIASES = {
    "mud-slap": "mud-slap",
    "mud slap": "mud-slap",
    "sonicboom": "sonic-boom",
    "sonic boom": "sonic-boom",
    "doubleslap": "double-slap",
    "double slap": "double-slap",
    "stringshot": "string-shot",
    "string shot": "string-shot",
    "meanlook": "mean-look",
    "mean look": "mean-look",
    "dreameater": "dream-eater",
    "dream eater": "dream-eater",
    "karatechop": "karate-chop",
    "karate chop": "karate-chop",
    "furyswipes": "fury-swipes",
    "fury swipes": "fury-swipes",
    "mindreader": "mind-reader",
    "mind reader": "mind-reader",
    "dynamicpunch": "dynamic-punch",
    "dynamic punch": "dynamic-punch",
    "irontail": "iron-tail",
    "iron tail": "iron-tail",
    "rockthrow": "rock-throw",
    "rock throw": "rock-throw",
    "sunnyday": "sunny-day",
    "sunny day": "sunny-day",
    "aurorabeam": "aurora-beam",
    "aurora beam": "aurora-beam",
    "icywind": "icy-wind",
    "icy wind": "icy-wind",
    "iceshard": "ice-shard",
    "ice shard": "ice-shard",
    "furyattack": "fury-attack",
    "fury attack": "fury-attack",
    "dragonbreath": "dragon-breath",
    "dragon breath": "dragon-breath",
    "smokescreen": "smoke-screen",
    "smoke screen": "smoke-screen",
    "hyperbeam": "hyper-beam",
    "hyper beam": "hyper-beam",
    "confuseray": "confuse-ray",
    "confuse ray": "confuse-ray",
    "calmmind": "calm-mind",
    "calm mind": "calm-mind",
    "lovelykiss": "lovely-kiss",
    "lovely kiss": "lovely-kiss",
    "icepunch": "ice-punch",
    "ice punch": "ice-punch",
    "slackoff": "slack-off",
    "slack off": "slack-off",
    "sleeppowder": "sleep-powder",
    "sleep powder": "sleep-powder",
    "gigadrain": "giga-drain",
    "giga drain": "giga-drain",
    "stunspore": "stun-spore",
    "stun spore": "stun-spore",
    "airslash": "air-slash",
    "air slash": "air-slash",
    "ominouswind": "ominous-wind",
    "ominous wind": "ominous-wind",
    "poisonjab": "poison-jab",
    "poison jab": "poison-jab",
    "shadowsneak": "shadow-sneak",
    "shadow sneak": "shadow-sneak",
    "swordsdance": "swords-dance",
    "swords dance": "swords-dance",
    "bugbuzz": "bug-buzz",
    "bug buzz": "bug-buzz",
    "acidarmor": "acid-armor",
    "acid armor": "acid-armor",
    "gyroball": "gyro-ball",
    "gyro ball": "gyro-ball",
    "toxicspikes": "toxic-spikes",
    "toxic spikes": "toxic-spikes",
    "crosspoison": "cross-poison",
    "cross poison": "cross-poison",
    "rapidspin": "rapid-spin",
    "rapid spin": "rapid-spin",
    "triplekick": "triple-kick",
    "triple kick": "triple-kick",
    "highjumpkick": "high-jump-kick",
    "high jump kick": "high-jump-kick",
    "brickbreak": "brick-break",
    "brick break": "brick-break",
    "focusenergy": "focus-energy",
    "focus energy": "focus-energy",
    "blazekick": "blaze-kick",
    "blaze kick": "blaze-kick",
    "thunderpunch": "thunder-punch",
    "thunder punch": "thunder-punch",
    "firepunch": "fire-punch",
    "fire punch": "fire-punch",
    "rockslide": "rock-slide",
    "rock slide": "rock-slide",
    "crosschop": "cross-chop",
    "cross chop": "cross-chop",
    "bulkup": "bulk-up",
    "bulk up": "bulk-up",
    "faintattack": "feint-attack",
    "feint attack": "feint-attack",
    "doubleteam": "double-team",
    "double team": "double-team",
    "drillpeck": "drill-peck",
    "drill peck": "drill-peck",
    "nightshade": "night-shade",
    "night shade": "night-shade",
    "featherdance": "feather-dance",
    "feather dance": "feather-dance",
    "shadowball": "shadow-ball",
    "shadow ball": "shadow-ball",
    "dragondance": "dragon-dance",
    "dragon dance": "dragon-dance",
    "fireblast": "fire-blast",
    "fire blast": "fire-blast",
    "dragonclaw": "dragon-claw",
    "dragon claw": "dragon-claw",
    "dragonrush": "dragon-rush",
    "dragon rush": "dragon-rush",
    "aquatail": "aqua-tail",
    "aqua tail": "aqua-tail",
    "thunderwave": "thunder-wave",
    "thunder wave": "thunder-wave",
    "defensecurl": "defense-curl",
    "defense curl": "defense-curl",
    "horndrill": "horn-drill",
    "horn drill": "horn-drill",
    "scaryface": "scary-face",
    "scary face": "scary-face",
    "takedown": "take-down",
    "take down": "take-down",
    "waterpulse": "water-pulse",
    "water pulse": "water-pulse",
    "sweetkiss": "sweet-kiss",
    "sweet kiss": "sweet-kiss",
    "aquaring": "aqua-ring",
    "aqua ring": "aqua-ring",
    "lightscreen": "light-screen",
    "light screen": "light-screen",
    "cottonspore": "cotton-spore",
    "cotton spore": "cotton-spore",
    "leechseed": "leech-seed",
    "leech seed": "leech-seed",
    "petaldance": "petal-dance",
    "petal dance": "petal-dance",
    "solarbeam": "solar-beam",
    "solar beam": "solar-beam",
    "spiderweb": "spider-web",
    "spider web": "spider-web",
    "suckerpunch": "sucker-punch",
    "sucker punch": "sucker-punch",
    "morningsun": "morning-sun",
    "morning sun": "morning-sun",
    "batonpass": "baton-pass",
    "baton pass": "baton-pass",
    "focusblast": "focus-blast",
    "focus blast": "focus-blast",
    "lavaplume": "lava-plume",
    "lava plume": "lava-plume",
    "flareblitz": "flare-blitz",
    "flare blitz": "flare-blitz",
    "megahorn": "megahorn",
    "poisonjab": "poison-jab",
    "extremespeed": "extreme-speed",
    "extreme speed": "extreme-speed",
    "rockwrecker": "rock-wrecker",
    "rock wrecker": "rock-wrecker",
    "icefang": "ice-fang",
    "ice fang": "ice-fang",
    "milkdrink": "milk-drink",
    "milk drink": "milk-drink",
    "quickattack": "quick-attack",
    "quick attack": "quick-attack",
    "furycutter": "fury-cutter",
    "fury cutter": "fury-cutter",
    "poisonsting": "poison-sting",
    "poison sting": "poison-sting",
}

POKEMON_TYPES: dict[str, list[str]] = {
    "pidgey": ["normal", "flying"],
    "pidgeotto": ["normal", "flying"],
    "metapod": ["bug"],
    "kakuna": ["bug", "poison"],
    "scyther": ["bug", "flying"],
    "clefairy": ["normal"],
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
    "aerodactyl": ["rock", "flying"],
    "graveler": ["rock", "ground"],
    "rhyhorn": ["ground", "rock"],
    "omastar": ["rock", "water"],
    "kabutops": ["rock", "water"],
    "onix": ["rock", "ground"],
    "quagsire": ["water", "ground"],
    "luvdisc": ["water"],
    "lapras": ["water", "ice"],
    "raichu": ["electric"],
    "electrode": ["electric"],
    "magneton": ["electric", "steel"],
    "electabuzz": ["electric"],
    "tangela": ["grass"],
    "jumpluff": ["grass", "flying"],
    "bellossom": ["grass"],
    "weezing": ["poison"],
    "espeon": ["psychic"],
    "mr-mime": ["psychic"],
    "alakazam": ["psychic"],
    "magcargo": ["fire", "rock"],
    "rapidash": ["fire"],
    "magmar": ["fire"],
    "pidgeot": ["normal", "flying"],
    "rhyperior": ["ground", "rock"],
    "arcanine": ["fire"],
}

DISPLAY_NAMES: dict[str, str] = {
    "pidgey": "Pidgey",
    "pidgeotto": "Pidgeotto",
    "metapod": "Metapod",
    "kakuna": "Kakuna",
    "scyther": "Scyther",
    "clefairy": "Clefairy",
    "miltank": "Miltank",
    "gastly": "Gastly",
    "haunter": "Haunter",
    "gengar": "Gengar",
    "primeape": "Primeape",
    "poliwrath": "Poliwrath",
    "magnemite": "Magnemite",
    "steelix": "Steelix",
    "seel": "Seel",
    "dewgong": "Dewgong",
    "piloswine": "Piloswine",
    "dragonair": "Dragonair",
    "kingdra": "Kingdra",
    "xatu": "Xatu",
    "jynx": "Jynx",
    "slowbro": "Slowbro",
    "exeggutor": "Exeggutor",
    "ariados": "Ariados",
    "venomoth": "Venomoth",
    "muk": "Muk",
    "forretress": "Forretress",
    "crobat": "Crobat",
    "hitmontop": "Hitmontop",
    "hitmonlee": "Hitmonlee",
    "hitmonchan": "Hitmonchan",
    "onix": "Onix",
    "machamp": "Machamp",
    "umbreon": "Umbreon",
    "vileplume": "Vileplume",
    "murkrow": "Murkrow",
    "houndoom": "Houndoom",
    "gyarados": "Gyarados",
    "dragonite": "Dragonite",
    "aerodactyl": "Aerodactyl",
    "graveler": "Graveler",
    "rhyhorn": "Rhyhorn",
    "omastar": "Omastar",
    "kabutops": "Kabutops",
    "quagsire": "Quagsire",
    "luvdisc": "Luvdisc",
    "lapras": "Lapras",
    "raichu": "Raichu",
    "electrode": "Electrode",
    "magneton": "Magneton",
    "electabuzz": "Electabuzz",
    "tangela": "Tangela",
    "jumpluff": "Jumpluff",
    "bellossom": "Bellossom",
    "weezing": "Weezing",
    "espeon": "Espeon",
    "mr-mime": "Mr. Mime",
    "alakazam": "Alakazam",
    "magcargo": "Magcargo",
    "rapidash": "Rapidash",
    "magmar": "Magmar",
    "pidgeot": "Pidgeot",
    "rhyperior": "Rhyperior",
    "arcanine": "Arcanine",
}


def move_slug(label: str) -> str:
    key = label.strip().lower()
    if key in MOVE_ALIASES:
        return MOVE_ALIASES[key]
    slug = re.sub(r"[^a-z0-9]+", "-", key).strip("-")
    return MOVE_ALIASES.get(slug, slug)


def move_entry(label: str) -> dict:
    return {"name": move_slug(label), "name_display": label.strip()}


def pokemon_entry(species: str, level: int, moves: list[str]) -> dict:
    name = species.lower().replace(" ", "-")
    display = DISPLAY_NAMES.get(name, species.replace("-", " ").title())
    types = POKEMON_TYPES.get(name, ["normal"])
    return {
        "name": name,
        "name_display": display,
        "level": level,
        "types": types,
        "moves": [move_entry(m) for m in moves],
    }


def team(*mons: tuple) -> list[dict]:
    out = []
    for item in mons:
        if len(item) == 3:
            species, level, moves = item
        else:
            raise ValueError(item)
        out.append(pokemon_entry(species, level, moves))
    return out


# (species, level, [moves])
TEAMS: dict[str, list] = {
    "Falkner": team(
        ("pidgey", 9, ["Tackle", "Mud-Slap"]),
        ("pidgeotto", 13, ["Gust", "Quick Attack", "Mud-Slap"]),
    ),
    "Bugsy": team(
        ("metapod", 15, ["Tackle", "String Shot", "Harden"]),
        ("kakuna", 15, ["Poison Sting", "String Shot", "Harden"]),
        ("scyther", 17, ["Quick Attack", "Focus Energy", "Fury Cutter"]),
    ),
    "Whitney": team(
        ("clefairy", 17, ["Double Slap", "Encore", "Metronome", "Mimic"]),
        ("miltank", 19, ["Rollout", "Stomp", "Attract", "Milk Drink"]),
    ),
    "Morty": team(
        ("gastly", 21, ["Hypnosis", "Lick", "Mean Look", "Curse"]),
        ("haunter", 21, ["Hypnosis", "Mean Look", "Curse", "Shadow Ball"]),
        ("haunter", 23, ["Hypnosis", "Shadow Ball", "Mean Look", "Curse"]),
        ("gengar", 25, ["Hypnosis", "Shadow Ball", "Mean Look", "Dream Eater"]),
    ),
    "Chuck": team(
        ("primeape", 29, ["Karate Chop", "Rage", "Fury Swipes", "Leer"]),
        ("poliwrath", 31, ["Surf", "Hypnosis", "Mind Reader", "Dynamic Punch"]),
    ),
    "Jasmine": team(
        ("magnemite", 30, ["Thunderbolt", "SonicBoom", "Supersonic", "Thunder Wave"]),
        ("magnemite", 30, ["Thunderbolt", "SonicBoom", "Supersonic", "Thunder Wave"]),
        ("steelix", 35, ["Iron Tail", "Screech", "Rock Throw", "Sunny Day"]),
    ),
    "Pryce": team(
        ("seel", 30, ["Headbutt", "Aurora Beam", "Rest", "Icy Wind"]),
        ("dewgong", 32, ["Headbutt", "Aurora Beam", "Rest", "Ice Shard"]),
        ("piloswine", 34, ["Fury Attack", "Mist", "Blizzard", "Icy Wind"]),
    ),
    "Clair": team(
        ("dragonair", 38, ["Thunder Wave", "Surf", "Slam", "DragonBreath"]),
        ("dragonair", 38, ["Thunder Wave", "Thunderbolt", "Slam", "DragonBreath"]),
        ("dragonair", 38, ["Thunder Wave", "Ice Beam", "Slam", "DragonBreath"]),
        ("kingdra", 41, ["SmokeScreen", "Surf", "Hyper Beam", "DragonBreath"]),
    ),
    "Will": team(
        ("xatu", 40, ["Psychic", "Confuse Ray", "Quick Attack", "Calm Mind"]),
        ("jynx", 41, ["Lovely Kiss", "Ice Punch", "Psychic", "Double Slap"]),
        ("slowbro", 41, ["Surf", "Psychic", "Amnesia", "Slack Off"]),
        ("exeggutor", 41, ["Psychic", "Sleep Powder", "Giga Drain", "Stun Spore"]),
        ("xatu", 42, ["Psychic", "Air Slash", "Shadow Ball", "Ominous Wind"]),
    ),
    "Koga": team(
        ("ariados", 40, ["Poison Jab", "Agility", "Shadow Sneak", "Swords Dance"]),
        ("venomoth", 41, ["Bug Buzz", "Psychic", "Sleep Powder", "Sludge Bomb"]),
        ("muk", 42, ["Sludge Bomb", "Minimize", "Toxic", "Acid Armor"]),
        ("forretress", 43, ["Explosion", "Gyro Ball", "Spikes", "Toxic Spikes"]),
        ("crobat", 44, ["Cross Poison", "Air Slash", "Confuse Ray", "Haze"]),
    ),
    "Bruno": team(
        ("hitmontop", 42, ["Rapid Spin", "Counter", "Agility", "Triple Kick"]),
        ("hitmonlee", 42, ["High Jump Kick", "Brick Break", "Focus Energy", "Blaze Kick"]),
        ("hitmonchan", 42, ["Ice Punch", "ThunderPunch", "Fire Punch", "Counter"]),
        ("onix", 43, ["Rock Slide", "Earthquake", "Sandstorm", "Screech"]),
        ("machamp", 46, ["Cross Chop", "Rock Slide", "Earthquake", "Bulk Up"]),
    ),
    "Karen": team(
        ("umbreon", 42, ["Faint Attack", "Confuse Ray", "Moonlight", "Double Team"]),
        ("vileplume", 42, ["Sludge Bomb", "Sleep Powder", "Moonlight", "Giga Drain"]),
        ("murkrow", 44, ["Drill Peck", "Night Shade", "Confuse Ray", "FeatherDance"]),
        ("gengar", 45, ["Shadow Ball", "Hypnosis", "Dream Eater", "Thunderbolt"]),
        ("houndoom", 47, ["Flamethrower", "Crunch", "Sludge Bomb", "Sunny Day"]),
    ),
    "Lance": team(
        ("gyarados", 46, ["Dragon Dance", "Waterfall", "Earthquake", "Hyper Beam"]),
        ("dragonite", 49, ["Dragon Claw", "Thunder", "Blizzard", "Fire Blast"]),
        ("dragonite", 49, ["Dragon Rush", "Aqua Tail", "Thunder Wave", "Hurricane"]),
        ("aerodactyl", 48, ["Rock Slide", "Earthquake", "Crunch", "Hyper Beam"]),
        ("dragonite", 50, ["Outrage", "Fire Blast", "Thunderbolt", "Ice Beam"]),
        ("dragonite", 50, ["Outrage", "Dragon Dance", "Fire Punch", "ThunderPunch"]),
    ),
    "Brock": team(
        ("graveler", 51, ["Rock Slide", "Earthquake", "Explosion", "Defense Curl"]),
        ("rhyhorn", 51, ["Earthquake", "Horn Attack", "Scary Face", "Take Down"]),
        ("omastar", 53, ["Surf", "Ice Beam", "Rock Slide", "Withdraw"]),
        ("onix", 54, ["Rock Slide", "Earthquake", "Sandstorm", "Screech"]),
        ("kabutops", 52, ["Waterfall", "Rock Slide", "Slash", "Leer"]),
    ),
    "Misty": team(
        ("quagsire", 52, ["Surf", "Earthquake", "Amnesia", "Mud Shot"]),
        ("luvdisc", 54, ["Water Pulse", "Attract", "Sweet Kiss", "Aqua Ring"]),
        ("lapras", 56, ["Ice Beam", "Surf", "Thunderbolt", "Psychic"]),
    ),
    "Lt. Surge": team(
        ("raichu", 51, ["Thunderbolt", "Quick Attack", "Thunder Wave", "Double Team"]),
        ("electrode", 47, ["Explosion", "Thunderbolt", "Light Screen", "SonicBoom"]),
        ("electrode", 47, ["Explosion", "Thunderbolt", "Light Screen", "SonicBoom"]),
        ("magneton", 47, ["Thunderbolt", "Supersonic", "SonicBoom", "Thunder Wave"]),
        ("electabuzz", 53, ["ThunderPunch", "Light Screen", "Quick Attack", "Thunder Wave"]),
    ),
    "Erika": team(
        ("tangela", 51, ["Giga Drain", "Stun Spore", "Sleep Powder", "Bind"]),
        ("jumpluff", 51, ["Sleep Powder", "Cotton Spore", "Acrobatics", "Leech Seed"]),
        ("bellossom", 52, ["Petal Dance", "Sunny Day", "Moonlight", "Stun Spore"]),
        ("vileplume", 56, ["Sludge Bomb", "Sleep Powder", "Petal Dance", "Acid"]),
    ),
    "Janine": team(
        ("ariados", 44, ["Poison Jab", "Agility", "Shadow Sneak", "Spider Web"]),
        ("crobat", 47, ["Cross Poison", "Air Slash", "Confuse Ray", "Haze"]),
        ("weezing", 47, ["Sludge Bomb", "Explosion", "Toxic", "Smokescreen"]),
        ("venomoth", 50, ["Psychic", "Bug Buzz", "Sleep Powder", "Sludge Bomb"]),
        ("ariados", 47, ["Poison Jab", "Shadow Sneak", "Sucker Punch", "Agility"]),
    ),
    "Sabrina": team(
        ("espeon", 53, ["Psychic", "Morning Sun", "Shadow Ball", "Quick Attack"]),
        ("mr-mime", 53, ["Psychic", "Reflect", "Light Screen", "Baton Pass"]),
        ("alakazam", 55, ["Psychic", "Recover", "Calm Mind", "Focus Blast"]),
    ),
    "Blaine": team(
        ("magcargo", 54, ["Lava Plume", "Rock Slide", "Amnesia", "Body Slam"]),
        ("rapidash", 53, ["Flare Blitz", "Megahorn", "Bounce", "Poison Jab"]),
        ("magmar", 54, ["Flamethrower", "ThunderPunch", "Psychic", "Confuse Ray"]),
        ("houndoom", 59, ["Flamethrower", "Crunch", "Sludge Bomb", "Sunny Day"]),
    ),
    "Blue": team(
        ("pidgeot", 60, ["Air Slash", "Quick Attack", "Whirlwind", "Roost"]),
        ("alakazam", 58, ["Psychic", "Recover", "Calm Mind", "Focus Blast"]),
        ("rhyperior", 58, ["Earthquake", "Rock Wrecker", "Megahorn", "Stone Edge"]),
        ("exeggutor", 58, ["Psychic", "SolarBeam", "Sleep Powder", "Stun Spore"]),
        ("arcanine", 58, ["Flamethrower", "ExtremeSpeed", "Crunch", "Roar"]),
        ("gyarados", 58, ["Waterfall", "Ice Fang", "Earthquake", "Dragon Dance"]),
    ),
}


def main() -> None:
    with DB_PATH.open(encoding="utf-8") as f:
        db = json.load(f)

    trainers = db.get("trainers", {}).get(GAME)
    if not trainers:
        raise SystemExit(f"No trainers for {GAME}")

    updated = 0
    for t in trainers:
        name = t.get("name")
        if name not in TEAMS:
            continue
        t["team"] = [dict(p) for p in TEAMS[name]]
        updated += 1
        print(f"  {name}: {len(t['team'])} Pokémon")

    with DB_PATH.open("w", encoding="utf-8") as f:
        json.dump(db, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"\nActualizados {updated} entrenadores en {GAME}")


if __name__ == "__main__":
    main()
