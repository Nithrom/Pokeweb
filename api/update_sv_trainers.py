"""
Gimnasios, Alto Mando y campeona — Escarlata / Púrpura.
Uso: python update_sv_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'scarlet-violet'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/sv/{slug}.jpg'


def mv(slug: str, display: str) -> dict:
    return {'name': slug, 'name_display': display}


def mon(name: str, display: str, level: int, types: list[str], moves: list[dict]) -> dict:
    return {
        'name': name,
        'name_display': display,
        'level': level,
        'types': types,
        'moves': moves,
    }


def gym(
    name: str,
    order: int,
    location: str,
    specialty: str,
    sprite: str,
    team: list[dict],
) -> dict:
    return {
        'name': name,
        'type': 'gym',
        'order': order,
        'location': location,
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite),
        'team': team,
    }


def e4(name: str, order: int, specialty: str, sprite: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'elite4',
        'order': order,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite),
        'team': team,
    }


def champion(name: str, specialty: str, sprite: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'champion',
        'order': 1,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite),
        'team': team,
    }


def build_gyms() -> list[dict]:
    return [
        gym('Katy', 1, 'Cortondo', 'badgebug', 'katy', [
            mon('nymble', 'Nymble', 14, ['bug'], [
                mv('tackle', 'Tackle'),
                mv('struggle-bug', 'Struggle Bug'),
                mv('astonish', 'Astonish'),
                mv('double-kick', 'Double Kick'),
            ]),
            mon('tarountula', 'Tarountula', 14, ['bug'], [
                mv('tackle', 'Tackle'),
                mv('string-shot', 'String Shot'),
                mv('bug-bite', 'Bug Bite'),
                mv('scary-face', 'Scary Face'),
            ]),
            mon('teddiursa', 'Teddiursa', 15, ['normal'], [
                mv('scratch', 'Scratch'),
                mv('leer', 'Leer'),
                mv('fury-swipes', 'Fury Swipes'),
                mv('lick', 'Lick'),
            ]),
        ]),
        gym('Brassius', 2, 'Artazon', 'badgegrass', 'brassius', [
            mon('petilil', 'Petilil', 16, ['grass'], [
                mv('absorb', 'Absorb'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('stun-spore', 'Stun Spore'),
                mv('magical-leaf', 'Magical Leaf'),
            ]),
            mon('smoliv', 'Smoliv', 16, ['grass', 'normal'], [
                mv('tackle', 'Tackle'),
                mv('razor-leaf', 'Razor Leaf'),
                mv('growth', 'Growth'),
                mv('sweet-scent', 'Sweet Scent'),
            ]),
            mon('sudowoodo', 'Sudowoodo', 17, ['rock'], [
                mv('rock-throw', 'Rock Throw'),
                mv('low-kick', 'Low Kick'),
                mv('flail', 'Flail'),
                mv('mimic', 'Mimic'),
            ]),
        ]),
        gym('Iono', 3, 'Levincia', 'badgedelectric', 'iono', [
            mon('wattrel', 'Wattrel', 23, ['electric', 'flying'], [
                mv('pluck', 'Pluck'),
                mv('quick-attack', 'Quick Attack'),
                mv('charge', 'Charge'),
                mv('wing-attack', 'Wing Attack'),
            ]),
            mon('bellibolt', 'Bellibolt', 23, ['electric'], [
                mv('water-gun', 'Water Gun'),
                mv('spark', 'Spark'),
                mv('mud-shot', 'Mud Shot'),
                mv('charge', 'Charge'),
            ]),
            mon('luxio', 'Luxio', 23, ['electric'], [
                mv('spark', 'Spark'),
                mv('bite', 'Bite'),
                mv('roar', 'Roar'),
                mv('thunder-fang', 'Thunder Fang'),
            ]),
            mon('mismagius', 'Mismagius', 24, ['ghost'], [
                mv('charge-beam', 'Charge Beam'),
                mv('hex', 'Hex'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('magical-leaf', 'Magical Leaf'),
            ]),
        ]),
        gym('Kofu', 4, 'Cascarrafa', 'badgewater', 'kofu', [
            mon('veluza', 'Veluza', 29, ['water', 'psychic'], [
                mv('aqua-cutter', 'Aqua Cutter'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('night-slash', 'Night Slash'),
                mv('slash', 'Slash'),
            ]),
            mon('wugtrio', 'Wugtrio', 29, ['water', 'ground'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('dig', 'Dig'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('mud-shot', 'Mud Shot'),
            ]),
            mon('crabominable', 'Crabominable', 30, ['fighting', 'ice'], [
                mv('ice-punch', 'Ice Punch'),
                mv('crabhammer', 'Crabhammer'),
                mv('close-combat', 'Close Combat'),
                mv('ice-hammer', 'Ice Hammer'),
            ]),
        ]),
        gym('Larry', 5, 'Medali', 'badgenormal', 'larry', [
            mon('komala', 'Komala', 35, ['normal'], [
                mv('yawn', 'Yawn'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('wood-hammer', 'Wood Hammer'),
                mv('slam', 'Slam'),
            ]),
            mon('dudunsparce', 'Dudunsparce', 35, ['normal'], [
                mv('hyper-drill', 'Hyper Drill'),
                mv('drill-run', 'Drill Run'),
                mv('glare', 'Glare'),
                mv('bite', 'Bite'),
            ]),
            mon('staraptor', 'Staraptor', 36, ['normal', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('close-combat', 'Close Combat'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('facade', 'Facade'),
            ]),
        ]),
        gym('Ryme', 6, 'Montenevera', 'badgeghost', 'ryme', [
            mon('banette', 'Banette', 41, ['ghost'], [
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('icy-wind', 'Icy Wind'),
                mv('scary-face', 'Scary Face'),
            ]),
            mon('mimikyu', 'Mimikyu', 41, ['ghost', 'fairy'], [
                mv('shadow-claw', 'Shadow Claw'),
                mv('play-rough', 'Play Rough'),
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('slash', 'Slash'),
            ]),
            mon('spiritomb', 'Spiritomb', 41, ['ghost', 'dark'], [
                mv('dark-pulse', 'Dark Pulse'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('curse', 'Curse'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('houndstone', 'Houndstone', 42, ['ghost'], [
                mv('last-respects', 'Last Respects'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('dig', 'Dig'),
            ]),
            mon('toxtricity', 'Toxtricity', 42, ['electric', 'poison'], [
                mv('overdrive', 'Overdrive'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('boomburst', 'Boomburst'),
                mv('hex', 'Hex'),
            ]),
        ]),
        gym('Tulip', 7, 'Alfornada', 'badgepsychic', 'tulip', [
            mon('farigiraf', 'Farigiraf', 44, ['normal', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('crunch', 'Crunch'),
                mv('reflect', 'Reflect'),
                mv('body-slam', 'Body Slam'),
            ]),
            mon('gardevoir', 'Gardevoir', 44, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('calm-mind', 'Calm Mind'),
            ]),
            mon('espathra', 'Espathra', 44, ['psychic'], [
                mv('lumina-crash', 'Lumina Crash'),
                mv('quick-attack', 'Quick Attack'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('feather-dance', 'Feather Dance'),
            ]),
            mon('gallade', 'Gallade', 44, ['psychic', 'fighting'], [
                mv('psycho-cut', 'Psycho Cut'),
                mv('leaf-blade', 'Leaf Blade'),
                mv('x-scissor', 'X-Scissor'),
                mv('close-combat', 'Close Combat'),
            ]),
            mon('florges', 'Florges', 45, ['fairy'], [
                mv('moonblast', 'Moonblast'),
                mv('petal-blizzard', 'Petal Blizzard'),
                mv('aromatherapy', 'Aromatherapy'),
                mv('psychic', 'Psychic'),
            ]),
        ]),
        gym('Grusha', 8, 'Glaseado Mountain', 'badgeice', 'grusha', [
            mon('frosmoth', 'Frosmoth', 47, ['ice', 'bug'], [
                mv('ice-beam', 'Ice Beam'),
                mv('bug-buzz', 'Bug Buzz'),
                mv('tailwind', 'Tailwind'),
                mv('hail', 'Hail'),
            ]),
            mon('beartic', 'Beartic', 47, ['ice'], [
                mv('ice-punch', 'Ice Punch'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('earthquake', 'Earthquake'),
                mv('icicle-crash', 'Icicle Crash'),
            ]),
            mon('cetitan', 'Cetitan', 47, ['ice'], [
                mv('ice-spinner', 'Ice Spinner'),
                mv('liquidation', 'Liquidation'),
                mv('ice-shard', 'Ice Shard'),
                mv('bounce', 'Bounce'),
            ]),
            mon('weavile', 'Weavile', 47, ['dark', 'ice'], [
                mv('night-slash', 'Night Slash'),
                mv('ice-punch', 'Ice Punch'),
                mv('ice-shard', 'Ice Shard'),
                mv('x-scissor', 'X-Scissor'),
            ]),
            mon('altaria', 'Altaria', 48, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('ice-beam', 'Ice Beam'),
                mv('moonblast', 'Moonblast'),
                mv('hurricane', 'Hurricane'),
            ]),
        ]),
    ]


def build_gym_rematch() -> list[dict]:
    return [
        gym('Katy', 1, 'Cortondo', 'rematchbug', 'katy', [
            mon('lokix', 'Lokix', 65, ['bug', 'dark'], [
                mv('axe-kick', 'Axe Kick'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('bounce', 'Bounce'),
                mv('lunge', 'Lunge'),
            ]),
            mon('forretress', 'Forretress', 65, ['bug', 'steel'], [
                mv('gyro-ball', 'Gyro Ball'),
                mv('bug-bite', 'Bug Bite'),
                mv('curse', 'Curse'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('spidops', 'Spidops', 65, ['bug'], [
                mv('skitter-smack', 'Skitter Smack'),
                mv('throat-chop', 'Throat Chop'),
                mv('brick-break', 'Brick Break'),
                mv('silk-trap', 'Silk Trap'),
            ]),
            mon('heracross', 'Heracross', 65, ['bug', 'fighting'], [
                mv('megahorn', 'Megahorn'),
                mv('close-combat', 'Close Combat'),
                mv('rock-slide', 'Rock Slide'),
                mv('night-slash', 'Night Slash'),
            ]),
            mon('ursaring', 'Ursaring', 66, ['normal'], [
                mv('fury-cutter', 'Fury Cutter'),
                mv('high-horsepower', 'High Horsepower'),
                mv('play-rough', 'Play Rough'),
                mv('crunch', 'Crunch'),
            ]),
        ]),
        gym('Brassius', 2, 'Artazon', 'rematchgrass', 'brassius', [
            mon('jumpluff', 'Jumpluff', 65, ['grass', 'flying'], [
                mv('sleep-powder', 'Sleep Powder'),
                mv('leech-seed', 'Leech Seed'),
                mv('giga-drain', 'Giga Drain'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('sunflora', 'Sunflora', 65, ['grass'], [
                mv('solar-beam', 'Solar Beam'),
                mv('earth-power', 'Earth Power'),
                mv('growth', 'Growth'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('cherrim', 'Cherrim', 65, ['grass'], [
                mv('solar-beam', 'Solar Beam'),
                mv('petal-blizzard', 'Petal Blizzard'),
                mv('weather-ball', 'Weather Ball'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('breloom', 'Breloom', 65, ['grass', 'fighting'], [
                mv('spore', 'Spore'),
                mv('mach-punch', 'Mach Punch'),
                mv('seed-bomb', 'Seed Bomb'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('roserade', 'Roserade', 66, ['grass', 'poison'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('energy-ball', 'Energy Ball'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('extrasensory', 'Extrasensory'),
            ]),
        ]),
        gym('Iono', 3, 'Levincia', 'rematchelectric', 'iono', [
            mon('bellibolt', 'Bellibolt', 65, ['electric'], [
                mv('water-gun', 'Water Gun'),
                mv('spark', 'Spark'),
                mv('mud-shot', 'Mud Shot'),
                mv('charge', 'Charge'),
            ]),
            mon('luxio', 'Luxio', 65, ['electric'], [
                mv('spark', 'Spark'),
                mv('bite', 'Bite'),
                mv('thunder-fang', 'Thunder Fang'),
                mv('roar', 'Roar'),
            ]),
            mon('mismagius', 'Mismagius', 65, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('charge-beam', 'Charge Beam'),
                mv('hex', 'Hex'),
                mv('magical-leaf', 'Magical Leaf'),
            ]),
            mon('kilowattrel', 'Kilowattrel', 65, ['electric', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('agility', 'Agility'),
                mv('volt-switch', 'Volt Switch'),
            ]),
            mon('raichu', 'Raichu', 66, ['electric'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('focus-blast', 'Focus Blast'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('agility', 'Agility'),
            ]),
        ]),
        gym('Kofu', 4, 'Cascarrafa', 'rematchwater', 'kofu', [
            mon('veluza', 'Veluza', 65, ['water', 'psychic'], [
                mv('aqua-cutter', 'Aqua Cutter'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('night-slash', 'Night Slash'),
                mv('slash', 'Slash'),
            ]),
            mon('wugtrio', 'Wugtrio', 65, ['water', 'ground'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('dig', 'Dig'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('mud-shot', 'Mud Shot'),
            ]),
            mon('crabominable', 'Crabominable', 65, ['fighting', 'ice'], [
                mv('ice-punch', 'Ice Punch'),
                mv('crabhammer', 'Crabhammer'),
                mv('close-combat', 'Close Combat'),
                mv('ice-hammer', 'Ice Hammer'),
            ]),
            mon('dondozo', 'Dondozo', 66, ['water'], [
                mv('wave-crash', 'Wave Crash'),
                mv('earthquake', 'Earthquake'),
                mv('rest', 'Rest'),
                mv('sleep-talk', 'Sleep Talk'),
            ]),
        ]),
        gym('Larry', 5, 'Medali', 'rematchnormal', 'larry', [
            mon('komala', 'Komala', 65, ['normal'], [
                mv('yawn', 'Yawn'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('wood-hammer', 'Wood Hammer'),
                mv('slam', 'Slam'),
            ]),
            mon('dudunsparce', 'Dudunsparce', 65, ['normal'], [
                mv('hyper-drill', 'Hyper Drill'),
                mv('drill-run', 'Drill Run'),
                mv('glare', 'Glare'),
                mv('bite', 'Bite'),
            ]),
            mon('staraptor', 'Staraptor', 65, ['normal', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('close-combat', 'Close Combat'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('facade', 'Facade'),
            ]),
            mon('flamigo', 'Flamigo', 66, ['flying', 'fighting'], [
                mv('brave-bird', 'Brave Bird'),
                mv('close-combat', 'Close Combat'),
                mv('throat-chop', 'Throat Chop'),
                mv('u-turn', 'U-turn'),
            ]),
        ]),
        gym('Ryme', 6, 'Montenevera', 'rematchghost', 'ryme', [
            mon('banette', 'Banette', 65, ['ghost'], [
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('icy-wind', 'Icy Wind'),
                mv('scary-face', 'Scary Face'),
            ]),
            mon('mimikyu', 'Mimikyu', 65, ['ghost', 'fairy'], [
                mv('shadow-claw', 'Shadow Claw'),
                mv('play-rough', 'Play Rough'),
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('slash', 'Slash'),
            ]),
            mon('spiritomb', 'Spiritomb', 65, ['ghost', 'dark'], [
                mv('dark-pulse', 'Dark Pulse'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('curse', 'Curse'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('houndstone', 'Houndstone', 66, ['ghost'], [
                mv('last-respects', 'Last Respects'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('dig', 'Dig'),
            ]),
            mon('toxtricity', 'Toxtricity', 66, ['electric', 'poison'], [
                mv('overdrive', 'Overdrive'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('boomburst', 'Boomburst'),
                mv('hex', 'Hex'),
            ]),
        ]),
        gym('Tulip', 7, 'Alfornada', 'rematchpsychic', 'tulip', [
            mon('farigiraf', 'Farigiraf', 65, ['normal', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('crunch', 'Crunch'),
                mv('reflect', 'Reflect'),
                mv('body-slam', 'Body Slam'),
            ]),
            mon('gardevoir', 'Gardevoir', 65, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('moonblast', 'Moonblast'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('calm-mind', 'Calm Mind'),
            ]),
            mon('espathra', 'Espathra', 65, ['psychic'], [
                mv('lumina-crash', 'Lumina Crash'),
                mv('quick-attack', 'Quick Attack'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('feather-dance', 'Feather Dance'),
            ]),
            mon('gallade', 'Gallade', 65, ['psychic', 'fighting'], [
                mv('psycho-cut', 'Psycho Cut'),
                mv('leaf-blade', 'Leaf Blade'),
                mv('close-combat', 'Close Combat'),
                mv('night-slash', 'Night Slash'),
            ]),
            mon('florges', 'Florges', 66, ['fairy'], [
                mv('moonblast', 'Moonblast'),
                mv('petal-blizzard', 'Petal Blizzard'),
                mv('aromatherapy', 'Aromatherapy'),
                mv('psychic', 'Psychic'),
            ]),
        ]),
        gym('Grusha', 8, 'Glaseado Mountain', 'rematchice', 'grusha', [
            mon('frosmoth', 'Frosmoth', 65, ['ice', 'bug'], [
                mv('ice-beam', 'Ice Beam'),
                mv('bug-buzz', 'Bug Buzz'),
                mv('tailwind', 'Tailwind'),
                mv('hail', 'Hail'),
            ]),
            mon('beartic', 'Beartic', 65, ['ice'], [
                mv('ice-punch', 'Ice Punch'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('earthquake', 'Earthquake'),
                mv('icicle-crash', 'Icicle Crash'),
            ]),
            mon('cetitan', 'Cetitan', 65, ['ice'], [
                mv('ice-spinner', 'Ice Spinner'),
                mv('liquidation', 'Liquidation'),
                mv('ice-shard', 'Ice Shard'),
                mv('bounce', 'Bounce'),
            ]),
            mon('weavile', 'Weavile', 65, ['dark', 'ice'], [
                mv('night-slash', 'Night Slash'),
                mv('ice-punch', 'Ice Punch'),
                mv('ice-shard', 'Ice Shard'),
                mv('x-scissor', 'X-Scissor'),
            ]),
            mon('altaria', 'Altaria', 66, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('ice-beam', 'Ice Beam'),
                mv('moonblast', 'Moonblast'),
                mv('hurricane', 'Hurricane'),
            ]),
        ]),
    ]


def build_elite4() -> list[dict]:
    return [
        e4('Rika', 1, 'e4ground', 'rika', [
            mon('whiscash', 'Whiscash', 57, ['water', 'ground'], [
                mv('muddy-water', 'Muddy Water'),
                mv('earth-power', 'Earth Power'),
                mv('waterfall', 'Waterfall'),
                mv('zen-headbutt', 'Zen Headbutt'),
            ]),
            mon('camerupt', 'Camerupt', 57, ['fire', 'ground'], [
                mv('earth-power', 'Earth Power'),
                mv('flamethrower', 'Flamethrower'),
                mv('rock-slide', 'Rock Slide'),
                mv('body-press', 'Body Press'),
            ]),
            mon('donphan', 'Donphan', 57, ['ground'], [
                mv('earthquake', 'Earthquake'),
                mv('ice-shard', 'Ice Shard'),
                mv('rapid-spin', 'Rapid Spin'),
                mv('rock-slide', 'Rock Slide'),
            ]),
            mon('dugtrio', 'Dugtrio', 57, ['ground'], [
                mv('earthquake', 'Earthquake'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('slash', 'Slash'),
                mv('sand-attack', 'Sand Attack'),
            ]),
            mon('clodsire', 'Clodsire', 58, ['poison', 'ground'], [
                mv('poison-jab', 'Poison Jab'),
                mv('earthquake', 'Earthquake'),
                mv('recover', 'Recover'),
                mv('stone-edge', 'Stone Edge'),
            ]),
        ]),
        e4('Poppy', 2, 'e4steel', 'poppy', [
            mon('copperajah', 'Copperajah', 58, ['steel'], [
                mv('heavy-slam', 'Heavy Slam'),
                mv('play-rough', 'Play Rough'),
                mv('high-horsepower', 'High Horsepower'),
                mv('rock-slide', 'Rock Slide'),
            ]),
            mon('corviknight', 'Corviknight', 58, ['flying', 'steel'], [
                mv('brave-bird', 'Brave Bird'),
                mv('iron-head', 'Iron Head'),
                mv('roost', 'Roost'),
                mv('body-press', 'Body Press'),
            ]),
            mon('magnezone', 'Magnezone', 58, ['electric', 'steel'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('tri-attack', 'Tri Attack'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('bronzong', 'Bronzong', 58, ['steel', 'psychic'], [
                mv('gyro-ball', 'Gyro Ball'),
                mv('earthquake', 'Earthquake'),
                mv('psychic', 'Psychic'),
                mv('light-screen', 'Light Screen'),
            ]),
            mon('tinkaton', 'Tinkaton', 59, ['fairy', 'steel'], [
                mv('gigaton-hammer', 'Gigaton Hammer'),
                mv('play-rough', 'Play Rough'),
                mv('brick-break', 'Brick Break'),
                mv('stone-edge', 'Stone Edge'),
            ]),
        ]),
        e4('Larry', 3, 'e4flying', 'larry', [
            mon('tropius', 'Tropius', 59, ['grass', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('leaf-blade', 'Leaf Blade'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
            mon('oricorio', 'Oricorio', 59, ['fire', 'flying'], [
                mv('revelation-dance', 'Revelation Dance'),
                mv('calm-mind', 'Calm Mind'),
                mv('air-slash', 'Air Slash'),
                mv('hurricane', 'Hurricane'),
            ]),
            mon('staraptor', 'Staraptor', 59, ['normal', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('close-combat', 'Close Combat'),
                mv('u-turn', 'U-turn'),
                mv('quick-attack', 'Quick Attack'),
            ]),
            mon('altaria', 'Altaria', 59, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('moonblast', 'Moonblast'),
                mv('hurricane', 'Hurricane'),
                mv('ice-beam', 'Ice Beam'),
            ]),
            mon('flamigo', 'Flamigo', 60, ['flying', 'fighting'], [
                mv('brave-bird', 'Brave Bird'),
                mv('close-combat', 'Close Combat'),
                mv('throat-chop', 'Throat Chop'),
                mv('u-turn', 'U-turn'),
            ]),
        ]),
        e4('Hassel', 4, 'e4dragon', 'hassel', [
            mon('noivern', 'Noivern', 60, ['flying', 'dragon'], [
                mv('draco-meteor', 'Draco Meteor'),
                mv('hurricane', 'Hurricane'),
                mv('flamethrower', 'Flamethrower'),
                mv('boomburst', 'Boomburst'),
            ]),
            mon('dragalge', 'Dragalge', 60, ['poison', 'dragon'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('surf', 'Surf'),
            ]),
            mon('kingdra', 'Kingdra', 60, ['water', 'dragon'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('ice-beam', 'Ice Beam'),
                mv('agility', 'Agility'),
            ]),
            mon('haxorus', 'Haxorus', 60, ['dragon'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('earthquake', 'Earthquake'),
                mv('poison-jab', 'Poison Jab'),
                mv('swords-dance', 'Swords Dance'),
            ]),
            mon('baxcalibur', 'Baxcalibur', 61, ['dragon', 'ice'], [
                mv('glaive-rush', 'Glaive Rush'),
                mv('ice-fang', 'Ice Fang'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
        ]),
    ]


def build_champion() -> list[dict]:
    return [
        champion('Geeta', 'champion', 'geeta', [
            mon('espathra', 'Espathra', 61, ['psychic'], [
                mv('lumina-crash', 'Lumina Crash'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('quick-attack', 'Quick Attack'),
                mv('reflect', 'Reflect'),
            ]),
            mon('gogoat', 'Gogoat', 61, ['grass'], [
                mv('horn-leech', 'Horn Leech'),
                mv('earthquake', 'Earthquake'),
                mv('bulk-up', 'Bulk Up'),
                mv('play-rough', 'Play Rough'),
            ]),
            mon('veluza', 'Veluza', 61, ['water', 'psychic'], [
                mv('aqua-cutter', 'Aqua Cutter'),
                mv('night-slash', 'Night Slash'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('liquidation', 'Liquidation'),
            ]),
            mon('avalugg', 'Avalugg', 61, ['ice'], [
                mv('avalanche', 'Avalanche'),
                mv('body-press', 'Body Press'),
                mv('recover', 'Recover'),
                mv('earthquake', 'Earthquake'),
            ]),
            mon('kingambit', 'Kingambit', 61, ['dark', 'steel'], [
                mv('kowtow-cleave', 'Kowtow Cleave'),
                mv('iron-head', 'Iron Head'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('swords-dance', 'Swords Dance'),
            ]),
            mon('glimmora', 'Glimmora', 62, ['rock', 'poison'], [
                mv('power-gem', 'Power Gem'),
                mv('sludge-wave', 'Sludge Wave'),
                mv('earth-power', 'Earth Power'),
                mv('toxic-spikes', 'Toxic Spikes'),
            ]),
        ]),
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    built = (
        build_gyms()
        + build_gym_rematch()
        + build_elite4()
        + build_champion()
    )
    skip = {'gym', 'elite4', 'champion'}
    rest = [t for t in current if t.get('type') not in skip]
    trainers[GAME_SLUG] = built + rest

    for g in data.get('games', []):
        if g.get('slug') == GAME_SLUG:
            g['trainer_count'] = len(trainers[GAME_SLUG])

    TRAINERS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(
        f'OK: {len(build_gyms())} gimnasios, {len(build_gym_rematch())} revanchas, '
        f'{len(build_elite4())} E4, {len(build_champion())} campeona, '
        f'{len(rest)} otros en {GAME_SLUG}'
    )


if __name__ == '__main__':
    main()
