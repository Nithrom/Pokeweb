"""
Gimnasios, Alto Mando y campeona — Diamante Brillante / Perla Reluciente.
Uso: python update_bdsp_gyms.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'brilliant-diamond-shining-pearl'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/diamond-pearl/{slug}.png'


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


def build_gyms() -> list[dict]:
    return [
        gym('Roark', 1, 'Oreburgh City', 'badgerock', 'roark', [
            mon('geodude', 'Geodude', 12, ['rock', 'ground'], [
                mv('stealth-rock', 'Stealth Rock'),
                mv('rock-polish', 'Rock Polish'),
                mv('bulldoze', 'Bulldoze'),
                mv('rock-throw', 'Rock Throw'),
            ]),
            mon('onix', 'Onix', 12, ['rock', 'ground'], [
                mv('rock-throw', 'Rock Throw'),
                mv('bind', 'Bind'),
                mv('screech', 'Screech'),
                mv('stealth-rock', 'Stealth Rock'),
            ]),
            mon('cranidos', 'Cranidos', 14, ['rock'], [
                mv('headbutt', 'Headbutt'),
                mv('leer', 'Leer'),
                mv('pursuit', 'Pursuit'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
        ]),
        gym('Gardenia', 2, 'Eterna City', 'badgegrass', 'gardenia', [
            mon('cherubi', 'Cherubi', 19, ['grass'], [
                mv('magical-leaf', 'Magical Leaf'),
                mv('leech-seed', 'Leech Seed'),
                mv('tackle', 'Tackle'),
                mv('growth', 'Growth'),
            ]),
            mon('roserade', 'Roserade', 22, ['grass', 'poison'], [
                mv('magical-leaf', 'Magical Leaf'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('stun-spore', 'Stun Spore'),
                mv('grass-knot', 'Grass Knot'),
            ]),
        ]),
        gym('Maylene', 3, 'Veilstone City', 'badgefighting', 'maylene', [
            mon('meditite', 'Meditite', 27, ['fighting', 'psychic'], [
                mv('drain-punch', 'Drain Punch'),
                mv('confusion', 'Confusion'),
                mv('detect', 'Detect'),
                mv('force-palm', 'Force Palm'),
            ]),
            mon('machoke', 'Machoke', 27, ['fighting'], [
                mv('karate-chop', 'Karate Chop'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('foresight', 'Foresight'),
                mv('focus-energy', 'Focus Energy'),
            ]),
            mon('lucario', 'Lucario', 30, ['fighting', 'steel'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('metal-claw', 'Metal Claw'),
                mv('quick-attack', 'Quick Attack'),
                mv('swords-dance', 'Swords Dance'),
            ]),
        ]),
        gym('Crasher Wake', 4, 'Pastoria City', 'badgewater', 'crasher-wake', [
            mon('gyarados', 'Gyarados', 27, ['water', 'flying'], [
                mv('waterfall', 'Waterfall'),
                mv('ice-fang', 'Ice Fang'),
                mv('bite', 'Bite'),
                mv('dragon-rage', 'Dragon Rage'),
            ]),
            mon('quagsire', 'Quagsire', 27, ['water', 'ground'], [
                mv('water-pulse', 'Water Pulse'),
                mv('yawn', 'Yawn'),
                mv('mud-shot', 'Mud Shot'),
                mv('slam', 'Slam'),
            ]),
            mon('floatzel', 'Floatzel', 30, ['water'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('swift', 'Swift'),
            ]),
        ]),
        gym('Fantina', 5, 'Hearthome City', 'badgeghost', 'fantina', [
            mon('duskull', 'Duskull', 32, ['ghost'], [
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('night-shade', 'Night Shade'),
                mv('pursuit', 'Pursuit'),
            ]),
            mon('haunter', 'Haunter', 34, ['ghost', 'poison'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('hypnosis', 'Hypnosis'),
                mv('dream-eater', 'Dream Eater'),
                mv('sludge-bomb', 'Sludge Bomb'),
            ]),
            mon('mismagius', 'Mismagius', 36, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('magical-leaf', 'Magical Leaf'),
                mv('psybeam', 'Psybeam'),
                mv('power-gem', 'Power Gem'),
            ]),
        ]),
        gym('Byron', 6, 'Canalave City', 'badgesteel', 'byron', [
            mon('magneton', 'Magneton', 37, ['electric', 'steel'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('tri-attack', 'Tri Attack'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('steelix', 'Steelix', 38, ['steel', 'ground'], [
                mv('iron-tail', 'Iron Tail'),
                mv('crunch', 'Crunch'),
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
            ]),
            mon('bastiodon', 'Bastiodon', 41, ['steel', 'rock'], [
                mv('iron-head', 'Iron Head'),
                mv('stone-edge', 'Stone Edge'),
                mv('curse', 'Curse'),
                mv('protect', 'Protect'),
            ]),
        ]),
        gym('Candice', 7, 'Snowpoint City', 'badgeice', 'candice', [
            mon('sneasel', 'Sneasel', 38, ['dark', 'ice'], [
                mv('ice-punch', 'Ice Punch'),
                mv('slash', 'Slash'),
                mv('fake-out', 'Fake Out'),
                mv('quick-attack', 'Quick Attack'),
            ]),
            mon('piloswine', 'Piloswine', 38, ['ice', 'ground'], [
                mv('ice-shard', 'Ice Shard'),
                mv('bulldoze', 'Bulldoze'),
                mv('ancient-power', 'Ancient Power'),
                mv('hail', 'Hail'),
            ]),
            mon('abomasnow', 'Abomasnow', 42, ['grass', 'ice'], [
                mv('blizzard', 'Blizzard'),
                mv('wood-hammer', 'Wood Hammer'),
                mv('ice-shard', 'Ice Shard'),
                mv('ingrain', 'Ingrain'),
            ]),
            mon('froslass', 'Froslass', 40, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('double-team', 'Double Team'),
            ]),
        ]),
        gym('Volkner', 8, 'Sunyshore City', 'badgedelectric', 'volkner', [
            mon('raichu', 'Raichu', 46, ['electric'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('focus-blast', 'Focus Blast'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('agility', 'Agility'),
            ]),
            mon('ambipom', 'Ambipom', 47, ['normal'], [
                mv('double-hit', 'Double Hit'),
                mv('agility', 'Agility'),
                mv('swift', 'Swift'),
                mv('fake-out', 'Fake Out'),
            ]),
            mon('octillery', 'Octillery', 47, ['water'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('flamethrower', 'Flamethrower'),
                mv('ice-beam', 'Ice Beam'),
                mv('bullet-seed', 'Bullet Seed'),
            ]),
            mon('luxray', 'Luxray', 49, ['electric'], [
                mv('thunder-fang', 'Thunder Fang'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
        ]),
    ]


def build_gym_rematch() -> list[dict]:
    return [
        gym('Roark', 1, 'Oreburgh City', 'rematchrock', 'roark', [
            mon('tyranitar', 'Tyranitar', 68, ['rock', 'dark'], [
                mv('stone-edge', 'Stone Edge'),
                mv('crunch', 'Crunch'),
                mv('stealth-rock', 'Stealth Rock'),
                mv('earthquake', 'Earthquake'),
            ]),
            mon('aerodactyl', 'Aerodactyl', 66, ['rock', 'flying'], [
                mv('rock-slide', 'Rock Slide'),
                mv('earthquake', 'Earthquake'),
                mv('roost', 'Roost'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('armaldo', 'Armaldo', 70, ['rock', 'bug'], [
                mv('x-scissor', 'X-Scissor'),
                mv('rock-slide', 'Rock Slide'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('earthquake', 'Earthquake'),
            ]),
            mon('relicanth', 'Relicanth', 64, ['water', 'rock'], [
                mv('head-smash', 'Head Smash'),
                mv('aqua-tail', 'Aqua Tail'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('rest', 'Rest'),
            ]),
            mon('rampardos', 'Rampardos', 72, ['rock'], [
                mv('head-smash', 'Head Smash'),
                mv('earthquake', 'Earthquake'),
                mv('fire-punch', 'Fire Punch'),
                mv('zen-headbutt', 'Zen Headbutt'),
            ]),
        ]),
        gym('Gardenia', 2, 'Eterna City', 'rematchgrass', 'gardenia', [
            mon('jumpluff', 'Jumpluff', 66, ['grass', 'flying'], [
                mv('sleep-powder', 'Sleep Powder'),
                mv('leech-seed', 'Leech Seed'),
                mv('giga-drain', 'Giga Drain'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('sunflora', 'Sunflora', 70, ['grass'], [
                mv('solar-beam', 'Solar Beam'),
                mv('earth-power', 'Earth Power'),
                mv('growth', 'Growth'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('cherrim', 'Cherrim', 69, ['grass'], [
                mv('solar-beam', 'Solar Beam'),
                mv('petal-blizzard', 'Petal Blizzard'),
                mv('weather-ball', 'Weather Ball'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('breloom', 'Breloom', 68, ['grass', 'fighting'], [
                mv('spore', 'Spore'),
                mv('mach-punch', 'Mach Punch'),
                mv('seed-bomb', 'Seed Bomb'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('torterra', 'Torterra', 68, ['grass', 'ground'], [
                mv('wood-hammer', 'Wood Hammer'),
                mv('earthquake', 'Earthquake'),
                mv('stone-edge', 'Stone Edge'),
                mv('leech-seed', 'Leech Seed'),
            ]),
            mon('roserade', 'Roserade', 72, ['grass', 'poison'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('energy-ball', 'Energy Ball'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('extrasensory', 'Extrasensory'),
            ]),
        ]),
        gym('Maylene', 3, 'Veilstone City', 'rematchfighting', 'maylene', [
            mon('hitmontop', 'Hitmontop', 64, ['fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('stone-edge', 'Stone Edge'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('brick-break', 'Brick Break'),
            ]),
            mon('breloom', 'Breloom', 66, ['grass', 'fighting'], [
                mv('mach-punch', 'Mach Punch'),
                mv('bullet-seed', 'Bullet Seed'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('spore', 'Spore'),
            ]),
            mon('heracross', 'Heracross', 68, ['bug', 'fighting'], [
                mv('megahorn', 'Megahorn'),
                mv('close-combat', 'Close Combat'),
                mv('facade', 'Facade'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('infernape', 'Infernape', 70, ['fire', 'fighting'], [
                mv('flare-blitz', 'Flare Blitz'),
                mv('close-combat', 'Close Combat'),
                mv('thunder-punch', 'Thunder Punch'),
                mv('acrobatics', 'Acrobatics'),
            ]),
            mon('medicham', 'Medicham', 72, ['fighting', 'psychic'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
            ]),
            mon('lucario', 'Lucario', 74, ['fighting', 'steel'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('vacuum-wave', 'Vacuum Wave'),
                mv('water-pulse', 'Water Pulse'),
            ]),
        ]),
        gym('Crasher Wake', 4, 'Pastoria City', 'rematchwater', 'crasher-wake', [
            mon('politoed', 'Politoed', 68, ['water'], [
                mv('surf', 'Surf'),
                mv('ice-beam', 'Ice Beam'),
                mv('perish-song', 'Perish Song'),
                mv('focus-blast', 'Focus Blast'),
            ]),
            mon('kingdra', 'Kingdra', 68, ['water', 'dragon'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('ice-beam', 'Ice Beam'),
                mv('rest', 'Rest'),
            ]),
            mon('ludicolo', 'Ludicolo', 68, ['water', 'grass'], [
                mv('energy-ball', 'Energy Ball'),
                mv('hydro-pump', 'Hydro Pump'),
                mv('teeter-dance', 'Teeter Dance'),
                mv('substitute', 'Substitute'),
            ]),
            mon('huntail', 'Huntail', 70, ['water'], [
                mv('crunch', 'Crunch'),
                mv('aqua-tail', 'Aqua Tail'),
                mv('ice-fang', 'Ice Fang'),
                mv('shell-smash', 'Shell Smash'),
            ]),
            mon('gyarados', 'Gyarados', 70, ['water', 'flying'], [
                mv('waterfall', 'Waterfall'),
                mv('earthquake', 'Earthquake'),
                mv('ice-fang', 'Ice Fang'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
            mon('floatzel', 'Floatzel', 72, ['water'], [
                mv('aqua-tail', 'Aqua Tail'),
                mv('brick-break', 'Brick Break'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
            ]),
        ]),
        gym('Fantina', 5, 'Hearthome City', 'rematchghost', 'fantina', [
            mon('drifblim', 'Drifblim', 68, ['ghost', 'flying'], [
                mv('acrobatics', 'Acrobatics'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('destiny-bond', 'Destiny Bond'),
                mv('calm-mind', 'Calm Mind'),
            ]),
            mon('banette', 'Banette', 65, ['ghost'], [
                mv('shadow-claw', 'Shadow Claw'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('curse', 'Curse'),
            ]),
            mon('dusknoir', 'Dusknoir', 70, ['ghost'], [
                mv('shadow-punch', 'Shadow Punch'),
                mv('earthquake', 'Earthquake'),
                mv('ice-punch', 'Ice Punch'),
                mv('fire-punch', 'Fire Punch'),
            ]),
            mon('mismagius', 'Mismagius', 70, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('mystical-fire', 'Mystical Fire'),
                mv('power-gem', 'Power Gem'),
                mv('psychic', 'Psychic'),
            ]),
            mon('froslass', 'Froslass', 72, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('spikes', 'Spikes'),
            ]),
            mon('gengar', 'Gengar', 72, ['ghost', 'poison'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('focus-blast', 'Focus Blast'),
                mv('destiny-bond', 'Destiny Bond'),
            ]),
        ]),
        gym('Byron', 6, 'Canalave City', 'rematchsteel', 'byron', [
            mon('skarmory', 'Skarmory', 69, ['steel', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('steel-wing', 'Steel Wing'),
                mv('stealth-rock', 'Stealth Rock'),
                mv('roost', 'Roost'),
            ]),
            mon('steelix', 'Steelix', 69, ['steel', 'ground'], [
                mv('earthquake', 'Earthquake'),
                mv('iron-tail', 'Iron Tail'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
            ]),
            mon('magnezone', 'Magnezone', 70, ['electric', 'steel'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('light-screen', 'Light Screen'),
                mv('magnet-rise', 'Magnet Rise'),
            ]),
            mon('empoleon', 'Empoleon', 70, ['water', 'steel'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('ice-beam', 'Ice Beam'),
                mv('grass-knot', 'Grass Knot'),
            ]),
            mon('aggron', 'Aggron', 72, ['steel', 'rock'], [
                mv('heavy-slam', 'Heavy Slam'),
                mv('stone-edge', 'Stone Edge'),
                mv('earthquake', 'Earthquake'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('bastiodon', 'Bastiodon', 72, ['steel', 'rock'], [
                mv('iron-head', 'Iron Head'),
                mv('stone-edge', 'Stone Edge'),
                mv('toxic', 'Toxic'),
                mv('protect', 'Protect'),
            ]),
        ]),
    ]


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


def build_elite4() -> list[dict]:
    return [
        e4('Aaron', 1, 'e4bug', 'aaron', [
            mon('dustox', 'Dustox', 53, ['bug', 'poison'], [
                mv('toxic', 'Toxic'),
                mv('bug-buzz', 'Bug Buzz'),
                mv('moonlight', 'Moonlight'),
                mv('light-screen', 'Light Screen'),
            ]),
            mon('beautifly', 'Beautifly', 53, ['bug', 'flying'], [
                mv('bug-buzz', 'Bug Buzz'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('psychic', 'Psychic'),
                mv('quiver-dance', 'Quiver Dance'),
            ]),
            mon('vespiquen', 'Vespiquen', 54, ['bug', 'flying'], [
                mv('attack-order', 'Attack Order'),
                mv('defend-order', 'Defend Order'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('heal-order', 'Heal Order'),
            ]),
            mon('heracross', 'Heracross', 54, ['bug', 'fighting'], [
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('facade', 'Facade'),
                mv('close-combat', 'Close Combat'),
            ]),
            mon('drapion', 'Drapion', 57, ['poison', 'dark'], [
                mv('cross-poison', 'Cross Poison'),
                mv('night-slash', 'Night Slash'),
                mv('earthquake', 'Earthquake'),
                mv('x-scissor', 'X-Scissor'),
            ]),
        ]),
        e4('Bertha', 2, 'e4ground', 'bertha', [
            mon('quagsire', 'Quagsire', 55, ['water', 'ground'], [
                mv('recover', 'Recover'),
                mv('toxic', 'Toxic'),
                mv('earthquake', 'Earthquake'),
                mv('surf', 'Surf'),
            ]),
            mon('sudowoodo', 'Sudowoodo', 56, ['rock'], [
                mv('double-edge', 'Double-Edge'),
                mv('head-smash', 'Head Smash'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('low-kick', 'Low Kick'),
            ]),
            mon('golem', 'Golem', 56, ['rock', 'ground'], [
                mv('rock-polish', 'Rock Polish'),
                mv('heavy-slam', 'Heavy Slam'),
                mv('earthquake', 'Earthquake'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('whiscash', 'Whiscash', 55, ['water', 'ground'], [
                mv('bulldoze', 'Bulldoze'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
                mv('zen-headbutt', 'Zen Headbutt'),
            ]),
            mon('hippowdon', 'Hippowdon', 59, ['ground'], [
                mv('ice-fang', 'Ice Fang'),
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rest', 'Rest'),
            ]),
        ]),
        e4('Flint', 3, 'e4fire', 'flint', [
            mon('rapidash', 'Rapidash', 58, ['fire'], [
                mv('flame-charge', 'Flame Charge'),
                mv('iron-tail', 'Iron Tail'),
                mv('poison-jab', 'Poison Jab'),
                mv('hypnosis', 'Hypnosis'),
            ]),
            mon('steelix', 'Steelix', 57, ['steel', 'ground'], [
                mv('thunder-fang', 'Thunder Fang'),
                mv('fire-fang', 'Fire Fang'),
                mv('iron-tail', 'Iron Tail'),
                mv('crunch', 'Crunch'),
            ]),
            mon('drifblim', 'Drifblim', 58, ['ghost', 'flying'], [
                mv('strength-sap', 'Strength Sap'),
                mv('minimize', 'Minimize'),
                mv('baton-pass', 'Baton Pass'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
            mon('lopunny', 'Lopunny', 57, ['normal'], [
                mv('mirror-coat', 'Mirror Coat'),
                mv('high-jump-kick', 'High Jump Kick'),
                mv('quick-attack', 'Quick Attack'),
                mv('fire-punch', 'Fire Punch'),
            ]),
            mon('infernape', 'Infernape', 61, ['fire', 'fighting'], [
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
                mv('close-combat', 'Close Combat'),
                mv('mach-punch', 'Mach Punch'),
            ]),
        ]),
        e4('Lucian', 4, 'e4psychic', 'lucian', [
            mon('mr-mime', 'Mr. Mime', 59, ['psychic', 'fairy'], [
                mv('light-screen', 'Light Screen'),
                mv('reflect', 'Reflect'),
                mv('psychic', 'Psychic'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
            ]),
            mon('girafarig', 'Girafarig', 59, ['normal', 'psychic'], [
                mv('light-screen', 'Light Screen'),
                mv('psychic', 'Psychic'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('trick-room', 'Trick Room'),
            ]),
            mon('medicham', 'Medicham', 60, ['fighting', 'psychic'], [
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('high-jump-kick', 'High Jump Kick'),
                mv('thunder-punch', 'Thunder Punch'),
                mv('ice-punch', 'Ice Punch'),
            ]),
            mon('alakazam', 'Alakazam', 60, ['psychic'], [
                mv('nasty-plot', 'Nasty Plot'),
                mv('psychic', 'Psychic'),
                mv('future-sight', 'Future Sight'),
                mv('shock-wave', 'Shock Wave'),
            ]),
            mon('bronzong', 'Bronzong', 63, ['steel', 'psychic'], [
                mv('gyro-ball', 'Gyro Ball'),
                mv('earthquake', 'Earthquake'),
                mv('payback', 'Payback'),
                mv('trick-room', 'Trick Room'),
            ]),
        ]),
    ]


def build_elite4_rematch() -> list[dict]:
    return [
        e4('Aaron', 1, 'rematchbug', 'aaron', [
            mon('yanmega', 'Yanmega', 65, ['bug', 'flying'], [
                mv('bug-buzz', 'Bug Buzz'),
                mv('air-slash', 'Air Slash'),
                mv('ancient-power', 'Ancient Power'),
                mv('detect', 'Detect'),
            ]),
            mon('scizor', 'Scizor', 65, ['bug', 'steel'], [
                mv('bullet-punch', 'Bullet Punch'),
                mv('x-scissor', 'X-Scissor'),
                mv('night-slash', 'Night Slash'),
                mv('swords-dance', 'Swords Dance'),
            ]),
            mon('vespiquen', 'Vespiquen', 66, ['bug', 'flying'], [
                mv('attack-order', 'Attack Order'),
                mv('defend-order', 'Defend Order'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('power-gem', 'Power Gem'),
            ]),
            mon('heracross', 'Heracross', 67, ['bug', 'fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('facade', 'Facade'),
            ]),
            mon('drapion', 'Drapion', 69, ['poison', 'dark'], [
                mv('cross-poison', 'Cross Poison'),
                mv('night-slash', 'Night Slash'),
                mv('earthquake', 'Earthquake'),
                mv('x-scissor', 'X-Scissor'),
            ]),
        ]),
        e4('Aaron', 1, 'rematch2bug', 'aaron', [
            mon('yanmega', 'Yanmega', 75, ['bug', 'flying'], [
                mv('bug-buzz', 'Bug Buzz'),
                mv('air-slash', 'Air Slash'),
                mv('ancient-power', 'Ancient Power'),
                mv('detect', 'Detect'),
            ]),
            mon('scizor', 'Scizor', 75, ['bug', 'steel'], [
                mv('bullet-punch', 'Bullet Punch'),
                mv('x-scissor', 'X-Scissor'),
                mv('night-slash', 'Night Slash'),
                mv('swords-dance', 'Swords Dance'),
            ]),
            mon('vespiquen', 'Vespiquen', 77, ['bug', 'flying'], [
                mv('attack-order', 'Attack Order'),
                mv('defend-order', 'Defend Order'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('power-gem', 'Power Gem'),
            ]),
            mon('heracross', 'Heracross', 77, ['bug', 'fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('facade', 'Facade'),
            ]),
            mon('flygon', 'Flygon', 75, ['ground', 'dragon'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('earth-power', 'Earth Power'),
                mv('boomburst', 'Boomburst'),
                mv('bug-buzz', 'Bug Buzz'),
            ]),
            mon('drapion', 'Drapion', 79, ['poison', 'dark'], [
                mv('cross-poison', 'Cross Poison'),
                mv('night-slash', 'Night Slash'),
                mv('earthquake', 'Earthquake'),
                mv('x-scissor', 'X-Scissor'),
            ]),
        ]),
        e4('Bertha', 2, 'rematchground', 'bertha', [
            mon('whiscash', 'Whiscash', 66, ['water', 'ground'], [
                mv('earthquake', 'Earthquake'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
                mv('zen-headbutt', 'Zen Headbutt'),
            ]),
            mon('gliscor', 'Gliscor', 69, ['ground', 'flying'], [
                mv('earthquake', 'Earthquake'),
                mv('thunder-fang', 'Thunder Fang'),
                mv('guillotine', 'Guillotine'),
                mv('x-scissor', 'X-Scissor'),
            ]),
            mon('golem', 'Golem', 68, ['rock', 'ground'], [
                mv('rock-polish', 'Rock Polish'),
                mv('heavy-slam', 'Heavy Slam'),
                mv('earthquake', 'Earthquake'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('hippowdon', 'Hippowdon', 68, ['ground'], [
                mv('ice-fang', 'Ice Fang'),
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rest', 'Rest'),
            ]),
            mon('rhyperior', 'Rhyperior', 71, ['ground', 'rock'], [
                mv('earthquake', 'Earthquake'),
                mv('rock-wrecker', 'Rock Wrecker'),
                mv('megahorn', 'Megahorn'),
                mv('hammer-arm', 'Hammer Arm'),
            ]),
        ]),
        e4('Bertha', 2, 'rematch2ground', 'bertha', [
            mon('whiscash', 'Whiscash', 75, ['water', 'ground'], [
                mv('earthquake', 'Earthquake'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
                mv('zen-headbutt', 'Zen Headbutt'),
            ]),
            mon('gliscor', 'Gliscor', 76, ['ground', 'flying'], [
                mv('earthquake', 'Earthquake'),
                mv('thunder-fang', 'Thunder Fang'),
                mv('guillotine', 'Guillotine'),
                mv('x-scissor', 'X-Scissor'),
            ]),
            mon('golem', 'Golem', 76, ['rock', 'ground'], [
                mv('rock-polish', 'Rock Polish'),
                mv('heavy-slam', 'Heavy Slam'),
                mv('earthquake', 'Earthquake'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('hippowdon', 'Hippowdon', 79, ['ground'], [
                mv('ice-fang', 'Ice Fang'),
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rest', 'Rest'),
            ]),
            mon('rhyperior', 'Rhyperior', 81, ['ground', 'rock'], [
                mv('earthquake', 'Earthquake'),
                mv('rock-wrecker', 'Rock Wrecker'),
                mv('megahorn', 'Megahorn'),
                mv('hammer-arm', 'Hammer Arm'),
            ]),
        ]),
        e4('Flint', 3, 'rematchfire', 'flint', [
            mon('houndoom', 'Houndoom', 68, ['dark', 'fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('destiny-bond', 'Destiny Bond'),
                mv('nasty-plot', 'Nasty Plot'),
            ]),
            mon('flareon', 'Flareon', 71, ['fire'], [
                mv('flare-blitz', 'Flare Blitz'),
                mv('flail', 'Flail'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('quick-attack', 'Quick Attack'),
            ]),
            mon('rapidash', 'Rapidash', 69, ['fire'], [
                mv('flare-blitz', 'Flare Blitz'),
                mv('iron-tail', 'Iron Tail'),
                mv('poison-jab', 'Poison Jab'),
                mv('hypnosis', 'Hypnosis'),
            ]),
            mon('infernape', 'Infernape', 71, ['fire', 'fighting'], [
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
                mv('close-combat', 'Close Combat'),
                mv('mach-punch', 'Mach Punch'),
            ]),
            mon('magmortar', 'Magmortar', 73, ['fire'], [
                mv('fire-blast', 'Fire Blast'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('focus-blast', 'Focus Blast'),
                mv('psychic', 'Psychic'),
            ]),
        ]),
        e4('Flint', 3, 'rematch2fire', 'flint', [
            mon('houndoom', 'Houndoom', 78, ['dark', 'fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('destiny-bond', 'Destiny Bond'),
                mv('nasty-plot', 'Nasty Plot'),
            ]),
            mon('flareon', 'Flareon', 81, ['fire'], [
                mv('flare-blitz', 'Flare Blitz'),
                mv('flail', 'Flail'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('quick-attack', 'Quick Attack'),
            ]),
            mon('rapidash', 'Rapidash', 79, ['fire'], [
                mv('flare-blitz', 'Flare Blitz'),
                mv('iron-tail', 'Iron Tail'),
                mv('poison-jab', 'Poison Jab'),
                mv('hypnosis', 'Hypnosis'),
            ]),
            mon('infernape', 'Infernape', 81, ['fire', 'fighting'], [
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
                mv('close-combat', 'Close Combat'),
                mv('mach-punch', 'Mach Punch'),
            ]),
            mon('magmortar', 'Magmortar', 83, ['fire'], [
                mv('fire-blast', 'Fire Blast'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('focus-blast', 'Focus Blast'),
                mv('psychic', 'Psychic'),
            ]),
        ]),
        e4('Lucian', 4, 'rematchpsychic', 'lucian', [
            mon('mr-mime', 'Mr. Mime', 69, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('light-screen', 'Light Screen'),
                mv('reflect', 'Reflect'),
            ]),
            mon('espeon', 'Espeon', 71, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('morning-sun', 'Morning Sun'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
            ]),
            mon('bronzong', 'Bronzong', 70, ['steel', 'psychic'], [
                mv('gyro-ball', 'Gyro Ball'),
                mv('earthquake', 'Earthquake'),
                mv('psychic', 'Psychic'),
                mv('stealth-rock', 'Stealth Rock'),
            ]),
            mon('alakazam', 'Alakazam', 72, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('energy-ball', 'Energy Ball'),
                mv('focus-blast', 'Focus Blast'),
            ]),
            mon('gallade', 'Gallade', 75, ['psychic', 'fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('night-slash', 'Night Slash'),
                mv('swords-dance', 'Swords Dance'),
            ]),
        ]),
        e4('Lucian', 4, 'rematch2psychic', 'lucian', [
            mon('mr-mime', 'Mr. Mime', 79, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('light-screen', 'Light Screen'),
                mv('reflect', 'Reflect'),
            ]),
            mon('espeon', 'Espeon', 81, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('morning-sun', 'Morning Sun'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
            ]),
            mon('bronzong', 'Bronzong', 80, ['steel', 'psychic'], [
                mv('gyro-ball', 'Gyro Ball'),
                mv('earthquake', 'Earthquake'),
                mv('psychic', 'Psychic'),
                mv('stealth-rock', 'Stealth Rock'),
            ]),
            mon('alakazam', 'Alakazam', 82, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('energy-ball', 'Energy Ball'),
                mv('focus-blast', 'Focus Blast'),
            ]),
            mon('slowbro', 'Slowbro', 82, ['water', 'psychic'], [
                mv('scald', 'Scald'),
                mv('psychic', 'Psychic'),
                mv('flamethrower', 'Flamethrower'),
                mv('slack-off', 'Slack Off'),
            ]),
            mon('gallade', 'Gallade', 85, ['psychic', 'fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('night-slash', 'Night Slash'),
                mv('shadow-sneak', 'Shadow Sneak'),
            ]),
        ]),
    ]


def build_champion() -> list[dict]:
    return [
        champion('Cynthia', 'champion', 'cynthia', [
            mon('spiritomb', 'Spiritomb', 61, ['ghost', 'dark'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('psychic', 'Psychic'),
                mv('sucker-punch', 'Sucker Punch'),
            ]),
            mon('roserade', 'Roserade', 60, ['grass', 'poison'], [
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('energy-ball', 'Energy Ball'),
            ]),
            mon('gastrodon', 'Gastrodon', 60, ['water', 'ground'], [
                mv('scald', 'Scald'),
                mv('earthquake', 'Earthquake'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('lucario', 'Lucario', 63, ['fighting', 'steel'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('nasty-plot', 'Nasty Plot'),
            ]),
            mon('milotic', 'Milotic', 63, ['water'], [
                mv('recover', 'Recover'),
                mv('mirror-coat', 'Mirror Coat'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
            ]),
            mon('garchomp', 'Garchomp', 66, ['dragon', 'ground'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('earthquake', 'Earthquake'),
                mv('swords-dance', 'Swords Dance'),
                mv('poison-jab', 'Poison Jab'),
            ]),
        ]),
        champion('Cynthia', 'rematchchampion', 'cynthia', [
            mon('spiritomb', 'Spiritomb', 74, ['ghost', 'dark'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('sucker-punch', 'Sucker Punch'),
            ]),
            mon('roserade', 'Roserade', 74, ['grass', 'poison'], [
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('energy-ball', 'Energy Ball'),
            ]),
            mon('togekiss', 'Togekiss', 76, ['fairy', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('aura-sphere', 'Aura Sphere'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('lucario', 'Lucario', 76, ['fighting', 'steel'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('nasty-plot', 'Nasty Plot'),
            ]),
            mon('milotic', 'Milotic', 74, ['water'], [
                mv('recover', 'Recover'),
                mv('mirror-coat', 'Mirror Coat'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
            ]),
            mon('garchomp', 'Garchomp', 78, ['dragon', 'ground'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('earthquake', 'Earthquake'),
                mv('swords-dance', 'Swords Dance'),
                mv('poison-jab', 'Poison Jab'),
            ]),
        ]),
        champion('Cynthia', 'rematch2champion', 'cynthia', [
            mon('spiritomb', 'Spiritomb', 84, ['ghost', 'dark'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('sucker-punch', 'Sucker Punch'),
            ]),
            mon('porygon-z', 'Porygon-Z', 85, ['normal'], [
                mv('hyper-beam', 'Hyper Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('ice-beam', 'Ice Beam'),
                mv('thunderbolt', 'Thunderbolt'),
            ]),
            mon('togekiss', 'Togekiss', 86, ['fairy', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('aura-sphere', 'Aura Sphere'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('lucario', 'Lucario', 86, ['fighting', 'steel'], [
                mv('close-combat', 'Close Combat'),
                mv('meteor-mash', 'Meteor Mash'),
                mv('earthquake', 'Earthquake'),
                mv('extreme-speed', 'Extreme Speed'),
            ]),
            mon('milotic', 'Milotic', 84, ['water'], [
                mv('recover', 'Recover'),
                mv('mirror-coat', 'Mirror Coat'),
                mv('ice-beam', 'Ice Beam'),
                mv('scald', 'Scald'),
            ]),
            mon('garchomp', 'Garchomp', 88, ['dragon', 'ground'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('earthquake', 'Earthquake'),
                mv('swords-dance', 'Swords Dance'),
                mv('poison-jab', 'Poison Jab'),
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
        + build_elite4_rematch()
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
        f'OK: {len(build_gyms())} gimnasios, {len(build_gym_rematch())} rev. gimnasio, '
        f'{len(build_elite4())} E4 liga, {len(build_elite4_rematch())} E4 revanchas, '
        f'{len(build_champion())} Cynthia, {len(rest)} otros en {GAME_SLUG}'
    )


if __name__ == '__main__':
    main()
