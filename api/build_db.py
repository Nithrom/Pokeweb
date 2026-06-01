"""
build_db.py — Genera data/pokemon_db.json
Uso: python build_db.py
"""
import json, time, os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

SESSION = requests.Session()
SESSION.headers.update({'User-Agent': 'PokeCounter/1.0'})
BASE = 'https://pokeapi.co/api/v2'
OUT_DIR  = os.path.join(os.path.dirname(__file__), 'data')
OUT_FILE = os.path.join(OUT_DIR, 'pokemon_db.json')
os.makedirs(OUT_DIR, exist_ok=True)

POKE_WORKERS = 6
MOVE_WORKERS = 12

def fetch(url, retries=5):
    for i in range(retries):
        try:
            r = SESSION.get(url, timeout=20)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if i == retries-1:
                raise
            time.sleep(2*(i+1))

# ── Evo map ───────────────────────────────────────────────────────────────────
def build_evo_map():
    print("📥 Cargando cadenas evolutivas...")
    idx = fetch(f"{BASE}/evolution-chain?limit=1000")
    total = idx["count"]
    all_urls = [c["url"] for c in idx["results"]]
    if total > 1000:
        idx2 = fetch(f"{BASE}/evolution-chain?limit={total}&offset=0")
        all_urls = [c["url"] for c in idx2["results"]]

    evo_map = {}
    def walk(node, parent=None):
        name = node["species"]["name"]
        if parent:
            evo_map[name] = parent
        for nxt in node.get("evolves_to", []):
            walk(nxt, name)

    def fetch_chain(url):
        try:
            d = fetch(url)
            walk(d["chain"])
        except Exception:
            pass

    done = 0
    with ThreadPoolExecutor(max_workers=10) as ex:
        futures = {ex.submit(fetch_chain, url): url for url in all_urls}
        for f in as_completed(futures):
            done += 1
            if done % 100 == 0:
                print(f"  Cadenas: {done}/{len(all_urls)}")

    print(f"  ✓ Evo map: {len(evo_map)} entradas")
    return evo_map

# ── Move detail ───────────────────────────────────────────────────────────────
def get_move_detail(move_name, url):
    try:
        d = fetch(url)
        name_es_list = [n["name"] for n in d.get("names",[]) if n["language"]["name"]=="es"]
        return move_name, {
            'name_es':  name_es_list[0] if name_es_list else move_name,
            'type':     d['type']['name'],
            'category': d['damage_class']['name'] if d.get('damage_class') else 'status',
            'power':    d.get('power'),
            'pp':       d.get('pp'),
            'accuracy': d.get('accuracy'),
            'priority': d.get('priority', 0),
        }
    except Exception:
        return move_name, {'name_es': move_name, 'type':'normal','category':'status',
                           'power':None,'pp':None,'accuracy':None,'priority':0}

# ── Pokémon ───────────────────────────────────────────────────────────────────
def get_pokemon(entry):
    name = entry['name']
    try:
        d = fetch(f"{BASE}/pokemon/{name}")
        sp = d.get('sprites', {})
        sp_other = sp.get('other', {})
        sprite = (sp_other.get('official-artwork',{}).get('front_default') or
                  sp_other.get('home',{}).get('front_default') or
                  sp.get('front_default'))

        types = [t['type']['name'] for t in d['types']]
        stats_map = {s['stat']['name']: s['base_stat'] for s in d.get('stats',[])}

        # Moves
        level_set = {}
        for m in d['moves']:
            mn = m['move']['name']
            for vd in m['version_group_details']:
                if vd['move_learn_method']['name'] == 'level-up':
                    if mn not in level_set:
                        level_set[mn] = {'url': m['move']['url'], 'level': vd['level_learned_at']}
                    break
        lvl_moves = sorted(
            [{'name':n,'url':v['url'],'level':v['level'],'byLevel':True} for n,v in level_set.items()],
            key=lambda x:(x['level'],x['name'])
        )
        other_moves = sorted(
            [{'name':m['move']['name'],'url':m['move']['url'],'level':None,'byLevel':False}
             for m in d['moves'] if m['move']['name'] not in level_set],
            key=lambda x:x['name']
        )
        all_moves = lvl_moves + other_moves

        # Species: is_legendary + name_es (solo para pokémon base, no formas alternativas)
        is_legendary = 0
        name_es = name
        generation = None
        if d['id'] <= 1025:
            try:
                sp_data = fetch(f"{BASE}/pokemon-species/{d['id']}")
                is_legendary = int(sp_data.get('is_legendary',False) or sp_data.get('is_mythical',False))
                generation = sp_data['generation']['name'] if sp_data.get('generation') else None
                for n in sp_data.get('names',[]):
                    if n['language']['name'] == 'es':
                        name_es = n['name']
                        break
            except Exception:
                pass

        return name, {
            'id':          d['id'],
            'name_es':     name_es,
            'types':       types,
            'sprite':      sprite,
            'sprites': {
                'front_default':          sp.get('front_default'),
                'front_shiny':            sp.get('front_shiny'),
                'official_artwork':       sp_other.get('official-artwork',{}).get('front_default'),
                'official_artwork_shiny': sp_other.get('official-artwork',{}).get('front_shiny'),
                'home':                   sp_other.get('home',{}).get('front_default'),
                'home_shiny':             sp_other.get('home',{}).get('front_shiny'),
            },
            'hp':          stats_map.get('hp',0),
            'attack':      stats_map.get('attack',0),
            'defense':     stats_map.get('defense',0),
            'sp_attack':   stats_map.get('special-attack',0),
            'sp_defense':  stats_map.get('special-defense',0),
            'speed':       stats_map.get('speed',0),
            'height':      d.get('height'),
            'weight':      d.get('weight'),
            'base_experience': d.get('base_experience'),
            'is_legendary':is_legendary,
            'generation':  generation,
            'moves':       all_moves,
            # evolves_from se añade en post-proceso con evo_map
        }
    except Exception as e:
        print(f"\n  ERROR {name}: {e}")
        return name, None

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    # Fase 0: evo map (paralelo)
    evo_map = build_evo_map()

    # Fase 1: lista pokémon (sin límite, coge todos)
    print("\n📥 Cargando lista de pokémon...")
    data = fetch(f"{BASE}/pokemon?limit=2000")
    entries = data['results']
    total_count = data['count']
    if total_count > 2000:
        data = fetch(f"{BASE}/pokemon?limit={total_count}&offset=0")
        entries = data['results']
    print(f"  {len(entries)} pokémon encontrados.")

    # Fase 2: datos pokémon
    print(f"\n⚡ Fase 1/3: datos pokémon ({POKE_WORKERS} en paralelo)...")
    pokemon_db = {}
    done = 0
    with ThreadPoolExecutor(max_workers=POKE_WORKERS) as ex:
        futures = {ex.submit(get_pokemon, e): e['name'] for e in entries}
        for f in as_completed(futures):
            name, result = f.result()
            done += 1
            if result:
                pokemon_db[name] = result
            print(f"\r  {done}/{len(entries)} ({done/len(entries)*100:.1f}%) — {name}{'  '*10}", end='', flush=True)
    print(f"\n  ✓ {len(pokemon_db)} pokémon cargados.")

    # Fase 3: moves únicos
    print("\n⚡ Fase 2/3: detalles de movimientos...")
    move_urls = {}
    for pdata in pokemon_db.values():
        for m in pdata['moves']:
            move_urls[m['name']] = m['url']
    print(f"  {len(move_urls)} movimientos únicos.")

    move_details = {}
    done = 0
    with ThreadPoolExecutor(max_workers=MOVE_WORKERS) as ex:
        futures = {ex.submit(get_move_detail, mn, url): mn for mn, url in move_urls.items()}
        for f in as_completed(futures):
            mn, detail = f.result()
            move_details[mn] = detail
            done += 1
            print(f"\r  {done}/{len(move_urls)} ({done/len(move_urls)*100:.1f}%) — {mn}{'  '*10}", end='', flush=True)
    print(f"\n  ✓ {len(move_details)} movimientos procesados.")

    # Fase 4: combinar
    print("\n🔧 Fase 3/3: combinando datos...")

    def get_base_name(name):
        """Extrae el nombre base de una forma alternativa: greninja-ash → greninja"""
        suffixes = ['-mega','-mega-x','-mega-y','-gmax','-alola','-galar','-hisui',
                    '-paldea','-ash','-original','-therian','-sky','-land','-speed',
                    '-attack','-defense','-plant','-sandy','-trash','-heat','-wash',
                    '-frost','-fan','-mow','-origin','-altered','-aria','-pirouette',
                    '-baile','-pom-pom','-pau','-sensu','-midday','-midnight','-dusk',
                    '-solo','-school','-dusk-mane','-dawn-wings','-ultra','-rapid-strike',
                    '-single-strike','-hero','-crowned','-eternamax','-primal','-low-key',
                    '-amped','-ice','-hangry','-full-belly','-noice','-roaming','-ordinary',
                    '-resolute','-battle-bond','-power-construct','-10','-50','-complete']
        for s in sorted(suffixes, key=len, reverse=True):
            if name.endswith(s):
                return name[:-len(s)]
        # Fallback: quitar último segmento tras guión si el base existe
        parts = name.rsplit('-', 1)
        if len(parts) == 2 and parts[0] in pokemon_db:
            return parts[0]
        return None

    for name, pdata in pokemon_db.items():
        pdata['evolves_from'] = evo_map.get(name)
        for m in pdata['moves']:
            m['detail'] = move_details.get(m['name'], {})
            m.pop('url', None)
        # Herencia de moves para formas alternativas sin movepool
        if pdata['id'] > 1025 and not pdata['moves']:
            base = get_base_name(name)
            if base and base in pokemon_db and pokemon_db[base]['moves']:
                pdata['moves'] = pokemon_db[base]['moves']
                print(f"  Moves heredados: {name} ← {base}")

    # Guardar (tmp → rename para evitar JSON vacío si se interrumpe)
    tmp = OUT_FILE + '.tmp'
    print(f"\n💾 Guardando en {OUT_FILE}...")
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump({'pokemon': pokemon_db, 'moves': move_details},
                  f, separators=(',',':'), ensure_ascii=False)
    os.replace(tmp, OUT_FILE)

    size_mb = os.path.getsize(OUT_FILE) / 1024 / 1024
    n_evo = sum(1 for p in pokemon_db.values() if p.get('evolves_from'))
    print(f"✅ Listo! {size_mb:.1f} MB")
    print(f"   Pokémon: {len(pokemon_db)} | Con evolves_from: {n_evo} | Moves: {len(move_details)}")

if __name__ == '__main__':
    main()
