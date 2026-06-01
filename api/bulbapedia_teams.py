"""
bulbapedia_teams.py — Equipos y movimientos reales desde Bulbapedia (API MediaWiki).
"""
import re
import time
import requests
from bs4 import BeautifulSoup

UA = {'User-Agent': 'PokewebBot/1.0 (Pokeweb; educational trainer data)'}
API = 'https://bulbapedia.bulbagarden.net/w/api.php'

GAME_SECTION_TITLES = {
    'red-blue': 'Pokémon Red and Blue',
    'yellow': 'Pokémon Yellow',
    'gold-silver': 'Pokémon Gold, Silver, and Crystal',
    'crystal': 'Pokémon Gold, Silver, and Crystal',
    'ruby-sapphire': 'Pokémon Ruby and Sapphire',
    'emerald': 'Pokémon Ruby and Sapphire',
    'firered-leafgreen': 'Pokémon FireRed and LeafGreen',
    'diamond-pearl': 'Pokémon Diamond and Pearl',
    'platinum': 'Pokémon Platinum',
    'heartgold-soulsilver': 'Pokémon HeartGold and SoulSilver',
    'black-white': 'Pokémon Black and White',
    'black-white-2': 'Pokémon Black 2 and White 2',
    'x-y': 'Pokémon X and Y',
    'omega-ruby-alpha-sapphire': 'Pokémon Omega Ruby and Alpha Sapphire',
    'sun-moon': 'Pokémon Sun and Moon',
    'ultra-sun-ultra-moon': 'Pokémon Ultra Sun and Ultra Moon',
    'lets-go-pikachu-eevee': "Pokémon: Let's Go, Pikachu! and Let's Go, Eevee!",
    'sword-shield': 'Pokémon Sword and Shield',
    'brilliant-diamond-shining-pearl': 'Pokémon Brilliant Diamond and Shining Pearl',
    'scarlet-violet': 'Pokémon Scarlet and Violet',
}

TYPE_BATTLE_HINTS = {
    'gym': [r'gym', r'leader', r'gym leader', r'first battle', r'gym battle'],
    'elite4': [r'elite\s*four', r'elite four', r'pokémon league', r'pokemon league', r'indigo plateau'],
    'champion': [r'champion battle', r'champion', r'indigo plateau', r'title defense', r'become champion'],
    'kahuna': [r'kahuna', r'grand trial', r'island kahuna'],
    'captain': [r'captain', r'trial captain', r'trial', r'grand trial', r'post-game'],
    'other': [r'rival', r'boss', r'rematch'],
}

# Nombre en trainers_db → título de página en Bulbapedia
TRAINER_PAGE_ALIASES = {
    'Blue': 'Blue (game)',
    'Steven': 'Steven Stone',
    'Wallace': 'Wallace',
    'Kukui': 'Professor Kukui',
    'Tate & Liza': 'Tate and Liza',
    'Liza & Tate': 'Tate and Liza',
    'Mallow': 'Mallow',
    'Sophocles': 'Sophocles',
    'Kiawe': 'Kiawe',
    'Lana': 'Lana',
    'Ilima': 'Ilima',
    'Mina': 'Mina',
    'Hau': 'Hau',
    'Gladion': 'Gladion',
    'Nemona': 'Nemona',
    'Arven': 'Arven',
    'Penny': 'Penny',
    'Jacq': 'Jacq',
    'Trace': "Trace (Let's Go)",
    'Iono': 'Iono',
    'Cheren': 'Cheren',
    'Professor Kukui': 'Professor Kukui',
}

# (nombre entrenador, slug juego, tipo) → sección Bulbapedia (contiene este texto)
BATTLE_SECTION_OVERRIDE = {
    ('Kukui', 'sun-moon', 'champion'): 'Champion battle',
    ('Professor Kukui', 'sun-moon', 'champion'): 'Champion battle',
    ('Hau', 'ultra-sun-ultra-moon', 'champion'): 'Title Defense battle',
    ('Tate and Liza', 'ruby-sapphire', 'gym'): 'Gym battle',
    ('Tate and Liza', 'emerald', 'gym'): 'Gym battle',
    ('Tate and Liza', 'omega-ruby-alpha-sapphire', 'gym'): 'Gym battle',
    ('Liza & Tate', 'omega-ruby-alpha-sapphire', 'gym'): 'Gym battle',
    ('Tate & Liza', 'ruby-sapphire', 'gym'): 'Gym battle',
    ('Cynthia', 'platinum', 'champion'): 'Champion battle',
    ('Cynthia', 'diamond-pearl', 'champion'): 'Champion battle',
    ('Cynthia', 'brilliant-diamond-shining-pearl', 'champion'): 'Champion battle',
    ('Diantha', 'x-y', 'champion'): 'Champion battle',
    ('Cheren', 'black-white-2', 'gym'): 'Gym battle',
    ('Kiawe', 'sun-moon', 'captain'): 'Pokémon Sun',
    ('Kiawe', 'ultra-sun-ultra-moon', 'captain'): 'Pokémon Ultra Sun',
    ('Bea', 'sword-shield', 'gym'): 'Gym battle',
    ('Drayden', 'black-white', 'gym'): 'Gym battle',
    ('Erika', 'firered-leafgreen', 'gym'): 'Gym battle',
    ('Erika', 'heartgold-soulsilver', 'gym'): 'Gym battle',
    ('Misty', 'yellow', 'gym'): 'Pokémon Yellow',
}

_section_index_cache = {}
_page_sections_cache = {}
_section_html_cache = {}
_teams_cache = {}


def _api(params):
    r = requests.get(API, params=params, headers=UA, timeout=45)
    r.raise_for_status()
    return r.json()


def get_page_sections(page):
    if page not in _page_sections_cache:
        data = _api({'action': 'parse', 'page': page, 'format': 'json', 'prop': 'sections'})
        _page_sections_cache[page] = data.get('parse', {}).get('sections', [])
    return _page_sections_cache[page]


def resolve_bulbapedia_page(trainer_name):
    return TRAINER_PAGE_ALIASES.get(trainer_name, trainer_name)


def _normalize_section_line(line):
    return re.sub(r'\s+', ' ', line.replace('[edit]', '').strip())


def find_section_indices(page, title_substring):
    needle = title_substring.lower()
    needle_compact = needle.replace(' ', '')
    out = []
    for s in get_page_sections(page):
        line = _normalize_section_line(s.get('line', '')).lower()
        if needle in line or needle_compact in line.replace(' ', ''):
            out.append(s['index'])
    return out


def find_best_section_index(page, title_substring, game_slug=None):
    """Si hay varias secciones con el mismo título, elige la que tiene equipo PKMN."""
    key = (page, title_substring, game_slug or '')
    if key in _section_index_cache:
        return _section_index_cache[key]

    indices = find_section_indices(page, title_substring)
    if not indices:
        _section_index_cache[key] = None
        return None

    sections = get_page_sections(page)
    best_idx = None
    best_n = -1
    for idx in indices:
        if game_slug and not _last_game_section_before(sections, idx, game_slug):
            continue
        html = fetch_section_html(page, idx)
        if not _section_has_team(html):
            continue
        n = html.count('PKMNcontainer')
        if n > best_n:
            best_n = n
            best_idx = idx

    if best_idx is None and indices:
        best_idx = indices[-1]

    _section_index_cache[key] = best_idx
    return best_idx


def find_section_index(page, title_substring):
    return find_best_section_index(page, title_substring)


def _battle_section_override(trainer_name, game_slug, trainer_type):
    page_key = resolve_bulbapedia_page(trainer_name)
    for key in ((trainer_name, game_slug, trainer_type), (page_key, game_slug, trainer_type)):
        if key in BATTLE_SECTION_OVERRIDE:
            return BATTLE_SECTION_OVERRIDE[key]
    return None


def _section_has_team(html):
    return bool(html and 'PKMNcontainer' in html)


def _other_game_titles(game_slug):
    return [v.lower() for k, v in GAME_SECTION_TITLES.items() if k != game_slug]


def _last_game_section_before(sections, target_index, game_slug):
    """True si hay una cabecera del juego pedido antes de esta sección."""
    game_title = GAME_SECTION_TITLES.get(game_slug, '').lower()
    if not game_title:
        return True
    others = _other_game_titles(game_slug)
    seen = False
    for s in sections:
        if int(s['index']) >= int(target_index):
            break
        line = _normalize_section_line(s.get('line', '')).lower()
        if game_title in line:
            seen = True
        elif any(og in line for og in others if len(og) > 14):
            seen = False
    return seen


def find_section_for_trainer(page, game_slug, trainer_name, trainer_type):
    override = _battle_section_override(trainer_name, game_slug, trainer_type)
    if override:
        idx = find_best_section_index(page, override, game_slug)
        if idx:
            html = fetch_section_html(page, idx)
            if _section_has_team(html):
                return idx

    sections = get_page_sections(page)
    game_title = GAME_SECTION_TITLES.get(game_slug, '').lower()
    hints = TYPE_BATTLE_HINTS.get(trainer_type, TYPE_BATTLE_HINTS['other'])

    scored = []
    for s in sections:
        line = _normalize_section_line(s.get('line', ''))
        if not any(re.search(p, line, re.I) for p in hints):
            continue
        if not _last_game_section_before(sections, s['index'], game_slug):
            continue
        html = fetch_section_html(page, s['index'])
        if not _section_has_team(html):
            continue
        soup = BeautifulSoup(html, 'html.parser')
        n = len(soup.find_all('div', class_='PKMNcontainer'))
        sc = _score_label(line, trainer_type)
        scored.append((sc, n, s['index']))

    if scored:
        scored.sort(key=lambda x: (-x[0], -x[1]))
        return scored[0][2]

    for s in reversed(sections):
        if not game_title or game_title not in s.get('line', '').lower():
            continue
        html = fetch_section_html(page, s['index'])
        if _section_has_team(html):
            return s['index']

    if trainer_type == 'gym':
        for s in sections:
            if 'gym battle' not in s.get('line', '').lower():
                continue
            if not _last_game_section_before(sections, s['index'], game_slug):
                continue
            html = fetch_section_html(page, s['index'])
            if _section_has_team(html):
                return s['index']
    return None


def fetch_section_html(page, section_index):
    cache_key = (page, section_index)
    if cache_key in _section_html_cache:
        return _section_html_cache[cache_key]
    data = _api({
        'action': 'parse',
        'page': page,
        'section': section_index,
        'format': 'json',
        'prop': 'text',
    })
    html = data.get('parse', {}).get('text', {}).get('*', '')
    _section_html_cache[cache_key] = html
    time.sleep(0.15)
    return html


MOVE_ALIASES = {
    'ancientpower': 'ancient-power',
    'featherdance': 'feather-dance',
    'fleur-cannon': 'fleur-cannon',
    'highhorsepower': 'high-horsepower',
}

def move_name_to_api(text):
    n = text.lower().strip()
    n = re.sub(r"[^a-z0-9]+", '-', n)
    n = n.strip('-')
    return MOVE_ALIASES.get(n, n)


def parse_pokemon_container(container):
    name_box = container.find('div', class_='PKMNnamebox')
    if not name_box:
        return None
    name_link = name_box.find('a', title=re.compile(r'\(Pokémon\)'))
    if not name_link:
        return None
    display = name_link.get_text(strip=True)
    api_name = display.lower().replace(' ', '-')
    api_name = re.sub(r"[^a-z0-9\-]", '', api_name)
    disp_low = display.lower()
    if api_name == 'jellicent' or api_name.startswith('jellicent'):
        api_name = 'jellicent-female' if 'female' in disp_low else 'jellicent-male'

    level = None
    lv_el = container.find('div', class_='PKMNlevel')
    lv_text = (lv_el.get_text() if lv_el else '') or container.get_text(' ', strip=True)
    m = re.search(r'Lv\.?\s*(\d+)', lv_text)
    if m:
        level = int(m.group(1))

    moves = []
    for mb in container.find_all('div', class_='PKMNmovename'):
        ma = mb.find('a', href=re.compile(r'_\(move\)'))
        if ma:
            moves.append({
                'name': move_name_to_api(ma.get_text(strip=True)),
                'name_display': ma.get_text(strip=True),
            })

    types = []
    for cls in ('PKMNtype1', 'PKMNtype2'):
        tbox = container.find('div', class_=cls)
        if tbox:
            ta = tbox.find('a', href=re.compile(r'\(type\)'))
            if ta:
                types.append(ta.get_text(strip=True).lower())

    return {
        'name': api_name,
        'name_display': display,
        'level': level,
        'types': types,
        'moves': moves,
    }


def split_teams_in_section(soup):
    teams = []
    current_label = ''
    current_mons = []

    for el in soup.find_all(True):
        if el.name in ('h3', 'h4', 'h5', 'th', 'caption'):
            t = re.sub(r'\[edit\]', '', el.get_text(strip=True))
            if t and len(t) < 80:
                if current_mons:
                    teams.append((current_label, current_mons))
                    current_mons = []
                current_label = t
        if el.name == 'div' and 'PKMNcontainer' in el.get('class', []):
            mon = parse_pokemon_container(el)
            if mon:
                current_mons.append(mon)

    if current_mons:
        teams.append((current_label, current_mons))
    return teams


def _score_label(label, trainer_type):
    if not label:
        return 0
    low = re.sub(r'<[^>]+>', '', label).lower()
    score = 0
    for pat in TYPE_BATTLE_HINTS.get(trainer_type, []):
        if re.search(pat, low, re.I):
            score += 10
    if re.search(r'tournament|battle tree|world leaders|mix master|league club', low, re.I):
        score -= 25
    if re.search(r'rematch', low, re.I):
        score -= 5
    if re.search(r'gym battle|champion battle|first battle', low, re.I):
        score += 15
    return score


def pick_team_for_trainer(teams, trainer_type):
    if not teams:
        return None
    if len(teams) == 1:
        return teams[0][1]

    scored = [(_score_label(lbl, trainer_type), lbl, mons) for lbl, mons in teams]
    scored.sort(key=lambda x: (-x[0], -len(x[2])))
    if scored[0][0] > 0:
        return scored[0][2]

    teams.sort(key=lambda t: -len(t[1]))
    return teams[0][1]


# Mínimo de niveles entre apariciones del mismo Pokémon para tratarlo como otro modo (BW2 Challenge)
DIFFICULTY_LEVEL_GAP = 3


def split_difficulty_blocks(mons, level_gap=DIFFICULTY_LEVEL_GAP):
    """Normal/Fácil vs Challenge: segunda aparición con nivel claramente mayor."""
    if not mons:
        return []
    first_level = {}
    for i, m in enumerate(mons):
        n = m['name']
        lv = m.get('level') or 0
        if n in first_level and lv > first_level[n] + level_gap:
            return [mons[:i], mons[i:]]
        if n not in first_level:
            first_level[n] = lv
    return [mons]


def _block_species(block):
    return [m['name'] for m in block]


def _is_rematch_block_pattern(blocks):
    if len(blocks) < 2:
        return False
    b0, b1 = blocks[0], blocks[1]
    if len(b0) < 3 or len(b1) < 3 or len(b0) != len(b1):
        return False
    n0, n1 = set(_block_species(b0)), set(_block_species(b1))
    if n0 != n1:
        return False
    avg0 = sum(m.get('level') or 0 for m in b0) / len(b0)
    avg1 = sum(m.get('level') or 0 for m in b1) / len(b1)
    return avg1 >= avg0 + 6


def has_difficulty_variants(mons, game_slug=''):
    """Solo Challenge Mode real (BW2), alineado con trainers.js."""
    if game_slug != 'black-white-2' or not mons:
        return False
    blocks = split_difficulty_blocks(mons)
    if len(blocks) < 2 or len(blocks[0]) < 2 or len(blocks[1]) < 2:
        return False
    if _is_rematch_block_pattern(blocks):
        return False
    b0 = blocks[0]
    if len(_block_species(b0)) != len(b0):
        return False
    n0, n1 = set(_block_species(b0)), set(_block_species(blocks[1]))
    if n0 == n1:
        return False
    return len(blocks[1]) > len(b0) or bool(n0 & n1)


def _teams_from_section(page, section_index):
    if section_index is None:
        return []
    try:
        html = fetch_section_html(page, section_index)
    except Exception:
        return []
    if not _section_has_team(html):
        return []
    soup = BeautifulSoup(html, 'html.parser')
    return split_teams_in_section(soup)


def gather_all_page_teams(trainer_name, game_slug, trainer_type='gym'):
    """
    Subsecciones de batalla del juego (gym, rematch, champion…).
    Evita quedarse solo con la primera sección vacía del juego.
    """
    cache_key = ('all', trainer_name, game_slug, trainer_type)
    if cache_key in _teams_cache:
        return _teams_cache[cache_key]

    page = resolve_bulbapedia_page(trainer_name)
    sections = get_page_sections(page)
    if not sections:
        _teams_cache[cache_key] = None
        return None

    hints = list(TYPE_BATTLE_HINTS.get(trainer_type, TYPE_BATTLE_HINTS['other']))
    hints.extend([r'rematch', r'first battle'])

    all_teams = []
    seen = set()

    def add_teams(teams, section_idx):
        for lbl, mons in teams or []:
            if not mons:
                continue
            key = (_label_clean(lbl), tuple(m['name'] for m in mons))
            if key in seen:
                continue
            seen.add(key)
            all_teams.append((lbl, mons))

    main_idx = find_section_for_trainer(page, game_slug, trainer_name, trainer_type)
    add_teams(_teams_from_section(page, main_idx), main_idx)

    for s in sections:
        line = _normalize_section_line(s.get('line', ''))
        if not any(re.search(p, line, re.I) for p in hints):
            continue
        if not _last_game_section_before(sections, s['index'], game_slug):
            continue
        ll = _label_clean(line)
        if re.search(r'tournament|battle tree|world leaders|mix master|league club', ll):
            continue
        if _score_label(line, trainer_type) < 0 and 'rematch' not in ll:
            continue
        idx = s['index']
        if idx == main_idx:
            continue
        add_teams(_teams_from_section(page, idx), idx)

    _teams_cache[cache_key] = all_teams if all_teams else None
    return _teams_cache[cache_key]


def get_teams_for_game_section(trainer_name, game_slug, trainer_type='gym'):
    cache_key = (trainer_name, game_slug, trainer_type)
    if cache_key in _teams_cache:
        return _teams_cache[cache_key]

    teams = gather_all_page_teams(trainer_name, game_slug, trainer_type)
    _teams_cache[cache_key] = teams
    return teams


def fetch_trainer_team(trainer_name, game_slug, trainer_type):
    teams = get_teams_for_game_section(trainer_name, game_slug, trainer_type)
    if not teams:
        return None
    team = pick_team_for_trainer(teams, trainer_type)
    if not team:
        return None
    if has_difficulty_variants(team, game_slug):
        return team
    return team[:6]


def _normalize_team_mons(mons, normalize_name):
    if normalize_name:
        for mon in mons:
            mon['name'] = normalize_name(mon['name'], mon.get('name_display', ''))
    return mons


def _copy_moves_into_team(existing, source):
    """Copia movimientos de source a existing emparejando nombre + nivel."""
    if not existing or not source:
        return 0
    used = set()
    n = 0
    for ex in existing:
        best_i = None
        best_d = 999
        for j, src in enumerate(source):
            if j in used:
                continue
            if ex.get('name') != src.get('name'):
                continue
            d = abs((ex.get('level') or 0) - (src.get('level') or 0))
            if d < best_d:
                best_d = d
                best_i = j
        if best_i is None:
            continue
        used.add(best_i)
        src = source[best_i]
        if src.get('moves'):
            ex['moves'] = src['moves']
            if src.get('types'):
                ex['types'] = src['types']
            n += 1
    return n


def _label_clean(label):
    return re.sub(r'<[^>]+>', '', label or '').lower()


def block_avg(mons):
    if not mons:
        return 0
    return sum(m.get('level') or 0 for m in mons) / len(mons)


def collapse_duplicated_roster(team):
    """
    Dos bloques iguales pegados por error de scrape/enrich (p. ej. Drayden BW).
    No colapsar revanchas reales (Cynthia: mismas especies pero niveles distintos).
    """
    if len(team) < 4 or len(team) % 2:
        return team
    half = len(team) // 2
    first, second = team[:half], team[half:]
    if [p['name'] for p in first] != [p['name'] for p in second]:
        return team
    if _is_rematch_block_pattern([first, second]):
        return team
    return first


def enrich_trainer_moves(t, slug, normalize_name=None):
    """Rellena movimientos reales sin cambiar la composición del equipo en JSON."""
    typ = t.get('type', 'gym')
    page_teams = gather_all_page_teams(t['name'], slug, typ)
    if not page_teams:
        return False

    existing = t.get('team') or []
    if not existing:
        team = fetch_trainer_team(t['name'], slug, typ)
        if not team:
            return False
        _normalize_team_mons(team, normalize_name)
        t['team'] = collapse_duplicated_roster(team)
        return True

    blocks = split_difficulty_blocks(existing)
    has_rem = _is_rematch_block_pattern(blocks)
    has_diff = has_difficulty_variants(existing, slug)
    changed = 0

    for label, mons in page_teams:
        if not mons:
            continue
        _normalize_team_mons(mons, normalize_name)
        ll = _label_clean(label)
        if re.search(r'tournament|battle tree|world leaders|mix master', ll):
            continue

        if has_rem and len(blocks) >= 2:
            if 'rematch' in ll or ('after' in ll and 'stark' in ll):
                changed += _copy_moves_into_team(blocks[1], mons)
            elif 'before' in ll and 'stark' in ll:
                changed += _copy_moves_into_team(blocks[0], mons)
            elif re.search(
                r'gym battle|champion battle|first battle|trial|captain|pokémon sun|pokémon moon',
                ll,
            ):
                changed += _copy_moves_into_team(blocks[0], mons)
            elif block_avg(mons) <= block_avg(blocks[0]) + 2:
                changed += _copy_moves_into_team(blocks[0], mons)
            elif block_avg(mons) >= block_avg(blocks[1]) - 2:
                changed += _copy_moves_into_team(blocks[1], mons)
        elif has_diff and len(blocks) >= 2:
            avg = sum(m.get('level') or 0 for m in mons) / len(mons)
            avg0 = sum(m.get('level') or 0 for m in blocks[0]) / len(blocks[0])
            target = blocks[0] if avg <= avg0 + 4 else blocks[1]
            changed += _copy_moves_into_team(target, mons)
        else:
            changed += _copy_moves_into_team(existing, mons)

    if has_rem and len(blocks) >= 2:
        t['team'] = blocks[0] + blocks[1]
    elif changed:
        t['team'] = existing

    collapsed = collapse_duplicated_roster(t.get('team') or [])
    if len(collapsed) != len(t.get('team') or []):
        t['team'] = collapsed
        changed += 1
    else:
        t['team'] = collapsed

    return changed > 0


def _trainer_needs_moves(trainer):
    team = trainer.get('team') or []
    if not team:
        return True
    return any(not (p.get('moves') or []) for p in team)


def enrich_trainers_db(trainers_db, normalize_name=None, on_progress=None, only_missing_moves=False):
    """Equipos y movimientos desde Bulbapedia."""
    items = [(slug, t) for slug, trainers in trainers_db.items() for t in trainers]
    if only_missing_moves:
        items = [(slug, t) for slug, t in items if _trainer_needs_moves(t)]
    total = len(items)
    updated = 0
    skipped = 0

    for i, (slug, t) in enumerate(items, 1):
        if on_progress:
            on_progress(i, total, t['name'], slug)
        if enrich_trainer_moves(t, slug, normalize_name):
            updated += 1
        else:
            skipped += 1

    return updated, skipped


def clear_caches():
    _section_index_cache.clear()
    _page_sections_cache.clear()
    _section_html_cache.clear()
    _teams_cache.clear()


def print_enrich_progress(current, total, name, slug):
    pct = int(100 * current / total) if total else 0
    line = f"  Bulbapedia [{current}/{total}] ({pct}%) {name} — {slug}"
    print(line.ljust(72), end='\r', flush=True)
