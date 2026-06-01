"""
Actualiza gimnasios, Alto Mando y campeón en data/trainers_db.json — Negro / Blanco.
Uso: python update_bw_gyms.py
Luego: python import_db.py --only trainers
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'black-white'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/black-white/{slug}.png'


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


def lillipup_12() -> dict:
    return mon('lillipup', 'Lillipup', 12, ['normal'], [
        mv('tackle', 'Tackle'),
        mv('leer', 'Leer'),
    ])


def striaton_leader(name: str, sprite_slug: str, specialty: str, pan: dict) -> dict:
    return {
        'name': name,
        'type': 'gym',
        'order': 1,
        'location': 'Striaton City',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite_slug),
        'team': [lillipup_12(), pan],
    }


def build_gyms() -> list[dict]:
    return [
        striaton_leader(
            'Cilan', 'cilan', 'badgegrass',
            mon('pansage', 'Pansage', 14, ['grass'], [
                mv('vine-whip', 'Vine Whip'),
                mv('work-up', 'Work Up'),
            ]),
        ),
        striaton_leader(
            'Chili', 'chili', 'badgefire',
            mon('pansear', 'Pansear', 14, ['fire'], [
                mv('incinerate', 'Incinerate'),
                mv('work-up', 'Work Up'),
            ]),
        ),
        striaton_leader(
            'Cress', 'cress', 'badgewater',
            mon('panpour', 'Panpour', 14, ['water'], [
                mv('water-gun', 'Water Gun'),
                mv('work-up', 'Work Up'),
            ]),
        ),
        {
            'name': 'Lenora',
            'type': 'gym',
            'order': 2,
            'location': 'Nacrene City',
            'badge': '',
            'specialty': 'badgenormal',
            'sprite': SPRITE.format(slug='lenora'),
            'team': [
                mon('herdier', 'Herdier', 18, ['normal'], [
                    mv('take-down', 'Take Down'),
                    mv('bite', 'Bite'),
                    mv('work-up', 'Work Up'),
                ]),
                mon('watchog', 'Watchog', 20, ['normal'], [
                    mv('hypnosis', 'Hypnosis'),
                    mv('confuse-ray', 'Confuse Ray'),
                    mv('crunch', 'Crunch'),
                    mv('super-fang', 'Super Fang'),
                ]),
            ],
        },
        {
            'name': 'Burgh',
            'type': 'gym',
            'order': 3,
            'location': 'Castelia City',
            'badge': '',
            'specialty': 'badgebug',
            'sprite': SPRITE.format(slug='burgh'),
            'team': [
                mon('whirlipede', 'Whirlipede', 21, ['bug', 'poison'], [
                    mv('bug-bite', 'Bug Bite'),
                    mv('poison-sting', 'Poison Sting'),
                    mv('protect', 'Protect'),
                ]),
                mon('dwebble', 'Dwebble', 21, ['bug', 'rock'], [
                    mv('rock-blast', 'Rock Blast'),
                    mv('bug-bite', 'Bug Bite'),
                    mv('withdraw', 'Withdraw'),
                ]),
                mon('leavanny', 'Leavanny', 23, ['bug', 'grass'], [
                    mv('razor-leaf', 'Razor Leaf'),
                    mv('bug-bite', 'Bug Bite'),
                    mv('string-shot', 'String Shot'),
                ]),
            ],
        },
        {
            'name': 'Elesa',
            'type': 'gym',
            'order': 4,
            'location': 'Nimbasa City',
            'badge': '',
            'specialty': 'badgeelectric',
            'sprite': SPRITE.format(slug='elesa'),
            'team': [
                mon('emolga', 'Emolga', 25, ['electric', 'flying'], [
                    mv('volt-switch', 'Volt Switch'),
                    mv('aerial-ace', 'Aerial Ace'),
                    mv('quick-attack', 'Quick Attack'),
                ]),
                mon('emolga', 'Emolga', 25, ['electric', 'flying'], [
                    mv('volt-switch', 'Volt Switch'),
                    mv('double-team', 'Double Team'),
                    mv('aerial-ace', 'Aerial Ace'),
                ]),
                mon('zebstrika', 'Zebstrika', 27, ['electric'], [
                    mv('flame-charge', 'Flame Charge'),
                    mv('spark', 'Spark'),
                    mv('pursuit', 'Pursuit'),
                ]),
            ],
        },
        {
            'name': 'Clay',
            'type': 'gym',
            'order': 5,
            'location': 'Driftveil City',
            'badge': '',
            'specialty': 'badgeground',
            'sprite': SPRITE.format(slug='clay'),
            'team': [
                mon('krokorok', 'Krokorok', 29, ['ground', 'dark'], [
                    mv('bite', 'Bite'),
                    mv('sand-tomb', 'Sand Tomb'),
                    mv('torment', 'Torment'),
                ]),
                mon('excadrill', 'Excadrill', 31, ['ground', 'steel'], [
                    mv('drill-run', 'Drill Run'),
                    mv('metal-claw', 'Metal Claw'),
                    mv('rock-slide', 'Rock Slide'),
                ]),
                mon('palpitoad', 'Palpitoad', 29, ['water', 'ground'], [
                    mv('mud-shot', 'Mud Shot'),
                    mv('bubble-beam', 'Bubble Beam'),
                    mv('supersonic', 'Supersonic'),
                ]),
            ],
        },
        {
            'name': 'Skyla',
            'type': 'gym',
            'order': 6,
            'location': 'Mistralton City',
            'badge': '',
            'specialty': 'badgeflying',
            'sprite': SPRITE.format(slug='skyla'),
            'team': [
                mon('swoobat', 'Swoobat', 33, ['psychic', 'flying'], [
                    mv('acrobatics', 'Acrobatics'),
                    mv('confusion', 'Confusion'),
                    mv('assurance', 'Assurance'),
                ]),
                mon('unfezant', 'Unfezant', 33, ['normal', 'flying'], [
                    mv('air-slash', 'Air Slash'),
                    mv('quick-attack', 'Quick Attack'),
                    mv('detect', 'Detect'),
                ]),
                mon('swanna', 'Swanna', 35, ['water', 'flying'], [
                    mv('surf', 'Surf'),
                    mv('air-slash', 'Air Slash'),
                    mv('aqua-ring', 'Aqua Ring'),
                ]),
            ],
        },
        {
            'name': 'Brycen',
            'type': 'gym',
            'order': 7,
            'location': 'Icirrus City',
            'badge': '',
            'specialty': 'badgeice',
            'sprite': SPRITE.format(slug='brycen'),
            'team': [
                mon('vanillish', 'Vanillish', 37, ['ice'], [
                    mv('ice-beam', 'Ice Beam'),
                    mv('mirror-shot', 'Mirror Shot'),
                    mv('acid-armor', 'Acid Armor'),
                ]),
                mon('cryogonal', 'Cryogonal', 37, ['ice'], [
                    mv('ice-beam', 'Ice Beam'),
                    mv('confuse-ray', 'Confuse Ray'),
                    mv('recover', 'Recover'),
                ]),
                mon('beartic', 'Beartic', 39, ['ice'], [
                    mv('icicle-crash', 'Icicle Crash'),
                    mv('slash', 'Slash'),
                    mv('aqua-jet', 'Aqua Jet'),
                ]),
            ],
        },
        {
            'name': 'Drayden',
            'type': 'gym',
            'order': 8,
            'location': 'Opelucid City',
            'badge': '',
            'specialty': 'badgedragon',
            'sprite': SPRITE.format(slug='drayden'),
            'team': [
                mon('druddigon', 'Druddigon', 41, ['dragon'], [
                    mv('dragon-tail', 'Dragon Tail'),
                    mv('slash', 'Slash'),
                    mv('revenge', 'Revenge'),
                ]),
                mon('flygon', 'Flygon', 41, ['ground', 'dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('earth-power', 'Earth Power'),
                    mv('crunch', 'Crunch'),
                ]),
                mon('haxorus', 'Haxorus', 43, ['dragon'], [
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('slash', 'Slash'),
                ]),
            ],
        },
        {
            'name': 'Iris',
            'type': 'gym',
            'order': 8,
            'location': 'Opelucid City',
            'badge': '',
            'specialty': 'badgedragon',
            'sprite': SPRITE.format(slug='iris'),
            'team': [
                mon('fraxure', 'Fraxure', 41, ['dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('slash', 'Slash'),
                    mv('dragon-dance', 'Dragon Dance'),
                ]),
                mon('druddigon', 'Druddigon', 41, ['dragon'], [
                    mv('revenge', 'Revenge'),
                    mv('dragon-tail', 'Dragon Tail'),
                    mv('crunch', 'Crunch'),
                ]),
                mon('haxorus', 'Haxorus', 43, ['dragon'], [
                    mv('dragon-pulse', 'Dragon Pulse'),
                    mv('dragon-dance', 'Dragon Dance'),
                    mv('outrage', 'Outrage'),
                ]),
            ],
        },
    ]


def e4(name: str, order: int, specialty: str, sprite_slug: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'elite4',
        'order': order,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite_slug),
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
        ]),
        e4('Grimsley', 2, 'grimsleydark', 'grimsley', [
            mon('scrafty', 'Scrafty', 48, ['dark', 'fighting'], [
                mv('crunch', 'Crunch'),
                mv('high-jump-kick', 'High Jump Kick'),
                mv('dragon-dance', 'Dragon Dance'),
                mv('brick-break', 'Brick Break'),
            ]),
            mon('krookodile', 'Krookodile', 48, ['ground', 'dark'], [
                mv('earthquake', 'Earthquake'),
                mv('crunch', 'Crunch'),
                mv('rock-slide', 'Rock Slide'),
                mv('swagger', 'Swagger'),
            ]),
            mon('liepard', 'Liepard', 48, ['dark'], [
                mv('night-slash', 'Night Slash'),
                mv('fake-out', 'Fake Out'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('torment', 'Torment'),
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
                mv('dream-eater', 'Dream Eater'),
                mv('moonlight', 'Moonlight'),
                mv('hypnosis', 'Hypnosis'),
            ]),
            mon('gothitelle', 'Gothitelle', 48, ['psychic'], [
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
                mv('revenge', 'Revenge'),
                mv('bulk-up', 'Bulk Up'),
            ]),
            mon('sawk', 'Sawk', 48, ['fighting'], [
                mv('close-combat', 'Close Combat'),
                mv('rock-slide', 'Rock Slide'),
                mv('earthquake', 'Earthquake'),
                mv('retaliate', 'Retaliate'),
            ]),
            mon('mienshao', 'Mienshao', 48, ['fighting', 'psychic'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('u-turn', 'U-turn'),
                mv('acrobatics', 'Acrobatics'),
                mv('fake-out', 'Fake Out'),
            ]),
        ]),
        {
            'name': 'Alder',
            'type': 'champion',
            'order': 1,
            'location': '',
            'badge': '',
            'specialty': '',
            'sprite': SPRITE.format(slug='alder'),
            'team': [
                mon('accelgor', 'Accelgor', 75, ['bug'], [
                    mv('bug-buzz', 'Bug Buzz'),
                    mv('energy-ball', 'Energy Ball'),
                    mv('acid-spray', 'Acid Spray'),
                    mv('focus-blast', 'Focus Blast'),
                ]),
                mon('bouffalant', 'Bouffalant', 75, ['normal'], [
                    mv('head-charge', 'Head Charge'),
                    mv('earthquake', 'Earthquake'),
                    mv('megahorn', 'Megahorn'),
                    mv('wild-charge', 'Wild Charge'),
                ]),
                mon('druddigon', 'Druddigon', 75, ['dragon'], [
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('crunch', 'Crunch'),
                    mv('revenge', 'Revenge'),
                    mv('flamethrower', 'Flamethrower'),
                ]),
                mon('vanilluxe', 'Vanilluxe', 75, ['ice'], [
                    mv('ice-beam', 'Ice Beam'),
                    mv('flash-cannon', 'Flash Cannon'),
                    mv('mirror-shot', 'Mirror Shot'),
                    mv('blizzard', 'Blizzard'),
                ]),
                mon('escavalier', 'Escavalier', 75, ['bug', 'steel'], [
                    mv('iron-head', 'Iron Head'),
                    mv('x-scissor', 'X-Scissor'),
                    mv('reversal', 'Reversal'),
                    mv('poison-jab', 'Poison Jab'),
                ]),
                mon('volcarona', 'Volcarona', 75, ['bug', 'fire'], [
                    mv('fiery-dance', 'Fiery Dance'),
                    mv('bug-buzz', 'Bug Buzz'),
                    mv('hurricane', 'Hurricane'),
                    mv('quiver-dance', 'Quiver Dance'),
                ]),
            ],
        },
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    gyms = build_gyms()
    e4_champ = build_e4_champion()
    skip = {'gym', 'elite4', 'champion'}
    rest = [t for t in current if t.get('type') not in skip]
    trainers[GAME_SLUG] = gyms + e4_champ + rest

    for g in data.get('games', []):
        if g.get('slug') == GAME_SLUG:
            g['trainer_count'] = len(trainers[GAME_SLUG])

    TRAINERS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(
        f'OK: {len(gyms)} gimnasios, {len(e4_champ)} E4+campeón en {GAME_SLUG}, '
        f'{len(rest)} otros'
    )


if __name__ == '__main__':
    main()
