"""
Gimnasios Espada / Escudo — versiones exclusivas como entradas separadas (Bea/Allister, Gordie/Melony).
Uso: python update_swsh_gyms.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'sword-shield'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/swsh/{slug}.jpg'


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
        gym('Milo', 1, 'Turffield', 'badgegrass', 'milo', [
            mon('gossifleur', 'Gossifleur', 19, ['grass'], [
                mv('rapid-spin', 'Rapid Spin'),
                mv('leafage', 'Leafage'),
                mv('round', 'Round'),
                mv('magical-leaf', 'Magical Leaf'),
            ]),
            mon('eldegoss', 'Eldegoss', 20, ['grass'], [
                mv('round', 'Round'),
                mv('leafage', 'Leafage'),
                mv('cotton-spore', 'Cotton Spore'),
                mv('razor-leaf', 'Razor Leaf'),
            ]),
        ]),
        gym('Nessa', 2, 'Hulbury', 'badgewater', 'nessa', [
            mon('goldeen', 'Goldeen', 22, ['water'], [
                mv('water-pulse', 'Water Pulse'),
                mv('horn-attack', 'Horn Attack'),
                mv('agility', 'Agility'),
                mv('fury-attack', 'Fury Attack'),
            ]),
            mon('arrokuda', 'Arrokuda', 23, ['water'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('bite', 'Bite'),
                mv('fury-attack', 'Fury Attack'),
                mv('scary-face', 'Scary Face'),
            ]),
            mon('drednaw', 'Drednaw', 24, ['water', 'rock'], [
                mv('razor-shell', 'Razor Shell'),
                mv('bite', 'Bite'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('water-gun', 'Water Gun'),
            ]),
        ]),
        gym('Kabu', 3, 'Motostoke', 'badgefire', 'kabu', [
            mon('ninetales', 'Ninetales', 25, ['fire'], [
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('fire-spin', 'Fire Spin'),
                mv('quick-attack', 'Quick Attack'),
                mv('confuse-ray', 'Confuse Ray'),
            ]),
            mon('arcanine', 'Arcanine', 25, ['fire'], [
                mv('flame-wheel', 'Flame Wheel'),
                mv('bite', 'Bite'),
                mv('roar', 'Roar'),
                mv('agility', 'Agility'),
            ]),
            mon('centiskorch', 'Centiskorch', 27, ['fire', 'bug'], [
                mv('flame-wheel', 'Flame Wheel'),
                mv('bug-bite', 'Bug Bite'),
                mv('coil', 'Coil'),
                mv('smokescreen', 'Smokescreen'),
            ]),
        ]),
        gym('Bea', 4, 'Stow-on-Side', 'beafighting', 'bea', [
            mon('hitmontop', 'Hitmontop', 34, ['fighting'], [
                mv('triple-kick', 'Triple Kick'),
                mv('counter', 'Counter'),
                mv('quick-attack', 'Quick Attack'),
                mv('pursuit', 'Pursuit'),
            ]),
            mon('pangoro', 'Pangoro', 34, ['fighting', 'dark'], [
                mv('circle-throw', 'Circle Throw'),
                mv('night-slash', 'Night Slash'),
                mv('work-up', 'Work Up'),
                mv('karate-chop', 'Karate Chop'),
            ]),
            mon('sirfetchd', "Sirfetch'd", 35, ['fighting'], [
                mv('brick-break', 'Brick Break'),
                mv('brutal-swing', 'Brutal Swing'),
                mv('swords-dance', 'Swords Dance'),
                mv('detect', 'Detect'),
            ]),
            mon('machamp', 'Machamp', 36, ['fighting'], [
                mv('revenge', 'Revenge'),
                mv('strength', 'Strength'),
                mv('scary-face', 'Scary Face'),
                mv('seismic-toss', 'Seismic Toss'),
            ]),
        ]),
        gym('Allister', 4, 'Stow-on-Side', 'allisterghost', 'allister', [
            mon('yamask-galar', 'Yamask', 34, ['ground', 'ghost'], [
                mv('brutal-swing', 'Brutal Swing'),
                mv('hex', 'Hex'),
                mv('disable', 'Disable'),
                mv('protect', 'Protect'),
            ]),
            mon('mimikyu', 'Mimikyu', 34, ['ghost', 'fairy'], [
                mv('shadow-sneak', 'Shadow Sneak'),
                mv('slash', 'Slash'),
                mv('baby-doll-eyes', 'Baby-Doll Eyes'),
                mv('hone-claws', 'Hone Claws'),
            ]),
            mon('cursola', 'Cursola', 35, ['ghost'], [
                mv('ancient-power', 'Ancient Power'),
                mv('hex', 'Hex'),
                mv('strength-sap', 'Strength Sap'),
                mv('curse', 'Curse'),
            ]),
            mon('gengar', 'Gengar', 36, ['ghost', 'poison'], [
                mv('venoshock', 'Venoshock'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('hypnosis', 'Hypnosis'),
                mv('payback', 'Payback'),
            ]),
        ]),
        gym('Opal', 5, 'Ballonlea', 'badgefairy', 'opal', [
            mon('weezing-galar', 'Weezing', 36, ['poison', 'fairy'], [
                mv('sludge', 'Sludge'),
                mv('fairy-wind', 'Fairy Wind'),
                mv('tackle', 'Tackle'),
                mv('smokescreen', 'Smokescreen'),
            ]),
            mon('mawile', 'Mawile', 36, ['steel', 'fairy'], [
                mv('draining-kiss', 'Draining Kiss'),
                mv('crunch', 'Crunch'),
                mv('iron-defense', 'Iron Defense'),
                mv('astonish', 'Astonish'),
            ]),
            mon('togekiss', 'Togekiss', 37, ['fairy', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('draining-kiss', 'Draining Kiss'),
                mv('ancient-power', 'Ancient Power'),
                mv('aura-sphere', 'Aura Sphere'),
            ]),
            mon('alcremie', 'Alcremie', 38, ['fairy'], [
                mv('draining-kiss', 'Draining Kiss'),
                mv('acid-armor', 'Acid Armor'),
                mv('sweet-kiss', 'Sweet Kiss'),
                mv('dazzling-gleam', 'Dazzling Gleam'),
            ]),
        ]),
        gym('Gordie', 6, 'Circhester', 'gordierock', 'gordie', [
            mon('barbaracle', 'Barbaracle', 40, ['rock', 'water'], [
                mv('shell-smash', 'Shell Smash'),
                mv('razor-shell', 'Razor Shell'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('cross-chop', 'Cross Chop'),
            ]),
            mon('shuckle', 'Shuckle', 40, ['bug', 'rock'], [
                mv('struggle-bug', 'Struggle Bug'),
                mv('rock-tomb', 'Rock Tomb'),
                mv('power-split', 'Power Split'),
                mv('guard-split', 'Guard Split'),
            ]),
            mon('stonjourner', 'Stonjourner', 41, ['rock'], [
                mv('rock-slide', 'Rock Slide'),
                mv('body-slam', 'Body Slam'),
                mv('stone-edge', 'Stone Edge'),
                mv('wide-guard', 'Wide Guard'),
            ]),
            mon('coalossal', 'Coalossal', 42, ['rock', 'fire'], [
                mv('tar-shot', 'Tar Shot'),
                mv('heat-crash', 'Heat Crash'),
                mv('rock-blast', 'Rock Blast'),
                mv('stealth-rock', 'Stealth Rock'),
            ]),
        ]),
        gym('Melony', 6, 'Circhester', 'melonyice', 'melony', [
            mon('frosmoth', 'Frosmoth', 40, ['ice', 'bug'], [
                mv('icy-wind', 'Icy Wind'),
                mv('bug-buzz', 'Bug Buzz'),
                mv('feather-dance', 'Feather Dance'),
                mv('hail', 'Hail'),
            ]),
            mon('darmanitan-galar-standard', 'Darmanitan', 40, ['ice'], [
                mv('fire-fang', 'Fire Fang'),
                mv('icicle-crash', 'Icicle Crash'),
                mv('headbutt', 'Headbutt'),
                mv('taunt', 'Taunt'),
            ]),
            mon('eiscue', 'Eiscue', 41, ['ice'], [
                mv('aurora-veil', 'Aurora Veil'),
                mv('ice-beam', 'Ice Beam'),
                mv('surf', 'Surf'),
                mv('headbutt', 'Headbutt'),
            ]),
            mon('lapras', 'Lapras', 42, ['water', 'ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('surf', 'Surf'),
                mv('body-slam', 'Body Slam'),
                mv('sing', 'Sing'),
            ]),
        ]),
        gym('Piers', 7, 'Spikemuth', 'badgedark', 'piers', [
            mon('scrafty', 'Scrafty', 44, ['dark', 'fighting'], [
                mv('fake-out', 'Fake Out'),
                mv('brick-break', 'Brick Break'),
                mv('sand-attack', 'Sand Attack'),
                mv('payback', 'Payback'),
            ]),
            mon('malamar', 'Malamar', 45, ['dark', 'psychic'], [
                mv('night-slash', 'Night Slash'),
                mv('foul-play', 'Foul Play'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('topsy-turvy', 'Topsy-Turvy'),
            ]),
            mon('skuntank', 'Skuntank', 45, ['poison', 'dark'], [
                mv('sucker-punch', 'Sucker Punch'),
                mv('toxic', 'Toxic'),
                mv('screech', 'Screech'),
                mv('flamethrower', 'Flamethrower'),
            ]),
            mon('obstagoon', 'Obstagoon', 46, ['dark', 'normal'], [
                mv('obstruct', 'Obstruct'),
                mv('throat-chop', 'Throat Chop'),
                mv('counter', 'Counter'),
                mv('shadow-claw', 'Shadow Claw'),
            ]),
        ]),
        gym('Raihan', 8, 'Hammerlocke', 'raihandragon', 'raihan', [
            mon('gigalith', 'Gigalith', 46, ['rock'], [
                mv('stealth-rock', 'Stealth Rock'),
                mv('body-press', 'Body Press'),
                mv('rock-blast', 'Rock Blast'),
                mv('sandstorm', 'Sandstorm'),
            ]),
            mon('flygon', 'Flygon', 47, ['ground', 'dragon'], [
                mv('dragon-rush', 'Dragon Rush'),
                mv('crunch', 'Crunch'),
                mv('fire-punch', 'Fire Punch'),
                mv('steel-wing', 'Steel Wing'),
            ]),
            mon('sandaconda', 'Sandaconda', 46, ['ground'], [
                mv('glare', 'Glare'),
                mv('fire-fang', 'Fire Fang'),
                mv('earth-power', 'Earth Power'),
                mv('protect', 'Protect'),
            ]),
            mon('duraludon', 'Duraludon', 48, ['steel', 'dragon'], [
                mv('breaking-swipe', 'Breaking Swipe'),
                mv('body-press', 'Body Press'),
                mv('iron-head', 'Iron Head'),
                mv('stone-edge', 'Stone Edge'),
            ]),
        ]),
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    gyms = build_gyms()
    rest = [t for t in current if t.get('type') != 'gym']
    trainers[GAME_SLUG] = gyms + rest

    for g in data.get('games', []):
        if g.get('slug') == GAME_SLUG:
            g['trainer_count'] = len(trainers[GAME_SLUG])

    TRAINERS_PATH.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'OK: {len(gyms)} gimnasios en {GAME_SLUG} ({len(rest)} otros entrenadores)')


if __name__ == '__main__':
    main()
