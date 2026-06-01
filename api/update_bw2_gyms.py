"""
Actualiza gimnasios, Alto Mando y campeón en data/trainers_db.json — Negro 2 / Blanco 2.
Uso: python update_bw2_gyms.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'black-white-2'
SPRITE_BW2 = 'https://img.pokemondb.net/sprites/trainers/black-white-2/{slug}.png'
SPRITE_BW = 'https://img.pokemondb.net/sprites/trainers/black-white/{slug}.png'


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
        'sprite': sprite,
        'team': team,
    }


def build_gyms() -> list[dict]:
    return [
        gym(
            'Cheren', 1, 'Aspertia City', 'badgenormal',
            SPRITE_BW2.format(slug='cheren'),
            [
                mon('patrat', 'Patrat', 11, ['normal'], [
                    mv('tackle', 'Tackle'),
                    mv('leer', 'Leer'),
                    mv('bide', 'Bide'),
                ]),
                mon('lillipup', 'Lillipup', 13, ['normal'], [
                    mv('bite', 'Bite'),
                    mv('work-up', 'Work Up'),
                    mv('take-down', 'Take Down'),
                ]),
                mon('watchog', 'Watchog', 13, ['normal'], [
                    mv('hypnosis', 'Hypnosis'),
                    mv('crunch', 'Crunch'),
                    mv('super-fang', 'Super Fang'),
                    mv('confuse-ray', 'Confuse Ray'),
                ]),
            ],
        ),
        gym(
            'Roxie', 2, 'Virbank City', 'badgepoison',
            SPRITE_BW2.format(slug='roxie'),
            [
                mon('koffing', 'Koffing', 16, ['poison'], [
                    mv('smog', 'Smog'),
                    mv('tackle', 'Tackle'),
                    mv('poison-gas', 'Poison Gas'),
                    mv('assurance', 'Assurance'),
                ]),
                mon('whirlipede', 'Whirlipede', 18, ['bug', 'poison'], [
                    mv('bug-bite', 'Bug Bite'),
                    mv('protect', 'Protect'),
                    mv('poison-tail', 'Poison Tail'),
                    mv('steamroller', 'Steamroller'),
                ]),
                mon('scolipede', 'Scolipede', 20, ['bug', 'poison'], [
                    mv('venoshock', 'Venoshock'),
                    mv('steamroller', 'Steamroller'),
                    mv('rock-slide', 'Rock Slide'),
                    mv('poison-jab', 'Poison Jab'),
                ]),
            ],
        ),
        gym(
            'Burgh', 3, 'Castelia City', 'badgebug',
            SPRITE_BW.format(slug='burgh'),
            [
                mon('whirlipede', 'Whirlipede', 22, ['bug', 'poison'], [
                    mv('bug-bite', 'Bug Bite'),
                    mv('protect', 'Protect'),
                    mv('poison-sting', 'Poison Sting'),
                    mv('steamroller', 'Steamroller'),
                ]),
                mon('dwebble', 'Dwebble', 22, ['bug', 'rock'], [
                    mv('smack-down', 'Smack Down'),
                    mv('bug-bite', 'Bug Bite'),
                    mv('shell-smash', 'Shell Smash'),
                    mv('rock-slide', 'Rock Slide'),
                ]),
                mon('leavanny', 'Leavanny', 24, ['bug', 'grass'], [
                    mv('leaf-blade', 'Leaf Blade'),
                    mv('x-scissor', 'X-Scissor'),
                    mv('string-shot', 'String Shot'),
                    mv('protect', 'Protect'),
                ]),
            ],
        ),
        gym(
            'Elesa', 4, 'Nimbasa City', 'badgeelectric',
            SPRITE_BW.format(slug='elesa'),
            [
                mon('emolga', 'Emolga', 25, ['electric', 'flying'], [
                    mv('volt-switch', 'Volt Switch'),
                    mv('aerial-ace', 'Aerial Ace'),
                    mv('electro-ball', 'Electro Ball'),
                    mv('quick-attack', 'Quick Attack'),
                ]),
                mon('emolga', 'Emolga', 25, ['electric', 'flying'], [
                    mv('volt-switch', 'Volt Switch'),
                    mv('double-team', 'Double Team'),
                    mv('aerial-ace', 'Aerial Ace'),
                    mv('pursuit', 'Pursuit'),
                ]),
                mon('zebstrika', 'Zebstrika', 27, ['electric'], [
                    mv('flame-charge', 'Flame Charge'),
                    mv('spark', 'Spark'),
                    mv('volt-switch', 'Volt Switch'),
                    mv('stomp', 'Stomp'),
                ]),
            ],
        ),
        gym(
            'Clay', 5, 'Driftveil City', 'badgeground',
            SPRITE_BW.format(slug='clay'),
            [
                mon('krokorok', 'Krokorok', 31, ['ground', 'dark'], [
                    mv('crunch', 'Crunch'),
                    mv('bulldoze', 'Bulldoze'),
                    mv('sand-tomb', 'Sand Tomb'),
                    mv('torment', 'Torment'),
                ]),
                mon('sandslash', 'Sandslash', 31, ['ground'], [
                    mv('slash', 'Slash'),
                    mv('dig', 'Dig'),
                    mv('sand-attack', 'Sand Attack'),
                    mv('crush-claw', 'Crush Claw'),
                ]),
                mon('excadrill', 'Excadrill', 33, ['ground', 'steel'], [
                    mv('earthquake', 'Earthquake'),
                    mv('rock-slide', 'Rock Slide'),
                    mv('metal-claw', 'Metal Claw'),
                    mv('slash', 'Slash'),
                ]),
            ],
        ),
        gym(
            'Skyla', 6, 'Mistralton City', 'badgeflying',
            SPRITE_BW.format(slug='skyla'),
            [
                mon('swoobat', 'Swoobat', 33, ['psychic', 'flying'], [
                    mv('acrobatics', 'Acrobatics'),
                    mv('confusion', 'Confusion'),
                    mv('air-cutter', 'Air Cutter'),
                    mv('attract', 'Attract'),
                ]),
                mon('skarmory', 'Skarmory', 33, ['steel', 'flying'], [
                    mv('steel-wing', 'Steel Wing'),
                    mv('air-slash', 'Air Slash'),
                    mv('spikes', 'Spikes'),
                    mv('slash', 'Slash'),
                ]),
                mon('swanna', 'Swanna', 35, ['water', 'flying'], [
                    mv('surf', 'Surf'),
                    mv('air-slash', 'Air Slash'),
                    mv('ice-beam', 'Ice Beam'),
                    mv('roost', 'Roost'),
                ]),
            ],
        ),
        gym(
            'Drayden', 7, 'Opelucid City', 'badgedragon',
            SPRITE_BW.format(slug='drayden'),
            [
                mon('druddigon', 'Druddigon', 46, ['dragon'], [
                    mv('dragon-tail', 'Dragon Tail'),
                    mv('crunch', 'Crunch'),
                    mv('revenge', 'Revenge'),
                    mv('flamethrower', 'Flamethrower'),
                ]),
                mon('flygon', 'Flygon', 46, ['ground', 'dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('earthquake', 'Earthquake'),
                    mv('rock-slide', 'Rock Slide'),
                    mv('crunch', 'Crunch'),
                ]),
                mon('haxorus', 'Haxorus', 48, ['dragon'], [
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('slash', 'Slash'),
                    mv('earthquake', 'Earthquake'),
                ]),
            ],
        ),
        gym(
            'Iris', 7, 'Opelucid City', 'badgedragon',
            SPRITE_BW2.format(slug='iris'),
            [
                mon('fraxure', 'Fraxure', 46, ['dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('slash', 'Slash'),
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('false-swipe', 'False Swipe'),
                ]),
                mon('druddigon', 'Druddigon', 46, ['dragon'], [
                    mv('revenge', 'Revenge'),
                    mv('dragon-tail', 'Dragon Tail'),
                    mv('crunch', 'Crunch'),
                    mv('flamethrower', 'Flamethrower'),
                ]),
                mon('haxorus', 'Haxorus', 48, ['dragon'], [
                    mv('outrage', 'Outrage'),
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('earthquake', 'Earthquake'),
                    mv('x-scissor', 'X-Scissor'),
                ]),
            ],
        ),
        gym(
            'Marlon', 8, 'Humilau City', 'badgewater',
            SPRITE_BW2.format(slug='marlon'),
            [
                mon('carracosta', 'Carracosta', 49, ['water', 'rock'], [
                    mv('aqua-jet', 'Aqua Jet'),
                    mv('stone-edge', 'Stone Edge'),
                    mv('crunch', 'Crunch'),
                    mv('shell-smash', 'Shell Smash'),
                ]),
                mon('wailord', 'Wailord', 49, ['water'], [
                    mv('surf', 'Surf'),
                    mv('bounce', 'Bounce'),
                    mv('heavy-slam', 'Heavy Slam'),
                    mv('rest', 'Rest'),
                ]),
                mon('jellicent', 'Jellicent', 51, ['water', 'ghost'], [
                    mv('scald', 'Scald'),
                    mv('shadow-ball', 'Shadow Ball'),
                    mv('recover', 'Recover'),
                    mv('will-o-wisp', 'Will-O-Wisp'),
                ]),
            ],
        ),
    ]


def e4(name: str, order: int, specialty: str, sprite_slug: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'elite4',
        'order': order,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE_BW.format(slug=sprite_slug),
        'team': team,
    }


def build_e4_champion() -> list[dict]:
    return [
        e4('Shauntal', 1, 'shauntalghost', 'shauntal', [
            mon('cofagrigus', 'Cofagrigus', 48, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('psychic', 'Psychic'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('protect', 'Protect'),
            ]),
            mon('golurk', 'Golurk', 48, ['ground', 'ghost'], [
                mv('earthquake', 'Earthquake'),
                mv('shadow-punch', 'Shadow Punch'),
                mv('fly', 'Fly'),
                mv('iron-defense', 'Iron Defense'),
            ]),
            mon('jellicent', 'Jellicent', 48, ['water', 'ghost'], [
                mv('surf', 'Surf'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('recover', 'Recover'),
                mv('ice-beam', 'Ice Beam'),
            ]),
            mon('chandelure', 'Chandelure', 50, ['ghost', 'fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('energy-ball', 'Energy Ball'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
        ]),
        e4('Grimsley', 2, 'grimsleydark', 'grimsley', [
            mon('liepard', 'Liepard', 48, ['dark'], [
                mv('fake-out', 'Fake Out'),
                mv('night-slash', 'Night Slash'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('torment', 'Torment'),
            ]),
            mon('krookodile', 'Krookodile', 48, ['ground', 'dark'], [
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rock-slide', 'Rock Slide'),
                mv('swagger', 'Swagger'),
            ]),
            mon('scrafty', 'Scrafty', 48, ['dark', 'fighting'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('crunch', 'Crunch'),
                mv('dragon-dance', 'Dragon Dance'),
                mv('brick-break', 'Brick Break'),
            ]),
            mon('bisharp', 'Bisharp', 50, ['dark', 'steel'], [
                mv('iron-head', 'Iron Head'),
                mv('night-slash', 'Night Slash'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('metal-claw', 'Metal Claw'),
            ]),
        ]),
        e4('Caitlin', 3, 'caitlinpsychic', 'caitlin', [
            mon('reuniclus', 'Reuniclus', 48, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('focus-blast', 'Focus Blast'),
                mv('recover', 'Recover'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
            mon('musharna', 'Musharna', 48, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('moonlight', 'Moonlight'),
                mv('hypnosis', 'Hypnosis'),
                mv('dream-eater', 'Dream Eater'),
            ]),
            mon('sigilyph', 'Sigilyph', 48, ['psychic', 'flying'], [
                mv('psychic', 'Psychic'),
                mv('air-slash', 'Air Slash'),
                mv('cosmic-power', 'Cosmic Power'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
            mon('gothitelle', 'Gothitelle', 50, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('energy-ball', 'Energy Ball'),
                mv('calm-mind', 'Calm Mind'),
            ]),
        ]),
        e4('Marshal', 4, 'marshalfighting', 'marshal', [
            mon('throh', 'Throh', 48, ['fighting'], [
                mv('storm-throw', 'Storm Throw'),
                mv('body-slam', 'Body Slam'),
                mv('bulk-up', 'Bulk Up'),
                mv('revenge', 'Revenge'),
            ]),
            mon('sawk', 'Sawk', 48, ['fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('retaliate', 'Retaliate'),
            ]),
            mon('mienshao', 'Mienshao', 48, ['fighting', 'psychic'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('u-turn', 'U-turn'),
                mv('acrobatics', 'Acrobatics'),
                mv('fake-out', 'Fake Out'),
            ]),
            mon('conkeldurr', 'Conkeldurr', 50, ['fighting'], [
                mv('hammer-arm', 'Hammer Arm'),
                mv('stone-edge', 'Stone Edge'),
                mv('mach-punch', 'Mach Punch'),
                mv('bulk-up', 'Bulk Up'),
            ]),
        ]),
        {
            'name': 'Alder',
            'type': 'champion',
            'order': 1,
            'location': '',
            'badge': '',
            'specialty': '',
            'sprite': SPRITE_BW.format(slug='alder'),
            'team': [
                mon('accelgor', 'Accelgor', 72, ['bug'], [
                    mv('bug-buzz', 'Bug Buzz'),
                    mv('energy-ball', 'Energy Ball'),
                    mv('focus-blast', 'Focus Blast'),
                    mv('acid-spray', 'Acid Spray'),
                ]),
                mon('bouffalant', 'Bouffalant', 72, ['normal'], [
                    mv('head-charge', 'Head Charge'),
                    mv('earthquake', 'Earthquake'),
                    mv('wild-charge', 'Wild Charge'),
                    mv('megahorn', 'Megahorn'),
                ]),
                mon('druddigon', 'Druddigon', 72, ['dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('crunch', 'Crunch'),
                    mv('flamethrower', 'Flamethrower'),
                    mv('revenge', 'Revenge'),
                ]),
                mon('vanilluxe', 'Vanilluxe', 72, ['ice'], [
                    mv('ice-beam', 'Ice Beam'),
                    mv('blizzard', 'Blizzard'),
                    mv('flash-cannon', 'Flash Cannon'),
                    mv('mirror-shot', 'Mirror Shot'),
                ]),
                mon('escavalier', 'Escavalier', 72, ['bug', 'steel'], [
                    mv('iron-head', 'Iron Head'),
                    mv('x-scissor', 'X-Scissor'),
                    mv('poison-jab', 'Poison Jab'),
                    mv('reversal', 'Reversal'),
                ]),
                mon('volcarona', 'Volcarona', 72, ['bug', 'fire'], [
                    mv('quiver-dance', 'Quiver Dance'),
                    mv('fiery-dance', 'Fiery Dance'),
                    mv('bug-buzz', 'Bug Buzz'),
                    mv('hurricane', 'Hurricane'),
                ]),
            ],
        },
        {
            'name': 'Iris',
            'type': 'champion',
            'order': 2,
            'location': '',
            'badge': '',
            'specialty': '',
            'sprite': SPRITE_BW2.format(slug='iris'),
            'team': [
                mon('haxorus', 'Haxorus', 57, ['dragon'], [
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('outrage', 'Outrage'),
                    mv('earthquake', 'Earthquake'),
                    mv('x-scissor', 'X-Scissor'),
                ]),
                mon('druddigon', 'Druddigon', 57, ['dragon'], [
                    mv('dragon-tail', 'Dragon Tail'),
                    mv('crunch', 'Crunch'),
                    mv('flamethrower', 'Flamethrower'),
                    mv('revenge', 'Revenge'),
                ]),
                mon('archeops', 'Archeops', 57, ['rock', 'flying'], [
                    mv('acrobatics', 'Acrobatics'),
                    mv('stone-edge', 'Stone Edge'),
                    mv('earth-power', 'Earth Power'),
                    mv('crunch', 'Crunch'),
                ]),
                mon('aggron', 'Aggron', 57, ['steel', 'rock'], [
                    mv('iron-tail', 'Iron Tail'),
                    mv('rock-slide', 'Rock Slide'),
                    mv('earthquake', 'Earthquake'),
                    mv('heavy-slam', 'Heavy Slam'),
                ]),
                mon('lapras', 'Lapras', 57, ['water', 'ice'], [
                    mv('surf', 'Surf'),
                    mv('ice-beam', 'Ice Beam'),
                    mv('thunderbolt', 'Thunderbolt'),
                    mv('psychic', 'Psychic'),
                ]),
                mon('hydreigon', 'Hydreigon', 59, ['dark', 'dragon'], [
                    mv('dragon-pulse', 'Dragon Pulse'),
                    mv('dark-pulse', 'Dark Pulse'),
                    mv('flamethrower', 'Flamethrower'),
                    mv('surf', 'Surf'),
                ]),
            ],
        },
    ]


def rematch_e4(name: str, order: int, specialty: str, sprite_slug: str, team: list[dict]) -> dict:
    return e4(name, order, specialty, sprite_slug, team)


def rematch_champion(name: str, order: int, specialty: str, sprite_slug: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'champion',
        'order': order,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE_BW2.format(slug=sprite_slug),
        'team': team,
    }


def build_rematch() -> list[dict]:
    return [
        rematch_e4('Shauntal', 1, 'rematchghost', 'shauntal', [
            mon('cofagrigus', 'Cofagrigus', 72, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('psychic', 'Psychic'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('protect', 'Protect'),
            ]),
            mon('drifblim', 'Drifblim', 72, ['ghost', 'flying'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('fly', 'Fly'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('hypnosis', 'Hypnosis'),
            ]),
            mon('froslass', 'Froslass', 72, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('double-team', 'Double Team'),
                mv('thunderbolt', 'Thunderbolt'),
            ]),
            mon('golurk', 'Golurk', 72, ['ground', 'ghost'], [
                mv('earthquake', 'Earthquake'),
                mv('shadow-punch', 'Shadow Punch'),
                mv('fly', 'Fly'),
                mv('iron-defense', 'Iron Defense'),
            ]),
            mon('chandelure', 'Chandelure', 74, ['ghost', 'fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('energy-ball', 'Energy Ball'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
        ]),
        rematch_e4('Grimsley', 2, 'rematchdark', 'grimsley', [
            mon('liepard', 'Liepard', 72, ['dark'], [
                mv('fake-out', 'Fake Out'),
                mv('night-slash', 'Night Slash'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('torment', 'Torment'),
            ]),
            mon('houndoom', 'Houndoom', 72, ['dark', 'fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('crunch', 'Crunch'),
                mv('sunny-day', 'Sunny Day'),
            ]),
            mon('scrafty', 'Scrafty', 72, ['dark', 'fighting'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('crunch', 'Crunch'),
                mv('dragon-dance', 'Dragon Dance'),
                mv('brick-break', 'Brick Break'),
            ]),
            mon('honchkrow', 'Honchkrow', 72, ['dark', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('night-slash', 'Night Slash'),
                mv('steel-wing', 'Steel Wing'),
                mv('heat-wave', 'Heat Wave'),
            ]),
            mon('krookodile', 'Krookodile', 72, ['ground', 'dark'], [
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rock-slide', 'Rock Slide'),
                mv('swagger', 'Swagger'),
            ]),
            mon('bisharp', 'Bisharp', 74, ['dark', 'steel'], [
                mv('iron-head', 'Iron Head'),
                mv('night-slash', 'Night Slash'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('metal-claw', 'Metal Claw'),
            ]),
        ]),
        rematch_e4('Caitlin', 3, 'rematchpsychic', 'caitlin', [
            mon('musharna', 'Musharna', 72, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('moonlight', 'Moonlight'),
                mv('hypnosis', 'Hypnosis'),
                mv('dream-eater', 'Dream Eater'),
            ]),
            mon('sigilyph', 'Sigilyph', 72, ['psychic', 'flying'], [
                mv('psychic', 'Psychic'),
                mv('air-slash', 'Air Slash'),
                mv('cosmic-power', 'Cosmic Power'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
            mon('reuniclus', 'Reuniclus', 72, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('focus-blast', 'Focus Blast'),
                mv('recover', 'Recover'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
            mon('gothitelle', 'Gothitelle', 72, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('energy-ball', 'Energy Ball'),
                mv('calm-mind', 'Calm Mind'),
            ]),
            mon('gallade', 'Gallade', 72, ['psychic', 'fighting'], [
                mv('psycho-cut', 'Psycho Cut'),
                mv('close-combat', 'Close Combat'),
                mv('night-slash', 'Night Slash'),
                mv('leaf-blade', 'Leaf Blade'),
            ]),
            mon('metagross', 'Metagross', 74, ['steel', 'psychic'], [
                mv('meteor-mash', 'Meteor Mash'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('earthquake', 'Earthquake'),
                mv('bullet-punch', 'Bullet Punch'),
            ]),
        ]),
        rematch_e4('Marshal', 4, 'rematchfighting', 'marshal', [
            mon('throh', 'Throh', 72, ['fighting'], [
                mv('storm-throw', 'Storm Throw'),
                mv('body-slam', 'Body Slam'),
                mv('bulk-up', 'Bulk Up'),
                mv('revenge', 'Revenge'),
            ]),
            mon('sawk', 'Sawk', 72, ['fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('retaliate', 'Retaliate'),
            ]),
            mon('mienshao', 'Mienshao', 72, ['fighting', 'psychic'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('u-turn', 'U-turn'),
                mv('acrobatics', 'Acrobatics'),
                mv('fake-out', 'Fake Out'),
            ]),
            mon('medicham', 'Medicham', 72, ['fighting', 'psychic'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('ice-punch', 'Ice Punch'),
                mv('thunder-punch', 'Thunder Punch'),
            ]),
            mon('lucario', 'Lucario', 72, ['fighting', 'steel'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('extreme-speed', 'Extreme Speed'),
            ]),
            mon('conkeldurr', 'Conkeldurr', 74, ['fighting'], [
                mv('hammer-arm', 'Hammer Arm'),
                mv('stone-edge', 'Stone Edge'),
                mv('mach-punch', 'Mach Punch'),
                mv('bulk-up', 'Bulk Up'),
            ]),
        ]),
        rematch_champion('Iris', 2, 'rematchdragon', 'iris', [
            mon('hydreigon', 'Hydreigon', 76, ['dark', 'dragon'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('flamethrower', 'Flamethrower'),
                mv('surf', 'Surf'),
            ]),
            mon('druddigon', 'Druddigon', 76, ['dragon'], [
                mv('dragon-tail', 'Dragon Tail'),
                mv('crunch', 'Crunch'),
                mv('flamethrower', 'Flamethrower'),
                mv('revenge', 'Revenge'),
            ]),
            mon('aggron', 'Aggron', 76, ['steel', 'rock'], [
                mv('iron-tail', 'Iron Tail'),
                mv('rock-slide', 'Rock Slide'),
                mv('earthquake', 'Earthquake'),
                mv('heavy-slam', 'Heavy Slam'),
            ]),
            mon('archeops', 'Archeops', 76, ['rock', 'flying'], [
                mv('acrobatics', 'Acrobatics'),
                mv('stone-edge', 'Stone Edge'),
                mv('earth-power', 'Earth Power'),
                mv('crunch', 'Crunch'),
            ]),
            mon('lapras', 'Lapras', 76, ['water', 'ice'], [
                mv('surf', 'Surf'),
                mv('ice-beam', 'Ice Beam'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('psychic', 'Psychic'),
            ]),
            mon('haxorus', 'Haxorus', 78, ['dragon'], [
                mv('dragon-dance', 'Dragon Dance'),
                mv('outrage', 'Outrage'),
                mv('earthquake', 'Earthquake'),
                mv('x-scissor', 'X-Scissor'),
            ]),
        ]),
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    gyms = build_gyms()
    e4_champ = build_e4_champion()
    rematch = build_rematch()
    skip = {'gym', 'elite4', 'champion'}
    rest = [t for t in current if t.get('type') not in skip]
    trainers[GAME_SLUG] = gyms + e4_champ + rematch + rest

    for g in data.get('games', []):
        if g.get('slug') == GAME_SLUG:
            g['trainer_count'] = len(trainers[GAME_SLUG])

    TRAINERS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(
        f'OK: {len(gyms)} gimnasios, {len(e4_champ)} E4+campeón, '
        f'{len(rematch)} revanchas en {GAME_SLUG}, {len(rest)} otros'
    )


if __name__ == '__main__':
    main()
