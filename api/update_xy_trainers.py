"""
Actualiza gimnasios, Alto Mando y campeona en data/trainers_db.json — Pokémon X / Y.
Uso: python update_xy_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'x-y'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/x-y/{slug}.jpg'


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
    sprite_slug: str,
    team: list[dict],
) -> dict:
    return {
        'name': name,
        'type': 'gym',
        'order': order,
        'location': location,
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite_slug),
        'team': team,
    }


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


def build_trainers() -> list[dict]:
    return [
        gym('Viola', 1, 'Santalune City', 'badgebug', 'viola', [
            mon('surskit', 'Surskit', 10, ['bug', 'water'], [
                mv('bubble', 'Bubble'),
                mv('quick-attack', 'Quick Attack'),
                mv('sweet-scent', 'Sweet Scent'),
            ]),
            mon('vivillon', 'Vivillon', 12, ['bug', 'flying'], [
                mv('struggle-bug', 'Struggle Bug'),
                mv('stun-spore', 'Stun Spore'),
                mv('gust', 'Gust'),
                mv('light-screen', 'Light Screen'),
            ]),
        ]),
        gym('Grant', 2, 'Cyllage City', 'badgerock', 'grant', [
            mon('amaura', 'Amaura', 25, ['rock', 'ice'], [
                mv('icy-wind', 'Icy Wind'),
                mv('rock-throw', 'Rock Throw'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('aurora-beam', 'Aurora Beam'),
            ]),
            mon('tyrunt', 'Tyrunt', 25, ['rock', 'dragon'], [
                mv('bite', 'Bite'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('dragon-tail', 'Dragon Tail'),
                mv('stomp', 'Stomp'),
            ]),
        ]),
        gym('Korrina', 3, 'Shalour City', 'badgefighting', 'korrina', [
            mon('mienfoo', 'Mienfoo', 29, ['fighting'], [
                mv('drain-punch', 'Drain Punch'),
                mv('knock-off', 'Knock Off'),
                mv('acrobatics', 'Acrobatics'),
                mv('fake-out', 'Fake Out'),
            ]),
            mon('machoke', 'Machoke', 28, ['fighting'], [
                mv('karate-chop', 'Karate Chop'),
                mv('rock-slide', 'Rock Slide'),
                mv('bulk-up', 'Bulk Up'),
                mv('strength', 'Strength'),
            ]),
            mon('hawlucha', 'Hawlucha', 32, ['fighting', 'flying'], [
                mv('flying-press', 'Flying Press'),
                mv('acrobatics', 'Acrobatics'),
                mv('swords-dance', 'Swords Dance'),
                mv('bounce', 'Bounce'),
            ]),
        ]),
        gym('Ramos', 4, 'Coumarine City', 'badgegrass', 'ramos', [
            mon('jumpluff', 'Jumpluff', 30, ['grass', 'flying'], [
                mv('acrobatics', 'Acrobatics'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('cotton-spore', 'Cotton Spore'),
                mv('giga-drain', 'Giga Drain'),
            ]),
            mon('weepinbell', 'Weepinbell', 31, ['grass', 'poison'], [
                mv('razor-leaf', 'Razor Leaf'),
                mv('acid', 'Acid'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('wrap', 'Wrap'),
            ]),
            mon('gogoat', 'Gogoat', 34, ['grass'], [
                mv('horn-leech', 'Horn Leech'),
                mv('earthquake', 'Earthquake'),
                mv('milk-drink', 'Milk Drink'),
                mv('leaf-blade', 'Leaf Blade'),
            ]),
        ]),
        gym('Clemont', 5, 'Lumiose City', 'badgeelectric', 'clemont', [
            mon('emolga', 'Emolga', 35, ['electric', 'flying'], [
                mv('volt-switch', 'Volt Switch'),
                mv('acrobatics', 'Acrobatics'),
                mv('electro-ball', 'Electro Ball'),
                mv('quick-attack', 'Quick Attack'),
            ]),
            mon('magneton', 'Magneton', 35, ['electric', 'steel'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('flash-cannon', 'Flash Cannon'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('tri-attack', 'Tri Attack'),
            ]),
            mon('heliolisk', 'Heliolisk', 37, ['electric', 'normal'], [
                mv('parabolic-charge', 'Parabolic Charge'),
                mv('hyper-voice', 'Hyper Voice'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('volt-switch', 'Volt Switch'),
            ]),
        ]),
        gym('Valerie', 6, 'Laverre City', 'badgefairy', 'valerie', [
            mon('mawile', 'Mawile', 38, ['steel', 'fairy'], [
                mv('play-rough', 'Play Rough'),
                mv('iron-head', 'Iron Head'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('fake-tears', 'Fake Tears'),
            ]),
            mon('mr-mime', 'Mr. Mime', 39, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('light-screen', 'Light Screen'),
                mv('reflect', 'Reflect'),
            ]),
            mon('sylveon', 'Sylveon', 42, ['fairy'], [
                mv('moonblast', 'Moonblast'),
                mv('calm-mind', 'Calm Mind'),
                mv('swift', 'Swift'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
        ]),
        gym('Olympia', 7, 'Anistar City', 'badgepsychic', 'olympia', [
            mon('sigilyph', 'Sigilyph', 44, ['psychic', 'flying'], [
                mv('psychic', 'Psychic'),
                mv('air-slash', 'Air Slash'),
                mv('cosmic-power', 'Cosmic Power'),
                mv('light-screen', 'Light Screen'),
            ]),
            mon('slowking', 'Slowking', 45, ['water', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('surf', 'Surf'),
                mv('slack-off', 'Slack Off'),
                mv('fire-blast', 'Fire Blast'),
            ]),
            mon('meowstic-male', 'Meowstic', 48, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('light-screen', 'Light Screen'),
            ]),
        ]),
        gym('Wulfric', 8, 'Snowbelle City', 'badgeice', 'wulfric', [
            mon('abomasnow', 'Abomasnow', 56, ['grass', 'ice'], [
                mv('ice-shard', 'Ice Shard'),
                mv('wood-hammer', 'Wood Hammer'),
                mv('earthquake', 'Earthquake'),
                mv('blizzard', 'Blizzard'),
            ]),
            mon('cryogonal', 'Cryogonal', 55, ['ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('light-screen', 'Light Screen'),
                mv('recover', 'Recover'),
                mv('confuse-ray', 'Confuse Ray'),
            ]),
            mon('avalugg', 'Avalugg', 59, ['ice'], [
                mv('avalanche', 'Avalanche'),
                mv('recover', 'Recover'),
                mv('crunch', 'Crunch'),
                mv('iron-defense', 'Iron Defense'),
            ]),
        ]),
        e4('Malva', 1, 'malvafire', 'malva', [
            mon('pyroar', 'Pyroar', 63, ['fire', 'normal'], [
                mv('flamethrower', 'Flamethrower'),
                mv('hyper-voice', 'Hyper Voice'),
                mv('noble-roar', 'Noble Roar'),
                mv('crunch', 'Crunch'),
            ]),
            mon('torkoal', 'Torkoal', 63, ['fire'], [
                mv('lava-plume', 'Lava Plume'),
                mv('protect', 'Protect'),
                mv('curse', 'Curse'),
                mv('body-slam', 'Body Slam'),
            ]),
            mon('chandelure', 'Chandelure', 63, ['ghost', 'fire'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('flamethrower', 'Flamethrower'),
                mv('energy-ball', 'Energy Ball'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
            mon('talonflame', 'Talonflame', 65, ['fire', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('flare-blitz', 'Flare Blitz'),
                mv('roost', 'Roost'),
                mv('swords-dance', 'Swords Dance'),
            ]),
        ]),
        e4('Siebold', 2, 'sieboldwater', 'siebold', [
            mon('clawitzer', 'Clawitzer', 63, ['water'], [
                mv('aura-sphere', 'Aura Sphere'),
                mv('dark-pulse', 'Dark Pulse'),
                mv('water-pulse', 'Water Pulse'),
                mv('ice-beam', 'Ice Beam'),
            ]),
            mon('gyarados', 'Gyarados', 63, ['water', 'flying'], [
                mv('aqua-tail', 'Aqua Tail'),
                mv('crunch', 'Crunch'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
            mon('starmie', 'Starmie', 63, ['water', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('surf', 'Surf'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('ice-beam', 'Ice Beam'),
            ]),
            mon('barbaracle', 'Barbaracle', 65, ['rock', 'water'], [
                mv('stone-edge', 'Stone Edge'),
                mv('cross-chop', 'Cross Chop'),
                mv('razor-shell', 'Razor Shell'),
                mv('shell-smash', 'Shell Smash'),
            ]),
        ]),
        e4('Wikstrom', 3, 'wikstromsteel', 'wikstrom', [
            mon('klefki', 'Klefki', 63, ['steel', 'fairy'], [
                mv('flash-cannon', 'Flash Cannon'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('spikes', 'Spikes'),
            ]),
            mon('probopass', 'Probopass', 63, ['rock', 'steel'], [
                mv('power-gem', 'Power Gem'),
                mv('earth-power', 'Earth Power'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('flash-cannon', 'Flash Cannon'),
            ]),
            mon('scizor', 'Scizor', 63, ['bug', 'steel'], [
                mv('bullet-punch', 'Bullet Punch'),
                mv('x-scissor', 'X-Scissor'),
                mv('swords-dance', 'Swords Dance'),
                mv('night-slash', 'Night Slash'),
            ]),
            mon('aegislash', 'Aegislash', 65, ['steel', 'ghost'], [
                mv('kings-shield', "King's Shield"),
                mv('shadow-ball', 'Shadow Ball'),
                mv('sacred-sword', 'Sacred Sword'),
                mv('iron-head', 'Iron Head'),
            ]),
        ]),
        e4('Drasna', 4, 'drasnadragon', 'drasna', [
            mon('dragalge', 'Dragalge', 63, ['poison', 'dragon'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('surf', 'Surf'),
                mv('focus-blast', 'Focus Blast'),
            ]),
            mon('druddigon', 'Druddigon', 63, ['dragon'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('crunch', 'Crunch'),
                mv('flamethrower', 'Flamethrower'),
                mv('revenge', 'Revenge'),
            ]),
            mon('altaria', 'Altaria', 63, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('moonblast', 'Moonblast'),
                mv('cotton-guard', 'Cotton Guard'),
                mv('roost', 'Roost'),
            ]),
            mon('noivern', 'Noivern', 65, ['flying', 'dragon'], [
                mv('draco-meteor', 'Draco Meteor'),
                mv('hurricane', 'Hurricane'),
                mv('flamethrower', 'Flamethrower'),
                mv('boomburst', 'Boomburst'),
            ]),
        ]),
        {
            'name': 'Diantha',
            'type': 'champion',
            'order': 1,
            'location': '',
            'badge': '',
            'specialty': '',
            'sprite': SPRITE.format(slug='diantha'),
            'team': [
                mon('hawlucha', 'Hawlucha', 64, ['fighting', 'flying'], [
                    mv('flying-press', 'Flying Press'),
                    mv('x-scissor', 'X-Scissor'),
                    mv('swords-dance', 'Swords Dance'),
                    mv('poison-jab', 'Poison Jab'),
                ]),
                mon('tyrantrum', 'Tyrantrum', 65, ['rock', 'dragon'], [
                    mv('head-smash', 'Head Smash'),
                    mv('dragon-claw', 'Dragon Claw'),
                    mv('earthquake', 'Earthquake'),
                    mv('crunch', 'Crunch'),
                ]),
                mon('aurorus', 'Aurorus', 65, ['rock', 'ice'], [
                    mv('ice-beam', 'Ice Beam'),
                    mv('thunderbolt', 'Thunderbolt'),
                    mv('reflect', 'Reflect'),
                    mv('light-screen', 'Light Screen'),
                ]),
                mon('gourgeist', 'Gourgeist', 65, ['ghost', 'grass'], [
                    mv('shadow-ball', 'Shadow Ball'),
                    mv('seed-bomb', 'Seed Bomb'),
                    mv('trick-or-treat', 'Trick-or-Treat'),
                    mv('will-o-wisp', 'Will-O-Wisp'),
                ]),
                mon('goodra', 'Goodra', 66, ['dragon'], [
                    mv('dragon-pulse', 'Dragon Pulse'),
                    mv('muddy-water', 'Muddy Water'),
                    mv('thunderbolt', 'Thunderbolt'),
                    mv('flamethrower', 'Flamethrower'),
                ]),
                mon('gardevoir-mega', 'Gardevoir (Mega)', 68, ['psychic', 'fairy'], [
                    mv('moonblast', 'Moonblast'),
                    mv('psychic', 'Psychic'),
                    mv('thunderbolt', 'Thunderbolt'),
                    mv('focus-blast', 'Focus Blast'),
                ]),
            ],
        },
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    built = build_trainers()
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
    gyms = sum(1 for t in built if t['type'] == 'gym')
    e4 = sum(1 for t in built if t['type'] == 'elite4')
    champ = sum(1 for t in built if t['type'] == 'champion')
    print(f'OK: {gyms} gimnasios, {e4} E4, {champ} campeona en {GAME_SLUG}')


if __name__ == '__main__':
    main()
