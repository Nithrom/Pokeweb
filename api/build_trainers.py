#!/usr/bin/env python3
"""
build_trainers.py — Genera data/trainers_db.json scrapeando pokemondb.net
Uso: python build_trainers.py
Requiere: pip install beautifulsoup4 requests
Salida: data/trainers_db.json
"""
import json, time, os, re, sys
try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    import subprocess
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'beautifulsoup4', 'requests'])
    import requests
    from bs4 import BeautifulSoup

SESSION = requests.Session()
SESSION.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml',
    'Accept-Language': 'en-US,en;q=0.9',
})

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_DIR  = os.path.join(ROOT_DIR, 'data')
OUT_FILE = os.path.join(OUT_DIR, 'trainers_db.json')
os.makedirs(OUT_DIR, exist_ok=True)

# Orden en JSON y en trainers.js (Alola: kahuna → elite4 → champion → captain)
TYPE_SORT_ORDER = {'gym': 0, 'kahuna': 0, 'elite4': 1, 'champion': 2, 'captain': 3, 'other': 4}

def sort_trainers(trainers):
    return sorted(
        trainers,
        key=lambda t: (TYPE_SORT_ORDER.get(t.get('type'), 4), t.get('order') or 0),
    )

GAMES = [
    ('red-blue',                        'Rojo / Azul',                          1, 'Kanto'),
    ('yellow',                           'Amarillo',                             1, 'Kanto'),
    ('gold-silver',                      'Oro / Plata',                          2, 'Johto'),
    ('crystal',                          'Cristal',                              2, 'Johto'),
    ('ruby-sapphire',                    'Rubí / Zafiro',                        3, 'Hoenn'),
    ('emerald',                          'Esmeralda',                            3, 'Hoenn'),
    ('firered-leafgreen',                'Rojo Fuego / Verde Hoja',              3, 'Kanto'),
    ('diamond-pearl',                    'Diamante / Perla',                     4, 'Sinnoh'),
    ('platinum',                         'Platino',                              4, 'Sinnoh'),
    ('heartgold-soulsilver',             'HeartGold / SoulSilver',               4, 'Johto'),
    ('black-white',                      'Negro / Blanco',                       5, 'Teselia'),
    ('black-white-2',                    'Negro 2 / Blanco 2',                   5, 'Teselia'),
    ('x-y',                              'X / Y',                                6, 'Kalos'),
    ('omega-ruby-alpha-sapphire',        'Rubí Omega / Zafiro Alfa',             6, 'Hoenn'),
    ('sun-moon',                         'Sol / Luna',                           7, 'Alola'),
    ('ultra-sun-ultra-moon',             'Ultra Sol / Ultra Luna',               7, 'Alola'),
    ('sword-shield',                     'Espada / Escudo',                      8, 'Galar'),
    ('lets-go-pikachu-eevee',            "Let's Go Pikachu / Eevee",             7, 'Kanto'),
    ('brilliant-diamond-shining-pearl',  'Diamante Brillante / Perla Reluciente',8, 'Sinnoh'),
    ('scarlet-violet',                   'Escarlata / Púrpura',                  9, 'Paldea'),
]

def fetch_page(url, retries=4):
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=20)
            if r.status_code == 200:
                return r.text
            if r.status_code == 404:
                return None
            print(f"  HTTP {r.status_code}")
        except Exception as e:
            print(f"  Error ({e}), reintento {i+1}/{retries}...")
            time.sleep(3*(i+1))
    return None

def normalize_trainer_poke_name(api_name, display_name=''):
    """Alinea nombres scrapeados con las claves de pokemon_db (formas, etc.)."""
    disp = (display_name or '').lower()
    if api_name == 'lycanroc':
        if 'midnight' in disp:
            return 'lycanroc-midnight'
        if 'dusk' in disp:
            return 'lycanroc-dusk'
        if 'midday' in disp:
            return 'lycanroc-midday'
        return 'lycanroc-midday'
    if 'alolan' in disp and not api_name.endswith('-alola'):
        alt = f'{api_name}-alola'
        return alt
    if 'galarian' in disp and not api_name.endswith('-galar'):
        return f'{api_name}-galar'
    if api_name == 'jellicent' or api_name.startswith('jellicent'):
        return 'jellicent-female' if 'female' in disp else 'jellicent-male'
    return api_name

def to_api_name(name):
    """'Lt. Surge' → 'lt-surge', 'Nidoran♀' → 'nidoran-f'"""
    n = name.lower().strip()
    n = n.replace('♀', '-f').replace('♂', '-m')
    n = re.sub(r"['.:]", '', n)
    n = re.sub(r'\s+', '-', n)
    n = re.sub(r'-+', '-', n)
    return n.strip('-')

def get_trainer_type_from_id(id_str, slug=''):
    """Determina tipo y orden desde el id del h2: gym-1, kahuna-2, elite4-3, champion-5, captain-1"""
    if not id_str:
        return None, 0
    m = re.match(r'(gym|kahuna|elite4|champion|captain|trial)[-_]?(\d*)', id_str, re.I)
    if not m:
        return None, 0
    kind = m.group(1).lower()
    order = int(m.group(2)) if m.group(2) else 0
    ttype_map = {
        'gym': 'gym',
        'kahuna': 'kahuna',
        'elite4': 'elite4',
        'champion': 'champion',
        'captain': 'captain',
        'trial': 'gym',
    }
    ttype = ttype_map.get(kind, 'other')
    # Campeón de liga (p. ej. Kukui/Hau): un solo bloque champion-N
    if ttype == 'champion':
        order = 1
    return ttype, order

def parse_page(html, slug):
    soup = BeautifulSoup(html, 'html.parser')

    trainers = []
    gym_order = 0
    elite_order = 0

    all_h2 = soup.find_all('h2')

    for h2 in all_h2:
        txt = h2.get_text(strip=True)
        h2_id = h2.get('id', '')

        # Intentar clasificar por id primero (formato kahuna-1, elite4-1, etc.)
        ttype, order = get_trainer_type_from_id(h2_id, slug)

        # Si no hay id útil, clasificar por texto
        if not ttype:
            if re.search(r'gym\s*#?\d+', txt, re.I) or re.search(r'gym\s+leader', txt, re.I):
                gym_order += 1
                ttype = 'gym'
                order = gym_order
            elif re.search(r'elite\s*(four|4)', txt, re.I):
                elite_order += 1
                ttype = 'elite4'
                order = elite_order
            elif re.search(r'champion', txt, re.I):
                ttype = 'champion'
                order = 0
            elif re.search(r'island\s*kahuna|kahuna\s*#', txt, re.I):
                gym_order += 1
                ttype = 'kahuna'
                order = gym_order
            elif re.search(r'trial\s*captain|captain\s*#', txt, re.I):
                gym_order += 1
                ttype = 'captain'
                order = gym_order
            elif re.search(r'titan|star\s*boss|team\s*star', txt, re.I):
                ttype = 'other'
                order = 0
            else:
                continue

        # Ubicación
        location = ''
        loc = re.search(r',\s*(.+)$', txt)
        if loc:
            location = loc.group(1).strip()

        # Recoger nodos hasta el próximo h2
        nodes = []
        node = h2.next_sibling
        while node:
            if getattr(node, 'name', None) == 'h2':
                break
            nodes.append(node)
            node = node.next_sibling
        block = BeautifulSoup(''.join(str(n) for n in nodes), 'html.parser')

        # Trainer name + sprite
        trainer_name = ''
        sprite_url = ''
        t_img = block.find('img', src=re.compile(r'/sprites/trainers/'))
        if t_img:
            sprite_url = t_img.get('src', '')
            trainer_name = t_img.get('alt', '').strip()

        # Fallback nombre: primer párrafo corto que no sea badge/tipo
        if not trainer_name:
            for tag in block.find_all(['p', 'strong', 'b']):
                t = tag.get_text(strip=True)
                if t and 3 < len(t) < 25 and not re.search(r'badge|type pokémon|level', t, re.I):
                    trainer_name = t
                    break

        # Badge y especialidad
        badge = ''
        specialty = ''
        for p in block.find_all(['p', 'div', 'li']):
            t = p.get_text(strip=True)
            if re.search(r'badge', t, re.I) and len(t) < 40:
                badge = t
            m = re.search(r'(\w+)\s+type\s+pok', t, re.I)
            if m:
                specialty = m.group(1).lower()

        # Equipo pokémon
        # Cada pokémon: <a href="/pokedex/NAME"><img ...></a>  Level N  Type·Type
        team = []
        # Buscar por links a /pokedex/
        poke_links = block.find_all('a', href=re.compile(r'/pokedex/[a-z]'))
        for link in poke_links:
            # pokemondb duplica cada Pokémon (enlace con img + enlace de texto)
            img = link.find('img')
            if not img:
                continue
            href = link.get('href', '')
            m = re.match(r'/pokedex/([a-z0-9\-]+)', href)
            if not m:
                continue
            api_name = m.group(1)

            display = img.get('alt', '') or link.get_text(strip=True)
            if not display:
                display = api_name.replace('-',' ').title()

            # Nivel: buscar en el padre y sus hijos
            level = None
            parent = link.parent
            for _ in range(6):
                if parent is None: break
                lvl = re.search(r'[Ll]evel\s*(\d+)', parent.get_text())
                if lvl:
                    level = int(lvl.group(1))
                    break
                parent = parent.parent

            # Tipos desde links /type/
            types = []
            p2 = link.parent
            for _ in range(6):
                if p2 is None: break
                tlinks = p2.find_all('a', href=re.compile(r'/type/'))
                if tlinks:
                    types = [tl.get_text(strip=True).lower() for tl in tlinks]
                    break
                p2 = p2.parent

            api_name = normalize_trainer_poke_name(api_name, display)
            # Nota: varios rivales incluyen las 3 finales de iniciales en el scrape;
            # trainers.js filtra por "Inicial" del jugador (máx. 6 Pokémon).
            team.append({
                'name': api_name,
                'name_display': display,
                'level': level,
                'types': types,
                'moves': []
            })

        # Solo añadir si tiene equipo o al menos nombre
        if trainer_name or team:
            trainers.append({
                'name': trainer_name,
                'type': ttype,   # gym / elite4 / champion / other
                'order': order,
                'location': location,
                'badge': badge,
                'specialty': specialty,
                'sprite': sprite_url,
                'team': team
            })

    return trainers


def main():
    use_bulbapedia = '--bulbapedia' in sys.argv or '-b' in sys.argv
    print("═"*60)
    print("  PokéWeb Trainers Builder")
    print("  Scraping pokemondb.net — gym leaders & elite four")
    if use_bulbapedia:
        print("  + Enriquecimiento Bulbapedia (movimientos reales)")
    print("═"*60)

    trainers_db = {}
    games_meta  = []

    alt_urls = {
        'sun-moon':               'kahunas-elitefour',
        'ultra-sun-ultra-moon':   'kahunas-elitefour',
        'sword-shield':           'gymleaders',
        'lets-go-pikachu-eevee':  'gymleaders-elitefour',
    }

    for slug, name, gen, region in GAMES:
        page = alt_urls.get(slug, 'gymleaders-elitefour')
        url = f"https://pokemondb.net/{slug}/{page}"
        print(f"\n[Gen {gen}] {name}")
        print(f"  {url}")

        html = fetch_page(url)
        if not html:
            print(f"  SKIP — página no disponible")
            time.sleep(1)
            continue

        trainers = sort_trainers(parse_page(html, slug))
        n_with_team = sum(1 for t in trainers if t['team'])
        print(f"  ✓ {len(trainers)} entrenadores, {n_with_team} con equipo")

        # Debug: mostrar primeros entrenadores
        for t in trainers[:3]:
            print(f"    - {t['name']} ({t['type']}) → {len(t['team'])} pokémon")

        trainers_db[slug] = trainers
        games_meta.append({
            'slug':          slug,
            'name':          name,
            'gen':           gen,
            'region':        region,
            'trainer_count': len(trainers)
        })

        time.sleep(1.5)

    if use_bulbapedia:
        print("\n" + "─"*60)
        print("  Enriqueciendo con Bulbapedia (API)...")
        try:
            from bulbapedia_teams import enrich_trainers_db, print_enrich_progress
            n_up, n_skip = enrich_trainers_db(
                trainers_db,
                normalize_trainer_poke_name,
                on_progress=print_enrich_progress,
            )
            print()
            print(f"  ✓ {n_up} equipos actualizados · {n_skip} sin datos en Bulbapedia")
        except Exception as e:
            print(f"  ⚠ Bulbapedia omitido: {e}")

    total_t = sum(len(v) for v in trainers_db.values())
    sources = 'pokemondb.net' + (', bulbapedia.bulbagarden.net' if use_bulbapedia else '')
    output = {
        'meta': {
            'source':          sources,
            'total_games':     len(trainers_db),
            'total_trainers':  total_t,
        },
        'games':    games_meta,
        'trainers': trainers_db,
    }

    tmp = OUT_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, separators=(',',':'), indent=2)
    os.replace(tmp, OUT_FILE)

    size_kb = os.path.getsize(OUT_FILE) / 1024
    print(f"\n✅ {OUT_FILE} ({size_kb:.0f} KB)")
    print(f"   {len(trainers_db)} juegos | {total_t} entrenadores")
    if use_bulbapedia:
        print(f"\n✓ Movimientos reales desde Bulbapedia (sin inventar por nivel).")
        print(f"   Solo movimientos: python enrich_moves.py")
        print(f"   Solo faltantes:   python enrich_moves.py --solo-faltantes")
    else:
        print(f"\n⚠  Sin --bulbapedia: el JSON no tendrá movimientos de rivales.")
        print(f"   Usa: python build_trainers.py --bulbapedia")
        print(f"   o:  python enrich_moves.py")

if __name__ == '__main__':
    main()
