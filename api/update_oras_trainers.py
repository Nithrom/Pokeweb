"""
Actualiza gimnasios, Alto Mando, campeón y revanchas — Rubí Omega / Zafiro Alfa.
Uso: python update_oras_trainers.py
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TRAINERS_PATH = ROOT / 'data' / 'trainers_db.json'
GAME_SLUG = 'omega-ruby-alpha-sapphire'
SPRITE = 'https://img.pokemondb.net/sprites/trainers/oras/{slug}.jpg'


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


def champion(name: str, order: int, specialty: str, sprite: str, team: list[dict]) -> dict:
    return {
        'name': name,
        'type': 'champion',
        'order': order,
        'location': '',
        'badge': '',
        'specialty': specialty,
        'sprite': SPRITE.format(slug=sprite),
        'team': team,
    }


def build_gyms() -> list[dict]:
    return [
        gym('Roxanne', 1, 'Rustboro City', 'badgerock', 'roxanne', [
            mon('geodude', 'Geodude', 12, ['rock', 'ground'], [
                mv('tackle', 'Tackle'),
                mv('defense-curl', 'Defense Curl'),
                mv('rock-throw', 'Rock Throw'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
            mon('nosepass', 'Nosepass', 14, ['rock'], [
                mv('tackle', 'Tackle'),
                mv('harden', 'Harden'),
                mv('rock-throw', 'Rock Throw'),
                mv('rock-tomb', 'Rock Tomb'),
            ]),
        ]),
        gym('Brawly', 2, 'Dewford Town', 'badgefighting', 'brawly', [
            mon('machop', 'Machop', 14, ['fighting'], [
                mv('bulk-up', 'Bulk Up'),
                mv('leer', 'Leer'),
                mv('karate-chop', 'Karate Chop'),
                mv('seismic-toss', 'Seismic Toss'),
            ]),
            mon('makuhita', 'Makuhita', 16, ['fighting'], [
                mv('arm-thrust', 'Arm Thrust'),
                mv('sand-attack', 'Sand Attack'),
                mv('fake-out', 'Fake Out'),
                mv('vital-throw', 'Vital Throw'),
            ]),
        ]),
        gym('Wattson', 3, 'Mauville City', 'badgeelectric', 'wattson', [
            mon('voltorb', 'Voltorb', 19, ['electric'], [
                mv('thunder-wave', 'Thunder Wave'),
                mv('tackle', 'Tackle'),
                mv('volt-switch', 'Volt Switch'),
                mv('sonic-boom', 'Sonic Boom'),
            ]),
            mon('magnemite', 'Magnemite', 19, ['electric', 'steel'], [
                mv('thunder-shock', 'Thunder Shock'),
                mv('supersonic', 'Supersonic'),
                mv('sonic-boom', 'Sonic Boom'),
                mv('volt-switch', 'Volt Switch'),
            ]),
            mon('magneton', 'Magneton', 21, ['electric', 'steel'], [
                mv('thunder-wave', 'Thunder Wave'),
                mv('magnet-bomb', 'Magnet Bomb'),
                mv('supersonic', 'Supersonic'),
                mv('volt-switch', 'Volt Switch'),
            ]),
        ]),
        gym('Flannery', 4, 'Lavaridge Town', 'badgefire', 'flannery', [
            mon('slugma', 'Slugma', 26, ['fire'], [
                mv('lava-plume', 'Lava Plume'),
                mv('smog', 'Smog'),
                mv('sunny-day', 'Sunny Day'),
                mv('amnesia', 'Amnesia'),
            ]),
            mon('slugma', 'Slugma', 26, ['fire'], [
                mv('lava-plume', 'Lava Plume'),
                mv('earth-power', 'Earth Power'),
                mv('sunny-day', 'Sunny Day'),
                mv('rock-slide', 'Rock Slide'),
            ]),
            mon('torkoal', 'Torkoal', 28, ['fire'], [
                mv('overheat', 'Overheat'),
                mv('body-slam', 'Body Slam'),
                mv('curse', 'Curse'),
                mv('sunny-day', 'Sunny Day'),
            ]),
        ]),
        gym('Norman', 5, 'Petalburg City', 'badgenormal', 'norman', [
            mon('slaking', 'Slaking', 28, ['normal'], [
                mv('feint-attack', 'Feint Attack'),
                mv('yawn', 'Yawn'),
                mv('slack-off', 'Slack Off'),
                mv('retaliate', 'Retaliate'),
            ]),
            mon('vigoroth', 'Vigoroth', 28, ['normal'], [
                mv('slash', 'Slash'),
                mv('encore', 'Encore'),
                mv('feint-attack', 'Feint Attack'),
                mv('fury-swipes', 'Fury Swipes'),
            ]),
            mon('slaking', 'Slaking', 30, ['normal'], [
                mv('retaliate', 'Retaliate'),
                mv('yawn', 'Yawn'),
                mv('encore', 'Encore'),
                mv('feint-attack', 'Feint Attack'),
            ]),
        ]),
        gym('Winona', 6, 'Fortree City', 'badgeflying', 'winona', [
            mon('swellow', 'Swellow', 33, ['normal', 'flying'], [
                mv('aerial-ace', 'Aerial Ace'),
                mv('double-team', 'Double Team'),
                mv('quick-attack', 'Quick Attack'),
                mv('endeavor', 'Endeavor'),
            ]),
            mon('pelipper', 'Pelipper', 33, ['water', 'flying'], [
                mv('water-pulse', 'Water Pulse'),
                mv('protect', 'Protect'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('roost', 'Roost'),
            ]),
            mon('skarmory', 'Skarmory', 33, ['steel', 'flying'], [
                mv('steel-wing', 'Steel Wing'),
                mv('air-cutter', 'Air Cutter'),
                mv('sand-attack', 'Sand Attack'),
                mv('aerial-ace', 'Aerial Ace'),
            ]),
            mon('altaria', 'Altaria', 35, ['dragon', 'flying'], [
                mv('dragon-breath', 'Dragon Breath'),
                mv('cotton-guard', 'Cotton Guard'),
                mv('earthquake', 'Earthquake'),
                mv('aerial-ace', 'Aerial Ace'),
            ]),
        ]),
        gym('Tate & Liza', 7, 'Mossdeep City', 'badgepsychic', 'liza-tate', [
            mon('lunatone', 'Lunatone', 45, ['rock', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('light-screen', 'Light Screen'),
                mv('hypnosis', 'Hypnosis'),
                mv('calm-mind', 'Calm Mind'),
            ]),
            mon('solrock', 'Solrock', 45, ['rock', 'psychic'], [
                mv('psychic', 'Psychic'),
                mv('rock-slide', 'Rock Slide'),
                mv('sunny-day', 'Sunny Day'),
                mv('solar-beam', 'Solar Beam'),
            ]),
        ]),
        gym('Wallace', 8, 'Sootopolis City', 'badgewater', 'wallace', [
            mon('luvdisc', 'Luvdisc', 44, ['water'], [
                mv('water-pulse', 'Water Pulse'),
                mv('attract', 'Attract'),
                mv('sweet-kiss', 'Sweet Kiss'),
                mv('draining-kiss', 'Draining Kiss'),
            ]),
            mon('whiscash', 'Whiscash', 44, ['water', 'ground'], [
                mv('waterfall', 'Waterfall'),
                mv('earthquake', 'Earthquake'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('mud-sport', 'Mud Sport'),
            ]),
            mon('sealeo', 'Sealeo', 44, ['ice', 'water'], [
                mv('aurora-beam', 'Aurora Beam'),
                mv('body-slam', 'Body Slam'),
                mv('encore', 'Encore'),
                mv('waterfall', 'Waterfall'),
            ]),
            mon('seaking', 'Seaking', 44, ['water'], [
                mv('water-pulse', 'Water Pulse'),
                mv('horn-drill', 'Horn Drill'),
                mv('rain-dance', 'Rain Dance'),
                mv('fury-attack', 'Fury Attack'),
            ]),
            mon('milotic', 'Milotic', 46, ['water'], [
                mv('hydro-pump', 'Hydro Pump'),
                mv('ice-beam', 'Ice Beam'),
                mv('recover', 'Recover'),
                mv('disarming-voice', 'Disarming Voice'),
            ]),
        ]),
    ]


def build_e4_champion() -> list[dict]:
    return [
        e4('Sidney', 1, 'sidneydark', 'sidney', [
            mon('mightyena', 'Mightyena', 50, ['dark'], [
                mv('crunch', 'Crunch'),
                mv('sucker-punch', 'Sucker Punch'),
                mv('take-down', 'Take Down'),
                mv('swagger', 'Swagger'),
            ]),
            mon('shiftry', 'Shiftry', 50, ['grass', 'dark'], [
                mv('leaf-blade', 'Leaf Blade'),
                mv('feint-attack', 'Feint Attack'),
                mv('extrasensory', 'Extrasensory'),
                mv('fake-out', 'Fake Out'),
            ]),
            mon('cacturne', 'Cacturne', 50, ['grass', 'dark'], [
                mv('needle-arm', 'Needle Arm'),
                mv('payback', 'Payback'),
                mv('leech-seed', 'Leech Seed'),
                mv('spiky-shield', 'Spiky Shield'),
            ]),
            mon('sharpedo', 'Sharpedo', 50, ['water', 'dark'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('crunch', 'Crunch'),
                mv('poison-fang', 'Poison Fang'),
                mv('slash', 'Slash'),
            ]),
            mon('absol', 'Absol', 52, ['dark'], [
                mv('night-slash', 'Night Slash'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('slash', 'Slash'),
            ]),
        ]),
        e4('Phoebe', 2, 'phoebeghost', 'phoebe', [
            mon('dusclops', 'Dusclops', 52, ['ghost'], [
                mv('shadow-punch', 'Shadow Punch'),
                mv('confuse-ray', 'Confuse Ray'),
                mv('curse', 'Curse'),
                mv('future-sight', 'Future Sight'),
            ]),
            mon('banette', 'Banette', 51, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('feint-attack', 'Feint Attack'),
                mv('spite', 'Spite'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
            mon('sableye', 'Sableye', 51, ['dark', 'ghost'], [
                mv('shadow-claw', 'Shadow Claw'),
                mv('foul-play', 'Foul Play'),
                mv('fake-out', 'Fake Out'),
                mv('power-gem', 'Power Gem'),
            ]),
            mon('banette', 'Banette', 51, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('psychic', 'Psychic'),
                mv('toxic', 'Toxic'),
                mv('grudge', 'Grudge'),
            ]),
            mon('dusknoir', 'Dusknoir', 53, ['ghost'], [
                mv('shadow-punch', 'Shadow Punch'),
                mv('ice-punch', 'Ice Punch'),
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
            ]),
        ]),
        e4('Glacia', 3, 'glaciaice', 'glacia', [
            mon('glalie', 'Glalie', 52, ['ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('crunch', 'Crunch'),
                mv('freeze-dry', 'Freeze-Dry'),
                mv('hail', 'Hail'),
            ]),
            mon('froslass', 'Froslass', 52, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('double-team', 'Double Team'),
            ]),
            mon('glalie', 'Glalie', 52, ['ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('crunch', 'Crunch'),
                mv('freeze-dry', 'Freeze-Dry'),
                mv('hail', 'Hail'),
            ]),
            mon('froslass', 'Froslass', 52, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('double-team', 'Double Team'),
            ]),
            mon('walrein', 'Walrein', 54, ['ice', 'water'], [
                mv('surf', 'Surf'),
                mv('blizzard', 'Blizzard'),
                mv('body-slam', 'Body Slam'),
                mv('sheer-cold', 'Sheer Cold'),
            ]),
        ]),
        e4('Drake', 4, 'drakedragon', 'drake', [
            mon('altaria', 'Altaria', 53, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('cotton-guard', 'Cotton Guard'),
                mv('moonblast', 'Moonblast'),
            ]),
            mon('flygon', 'Flygon', 53, ['ground', 'dragon'], [
                mv('dragon-rush', 'Dragon Rush'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-claw', 'Dragon Claw'),
                mv('flamethrower', 'Flamethrower'),
            ]),
            mon('salamence', 'Salamence', 55, ['dragon', 'flying'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('crunch', 'Crunch'),
                mv('dragon-dance', 'Dragon Dance'),
            ]),
            mon('kingdra', 'Kingdra', 53, ['water', 'dragon'], [
                mv('surf', 'Surf'),
                mv('ice-beam', 'Ice Beam'),
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('yawn', 'Yawn'),
            ]),
        ]),
        champion('Steven', 1, 'stevensteel', 'steven', [
            mon('skarmory', 'Skarmory', 57, ['steel', 'flying'], [
                mv('spikes', 'Spikes'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('steel-wing', 'Steel Wing'),
                mv('toxic', 'Toxic'),
            ]),
            mon('claydol', 'Claydol', 57, ['ground', 'psychic'], [
                mv('earth-power', 'Earth Power'),
                mv('psychic', 'Psychic'),
                mv('reflect', 'Reflect'),
                mv('light-screen', 'Light Screen'),
            ]),
            mon('aggron', 'Aggron', 57, ['steel', 'rock'], [
                mv('iron-tail', 'Iron Tail'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-claw', 'Dragon Claw'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('cradily', 'Cradily', 57, ['rock', 'grass'], [
                mv('giga-drain', 'Giga Drain'),
                mv('ancient-power', 'Ancient Power'),
                mv('sludge-bomb', 'Sludge Bomb'),
                mv('recover', 'Recover'),
            ]),
            mon('armaldo', 'Armaldo', 57, ['rock', 'bug'], [
                mv('x-scissor', 'X-Scissor'),
                mv('rock-blast', 'Rock Blast'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('slash', 'Slash'),
            ]),
            mon('metagross', 'Metagross', 59, ['steel', 'psychic'], [
                mv('meteor-mash', 'Meteor Mash'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('bullet-punch', 'Bullet Punch'),
                mv('giga-impact', 'Giga Impact'),
            ]),
        ]),
    ]


def build_rematch() -> list[dict]:
    return [
        e4('Sidney', 1, 'rematchdark', 'sidney', [
            mon('shiftry', 'Shiftry', 72, ['grass', 'dark'], [
                mv('leaf-blade', 'Leaf Blade'),
                mv('foul-play', 'Foul Play'),
                mv('fake-out', 'Fake Out'),
                mv('extrasensory', 'Extrasensory'),
            ]),
            mon('cacturne', 'Cacturne', 72, ['grass', 'dark'], [
                mv('needle-arm', 'Needle Arm'),
                mv('spikes', 'Spikes'),
                mv('payback', 'Payback'),
                mv('leech-seed', 'Leech Seed'),
            ]),
            mon('sharpedo', 'Sharpedo', 72, ['water', 'dark'], [
                mv('aqua-jet', 'Aqua Jet'),
                mv('crunch', 'Crunch'),
                mv('ice-fang', 'Ice Fang'),
                mv('earthquake', 'Earthquake'),
            ]),
            mon('mandibuzz', 'Mandibuzz', 72, ['dark', 'flying'], [
                mv('brave-bird', 'Brave Bird'),
                mv('foul-play', 'Foul Play'),
                mv('roost', 'Roost'),
                mv('toxic', 'Toxic'),
            ]),
            mon('absol', 'Absol', 74, ['dark'], [
                mv('night-slash', 'Night Slash'),
                mv('psycho-cut', 'Psycho Cut'),
                mv('play-rough', 'Play Rough'),
                mv('swords-dance', 'Swords Dance'),
            ]),
        ]),
        e4('Phoebe', 2, 'rematchghost', 'phoebe', [
            mon('dusclops', 'Dusclops', 72, ['ghost'], [
                mv('shadow-punch', 'Shadow Punch'),
                mv('will-o-wisp', 'Will-O-Wisp'),
                mv('pain-split', 'Pain Split'),
                mv('ice-punch', 'Ice Punch'),
            ]),
            mon('banette', 'Banette', 72, ['ghost'], [
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('ice-beam', 'Ice Beam'),
                mv('will-o-wisp', 'Will-O-Wisp'),
            ]),
            mon('sableye', 'Sableye', 72, ['dark', 'ghost'], [
                mv('foul-play', 'Foul Play'),
                mv('shadow-claw', 'Shadow Claw'),
                mv('recover', 'Recover'),
                mv('power-gem', 'Power Gem'),
            ]),
            mon('froslass', 'Froslass', 72, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('destiny-bond', 'Destiny Bond'),
            ]),
            mon('dusknoir', 'Dusknoir', 74, ['ghost'], [
                mv('shadow-punch', 'Shadow Punch'),
                mv('earthquake', 'Earthquake'),
                mv('fire-punch', 'Fire Punch'),
                mv('thunder-punch', 'Thunder Punch'),
            ]),
        ]),
        e4('Glacia', 3, 'rematchice', 'glacia', [
            mon('abomasnow', 'Abomasnow', 72, ['grass', 'ice'], [
                mv('blizzard', 'Blizzard'),
                mv('wood-hammer', 'Wood Hammer'),
                mv('earthquake', 'Earthquake'),
                mv('ice-shard', 'Ice Shard'),
            ]),
            mon('beartic', 'Beartic', 72, ['ice'], [
                mv('icicle-crash', 'Icicle Crash'),
                mv('superpower', 'Superpower'),
                mv('aqua-jet', 'Aqua Jet'),
                mv('slash', 'Slash'),
            ]),
            mon('froslass', 'Froslass', 72, ['ice', 'ghost'], [
                mv('ice-beam', 'Ice Beam'),
                mv('shadow-ball', 'Shadow Ball'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('confuse-ray', 'Confuse Ray'),
            ]),
            mon('vanilluxe', 'Vanilluxe', 72, ['ice'], [
                mv('ice-beam', 'Ice Beam'),
                mv('mirror-shot', 'Mirror Shot'),
                mv('freeze-dry', 'Freeze-Dry'),
                mv('signal-beam', 'Signal Beam'),
            ]),
            mon('walrein', 'Walrein', 72, ['ice', 'water'], [
                mv('surf', 'Surf'),
                mv('blizzard', 'Blizzard'),
                mv('body-slam', 'Body Slam'),
                mv('sheer-cold', 'Sheer Cold'),
            ]),
            mon('glalie-mega', 'Mega Glalie', 74, ['ice'], [
                mv('return', 'Return'),
                mv('ice-shard', 'Ice Shard'),
                mv('earthquake', 'Earthquake'),
                mv('explosion', 'Explosion'),
            ]),
        ]),
        e4('Drake', 4, 'rematchdragon', 'drake', [
            mon('altaria', 'Altaria', 73, ['dragon', 'flying'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('moonblast', 'Moonblast'),
                mv('cotton-guard', 'Cotton Guard'),
                mv('aerial-ace', 'Aerial Ace'),
            ]),
            mon('dragalge', 'Dragalge', 73, ['poison', 'dragon'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('sludge-wave', 'Sludge Wave'),
                mv('thunderbolt', 'Thunderbolt'),
                mv('hydro-pump', 'Hydro Pump'),
            ]),
            mon('kingdra', 'Kingdra', 73, ['water', 'dragon'], [
                mv('dragon-pulse', 'Dragon Pulse'),
                mv('surf', 'Surf'),
                mv('ice-beam', 'Ice Beam'),
                mv('yawn', 'Yawn'),
            ]),
            mon('flygon', 'Flygon', 73, ['ground', 'dragon'], [
                mv('earthquake', 'Earthquake'),
                mv('dragon-claw', 'Dragon Claw'),
                mv('flamethrower', 'Flamethrower'),
                mv('rock-slide', 'Rock Slide'),
            ]),
            mon('haxorus', 'Haxorus', 73, ['dragon'], [
                mv('dragon-claw', 'Dragon Claw'),
                mv('earthquake', 'Earthquake'),
                mv('x-scissor', 'X-Scissor'),
                mv('poison-jab', 'Poison Jab'),
            ]),
            mon('salamence-mega', 'Mega Salamence', 75, ['dragon', 'flying'], [
                mv('dragon-rush', 'Dragon Rush'),
                mv('double-edge', 'Double-Edge'),
                mv('earthquake', 'Earthquake'),
                mv('fire-blast', 'Fire Blast'),
            ]),
        ]),
        champion('Steven', 1, 'rematchsteel', 'steven', [
            mon('skarmory', 'Skarmory', 77, ['steel', 'flying'], [
                mv('toxic', 'Toxic'),
                mv('aerial-ace', 'Aerial Ace'),
                mv('spikes', 'Spikes'),
                mv('steel-wing', 'Steel Wing'),
            ]),
            mon('claydol', 'Claydol', 77, ['ground', 'psychic'], [
                mv('reflect', 'Reflect'),
                mv('light-screen', 'Light Screen'),
                mv('earth-power', 'Earth Power'),
                mv('extrasensory', 'Extrasensory'),
            ]),
            mon('carbink', 'Carbink', 77, ['rock', 'fairy'], [
                mv('moonblast', 'Moonblast'),
                mv('power-gem', 'Power Gem'),
                mv('psychic', 'Psychic'),
                mv('earth-power', 'Earth Power'),
            ]),
            mon('aerodactyl', 'Aerodactyl', 77, ['rock', 'flying'], [
                mv('rock-slide', 'Rock Slide'),
                mv('ice-fang', 'Ice Fang'),
                mv('thunder-fang', 'Thunder Fang'),
                mv('fire-fang', 'Fire Fang'),
            ]),
            mon('aggron', 'Aggron', 77, ['steel', 'rock'], [
                mv('iron-tail', 'Iron Tail'),
                mv('earthquake', 'Earthquake'),
                mv('dragon-claw', 'Dragon Claw'),
                mv('stone-edge', 'Stone Edge'),
            ]),
            mon('metagross-mega', 'Mega Metagross', 79, ['steel', 'psychic'], [
                mv('meteor-mash', 'Meteor Mash'),
                mv('zen-headbutt', 'Zen Headbutt'),
                mv('bullet-punch', 'Bullet Punch'),
                mv('hammer-arm', 'Hammer Arm'),
            ]),
        ]),
    ]


def main() -> None:
    data = json.loads(TRAINERS_PATH.read_text(encoding='utf-8'))
    trainers = data.setdefault('trainers', {})
    current = trainers.get(GAME_SLUG, [])
    built = build_gyms() + build_e4_champion() + build_rematch()
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
    rem = sum(1 for t in built if (t.get('specialty') or '').startswith('rematch'))
    print(f'OK: {gyms} gimnasios, {e4} E4, {champ} campeón, {rem} revanchas en {GAME_SLUG}')


if __name__ == '__main__':
    main()
