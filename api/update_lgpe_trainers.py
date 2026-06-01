"""
Actualiza gimnasios, Alto Mando y campeón — Let's Go Pikachu / Eevee.
Uso: python update_lgpe_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'lets-go-pikachu-eevee'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/lgpe/{slug}.jpg'


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


def gym(name: str, order: int, location: str, specialty: str, sprite: str, team: list[dict]) -> dict:
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


def trace_slot6(species: str, display: str) -> dict:
    return mon(species, display, 57, ['electric'], [
        mv('thunderbolt', 'Thunderbolt'),
        mv('thunder-wave', 'Thunder Wave'),
        mv('double-kick', 'Double Kick'),
        mv('slam', 'Slam'),
    ])


def trace_team(slot6: dict) -> list[dict]:
    return [
        mon('pidgeot', 'Pidgeot', 56, ['normal', 'flying'], [
            mv('brave-bird', 'Brave Bird'),
            mv('wing-attack', 'Wing Attack'),
            mv('quick-attack', 'Quick Attack'),
            mv('roost', 'Roost'),
        ]),
        mon('vileplume', 'Vileplume', 56, ['grass', 'poison'], [
            mv('petal-dance', 'Petal Dance'),
            mv('acid', 'Acid'),
            mv('sleep-powder', 'Sleep Powder'),
            mv('moonblast', 'Moonblast'),
        ]),
        mon('marowak', 'Marowak', 56, ['ground'], [
            mv('earthquake', 'Earthquake'),
            mv('bonemerang', 'Bonemerang'),
            mv('rock-slide', 'Rock Slide'),
            mv('thrash', 'Thrash'),
        ]),
        mon('rapidash', 'Rapidash', 56, ['fire'], [
            mv('fire-blast', 'Fire Blast'),
            mv('stomp', 'Stomp'),
            mv('agility', 'Agility'),
            mv('fire-spin', 'Fire Spin'),
        ]),
        mon('slowbro', 'Slowbro', 56, ['water', 'psychic'], [
            mv('psychic', 'Psychic'),
            mv('surf', 'Surf'),
            mv('flamethrower', 'Flamethrower'),
            mv('slack-off', 'Slack Off'),
        ]),
        slot6,
    ]


def build_trainers() -> list[dict]:
    jolteon = trace_slot6('jolteon', 'Jolteon')
    raichu = trace_slot6('raichu', 'Raichu')
    return [
        gym('Brock', 1, 'Pewter City', 'badgerock', 'brock', [
            mon('geodude', 'Geodude', 11, ['rock', 'ground'], [
                mv('tackle', 'Tackle'),
                mv('rock-throw', 'Rock Throw'),
                mv('defense-curl', 'Defense Curl'),
                mv('mud-sport', 'Mud Sport'),
            ]),
            mon('onix', 'Onix', 12, ['rock', 'ground'], [
                mv('rock-throw', 'Rock Throw'),
                mv('bind', 'Bind'),
                mv('slam', 'Slam'),
                mv('harden', 'Harden'),
            ]),
        ]),
        gym('Misty', 2, 'Cerulean City', 'badgewater', 'misty', [
            mon('psyduck', 'Psyduck', 18, ['water'], [
                mv('water-gun', 'Water Gun'),
                mv('scratch', 'Scratch'),
                mv('tail-whip', 'Tail Whip'),
                mv('disable', 'Disable'),
            ]),
            mon('starmie', 'Starmie', 19, ['water', 'psychic'], [
                mv('water-pulse', 'Water Pulse'),
                mv('swift', 'Swift'),
                mv('recover', 'Recover'),
                mv('psywave', 'Psywave'),
            ]),
        ]),
        gym('Lt. Surge', 3, 'Vermilion City', 'badgeelectric', 'lt-surge', [
            mon('voltorb', 'Voltorb', 25, ['electric'], [
                mv('sonic-boom', 'Sonic Boom'),
                mv('tackle', 'Tackle'),
                mv('thunder-shock', 'Thunder Shock'),
                mv('self-destruct', 'Self-Destruct'),
            ]),
            mon('magnemite', 'Magnemite', 25, ['electric', 'steel'], [
                mv('thunder-shock', 'Thunder Shock'),
                mv('supersonic', 'Supersonic'),
                mv('sonic-boom', 'Sonic Boom'),
                mv('thunder-wave', 'Thunder Wave'),
            ]),
            mon('raichu', 'Raichu', 26, ['electric'], [
                mv('thunderbolt', 'Thunderbolt'),
                mv('thunder-wave', 'Thunder Wave'),
                mv('slam', 'Slam'),
                mv('mega-kick', 'Mega Kick'),
            ]),
        ]),
        gym('Erika', 4, 'Celadon City', 'badgegrass', 'erika', [
            mon('tangela', 'Tangela', 33, ['grass'], [
                mv('vine-whip', 'Vine Whip'),
                mv('constrict', 'Constrict'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('mega-drain', 'Mega Drain'),
            ]),
            mon('weepinbell', 'Weepinbell', 33, ['grass', 'poison'], [
                mv('razor-leaf', 'Razor Leaf'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('acid', 'Acid'),
                mv('wrap', 'Wrap'),
            ]),
            mon('vileplume', 'Vileplume', 34, ['grass', 'poison'], [
                mv('petal-dance', 'Petal Dance'),
                mv('acid', 'Acid'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('moonblast', 'Moonblast'),
            ]),
        ]),
        gym('Koga', 5, 'Fuchsia City', 'badgepoison', 'koga', [
            mon('weezing', 'Weezing', 43, ['poison'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('smokescreen', 'Smokescreen'),
                mv('explosion', 'Explosion'),
                mv('toxic', 'Toxic'),
            ]),
            mon('muk', 'Muk', 43, ['poison'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('minimize', 'Minimize'),
                mv('acid-armor', 'Acid Armor'),
                mv('toxic', 'Toxic'),
            ]),
            mon('golbat', 'Golbat', 43, ['poison', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('bite', 'Bite'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('poison-fang', 'Poison Fang'),
            ]),
            mon('venomoth', 'Venomoth', 44, ['bug', 'poison'], [
                mv('psychic', 'Psychic'),
                mv('sleep-powder', 'Sleep Powder'),
                mv('bug-buzz', 'Bug Buzz'),
                mv('poison-fang', 'Poison Fang'),
            ]),
        ]),
        gym('Sabrina', 6, 'Saffron City', 'badgepsychic', 'sabrina', [
            mon('mr-mime', 'Mr. Mime', 43, ['psychic', 'fairy'], [
                mv('psychic', 'Psychic'),
                mv('light-screen', 'Light Screen'),
                mv('reflect', 'Reflect'),
                mv('baton-pass', 'Baton Pass'),
            ]),
            mon('slowbro', 'Slowbro', 43, ['water', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('surf', 'Surf'),
                mv('flamethrower', 'Flamethrower'),
                mv('slack-off', 'Slack Off'),
            ]),
            mon('jynx', 'Jynx', 43, ['ice', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('ice-beam', 'Ice Beam'),
                mv('lovely-kiss', 'Lovely Kiss'),
                mv('shadow-ball', 'Shadow Ball'),
            ]),
            mon('alakazam', 'Alakazam', 44, ['psychic'], [
                mv('psychic', 'Psychic'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('recover', 'Recover'),
                mv('calm-mind', 'Calm Mind'),
            ]),
        ]),
        gym('Blaine', 7, 'Cinnabar Island', 'badgefire', 'blaine', [
            mon('magmar', 'Magmar', 47, ['fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('fire-punch', 'Fire Punch'),
                mv('smokescreen', 'Smokescreen'),
                mv('confuse-ray', 'Confuse Ray'),
            ]),
            mon('rapidash', 'Rapidash', 47, ['fire'], [
                mv('fire-blast', 'Fire Blast'),
                mv('stomp', 'Stomp'),
                mv('fire-spin', 'Fire Spin'),
                mv('agility', 'Agility'),
            ]),
            mon('ninetales', 'Ninetales', 47, ['fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('extrasensory', 'Extrasensory'),
            ]),
            mon('arcanine', 'Arcanine', 48, ['fire'], [
                mv('flamethrower', 'Flamethrower'),
                mv('extreme-speed', 'Extreme Speed'),
                mv('crunch', 'Crunch'),
                mv('fire-fang', 'Fire Fang'),
            ]),
        ]),
        gym('Giovanni', 8, 'Viridian City', 'badgeground', 'giovanni', [
            mon('dugtrio', 'Dugtrio', 49, ['ground'], [
                mv('earthquake', 'Earthquake'),
                mv('slash', 'Slash'),
                mv('sand-attack', 'Sand Attack'),
                mv('sucker-punch', 'Sucker Punch'),
            ]),
            mon('nidoqueen', 'Nidoqueen', 49, ['poison', 'ground'], [
                mv('earthquake', 'Earthquake'),
                mv('poison-jab', 'Poison Jab'),
                mv('body-slam', 'Body Slam'),
                mv('crunch', 'Crunch'),
            ]),
            mon('nidoking', 'Nidoking', 49, ['poison', 'ground'], [
                mv('earthquake', 'Earthquake'),
                mv('megahorn', 'Megahorn'),
                mv('poison-jab', 'Poison Jab'),
                mv('thrash', 'Thrash'),
            ]),
            mon('rhydon', 'Rhydon', 50, ['ground', 'rock'], [
                mv('earthquake', 'Earthquake'),
                mv('rock-slide', 'Rock Slide'),
                mv('megahorn', 'Megahorn'),
                mv('stone-edge', 'Stone Edge'),
            ]),
        ]),
        e4('Lorelei', 1, 'loreleiice', 'lorelei', [
            mon('dewgong', 'Dewgong', 51, ['water', 'ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('waterfall', 'Waterfall'),
                mv('rest', 'Rest'),
            ]),
            mon('jynx', 'Jynx', 51, ['ice', 'psychic'], [
                mv('blizzard', 'Blizzard'),
                mv('psychic', 'Psychic'),
                mv('lovely-kiss', 'Lovely Kiss'),
                mv('focus-blast', 'Focus Blast'),
            ]),
            mon('cloyster', 'Cloyster', 51, ['water', 'ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('spike-cannon', 'Spike Cannon'),
                mv('hydro-pump', 'Hydro Pump'),
                mv('shell-smash', 'Shell Smash'),
            ]),
            mon('slowbro', 'Slowbro', 51, ['water', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('surf', 'Surf'),
                mv('flamethrower', 'Flamethrower'),
                mv('slack-off', 'Slack Off'),
            ]),
            mon('lapras', 'Lapras', 52, ['water', 'ice'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('blizzard', 'Blizzard'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('ice-beam', 'Ice Beam'),
            ]),
        ]),
        e4('Bruno', 2, 'brunofighting', 'bruno', [
            mon('onix', 'Onix', 52, ['rock', 'ground'], [
                mv('rock-slide', 'Rock Slide'),
                mv('earthquake', 'Earthquake'),
                mv('iron-tail', 'Iron Tail'),
                mv('crunch', 'Crunch'),
            ]),
            mon('hitmonlee', 'Hitmonlee', 52, ['fighting'], [
                mv('high-jump-kick', 'High Jump Kick'),
                mv('mega-kick', 'Mega Kick'),
                mv('brick-break', 'Brick Break'),
                mv('blaze-kick', 'Blaze Kick'),
            ]),
            mon('hitmonchan', 'Hitmonchan', 52, ['fighting'], [
                mv('thunder-punch', 'Thunder Punch'),
                mv('ice-punch', 'Ice Punch'),
                mv('fire-punch', 'Fire Punch'),
                mv('drain-punch', 'Drain Punch'),
            ]),
            mon('poliwrath', 'Poliwrath', 52, ['water', 'fighting'], [
                mv('surf', 'Surf'),
                mv('hypnosis', 'Hypnosis'),
                mv('ice-punch', 'Ice Punch'),
                mv('body-slam', 'Body Slam'),
            ]),
            mon('machamp', 'Machamp', 53, ['fighting'], [
                mv('dynamic-punch', 'Dynamic Punch'),
                mv('stone-edge', 'Stone Edge'),
                mv('earthquake', 'Earthquake'),
                mv('bulk-up', 'Bulk Up'),
            ]),
        ]),
        e4('Agatha', 3, 'agathaghost', 'agatha', [
            mon('arbok', 'Arbok', 53, ['poison'], [
                mv('poison-jab', 'Poison Jab'),
                mv('crunch', 'Crunch'),
                mv('glare', 'Glare'),
                mv('earthquake', 'Earthquake'),
            ]),
            mon('golbat', 'Golbat', 53, ['poison', 'flying'], [
                mv('air-slash', 'Air Slash'),
                mv('bite', 'Bite'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('poison-fang', 'Poison Fang'),
            ]),
            mon('haunter', 'Haunter', 53, ['ghost', 'poison'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('hypnosis', 'Hypnosis'),
                mv('dream-eater', 'Dream Eater'),
                mv('curse', 'Curse'),
            ]),
            mon('weezing', 'Weezing', 53, ['poison'], [
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('explosion', 'Explosion'),
                mv('toxic', 'Toxic'),
                mv('smokescreen', 'Smokescreen'),
            ]),
            mon('gengar', 'Gengar', 54, ['ghost', 'poison'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('focus-blast', 'Focus Blast'),
                mv('destiny-bond', 'Destiny Bond'),
            ]),
        ]),
        e4('Lance', 4, 'lancedragon', 'lance', [
            mon('seadra', 'Seadra', 54, ['water'], [
                mv('waterfall', 'Waterfall'),
                mv('ice-beam', 'Ice Beam'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('agility', 'Agility'),
            ]),
            mon('aerodactyl', 'Aerodactyl', 54, ['rock', 'flying'], [
                mv('rock-slide', 'Rock Slide'),
                mv('earthquake', 'Earthquake'),
                mv('fly', 'Fly'),
                mv('crunch', 'Crunch'),
            ]),
            mon('gyarados', 'Gyarados', 54, ['water', 'flying'], [
                mv('waterfall', 'Waterfall'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
            mon('charizard', 'Charizard', 54, ['fire', 'flying'], [
                mv('flamethrower', 'Flamethrower'),
                mv('air-slash', 'Air Slash'),
                mv('dragon-claw', 'Dragon Claw'),
                mv('fire-blast', 'Fire Blast'),
            ]),
            mon('dragonite', 'Dragonite', 55, ['dragon', 'flying'], [
                mv('outrage', 'Outrage'),
                mv('hyper-beam', 'Hyper Beam'),
                mv('fire-blast', 'Fire Blast'),
                mv('thunder', 'Thunder'),
            ]),
        ]),
        {
            'name': 'Trace',
            'type': 'champion',
            'order': 1,
            'location': '',
            'badge': '',
            'specialty': '',
            'sprite': SPRITE.format(slug='trace'),
            'team': trace_team(jolteon),
            'teamByStarter': {
                'pikachu': trace_team(jolteon),
                'eevee': trace_team(raichu),
            },
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
    e4n = sum(1 for t in built if t['type'] == 'elite4')
    print(f'OK: {gyms} gimnasios, {e4n} E4, 1 campeón en {GAME_SLUG}')


if __name__ == '__main__':
    main()
