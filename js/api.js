// ══════════════════════════════════════════════════════
//  api.js — Cliente REST → MariaDB (Flask)
// ══════════════════════════════════════════════════════

let _apiBase = null;
let _useApi = null;

// ── POKEWEB-TEMP-DATA-SOURCE-INDICATOR (eliminar bloque entero más adelante) ──
// Buscar en el proyecto: POKEWEB-TEMP-DATA-SOURCE-INDICATOR

/** Origen real de cada dataset: 'api' | 'json' | 'pokeapi' | 'none' */
const DATA_SOURCES = {
  pokemon: { mode: null, detail: '' },
  trainers: { mode: null, detail: '' },
  apiReachable: null,
};

const SOURCE_LABELS = {
  api: { short: 'API · SQL', title: 'Datos desde MariaDB vía Flask' },
  json: { short: 'JSON', title: 'Archivo local en data/' },
  pokeapi: { short: 'PokeAPI', title: 'PokéAPI en línea (sin DB local)' },
  none: { short: 'Sin datos', title: 'No se pudo cargar' },
};

const PART_LABELS = { pokemon: 'Pokémon', trainers: 'Entrenadores' };

function getApiBase() {
  if (_apiBase) return _apiBase;
  if (typeof window.POKEWEB_API_BASE === 'string' && window.POKEWEB_API_BASE) {
    _apiBase = window.POKEWEB_API_BASE.replace(/\/$/, '');
    return _apiBase;
  }
  const { protocol, hostname, port } = window.location;
  if (protocol === 'file:') {
    _apiBase = 'http://127.0.0.1:5000';
    return _apiBase;
  }
  if (port === '8080' || port === '80' || port === '') {
    _apiBase = '/api';
    return _apiBase;
  }
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    _apiBase = 'http://127.0.0.1:5000';
    return _apiBase;
  }
  _apiBase = '/api';
  return _apiBase;
}

function apiUrl(path) {
  const base = getApiBase();
  const p = path.startsWith('/') ? path : `/${path}`;
  return base ? `${base}${p}` : p;
}

async function fetchApi(path, options = {}) {
  const res = await fetch(apiUrl(path), {
    ...options,
    headers: { Accept: 'application/json', ...(options.headers || {}) },
  });
  if (!res.ok) {
    const err = new Error(`API ${res.status}: ${path}`);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

async function checkApiAvailable() {
  if (_useApi !== null) return _useApi;
  try {
    const h = await fetch(apiUrl('/health'), { signal: AbortSignal.timeout(4000) });
    if (!h.ok) {
      _useApi = false;
      DATA_SOURCES.apiReachable = false;
      return false;
    }
    const data = await h.json();
    _useApi = data.status === 'ok' && data.db === 'connected';
    DATA_SOURCES.apiReachable = _useApi;
  } catch {
    _useApi = false;
    DATA_SOURCES.apiReachable = false;
  }
  updateDataSourceUI();
  return _useApi;
}

function useApi() {
  return _useApi === true;
}

function setDataSource(part, mode, detail = '') {
  if (!DATA_SOURCES[part]) return;
  DATA_SOURCES[part] = { mode, detail };
  updateDataSourceUI();
}

function setPokemonDataSource(mode, detail = '') {
  setDataSource('pokemon', mode, detail);
}

function setTrainersDataSource(mode, detail = '') {
  setDataSource('trainers', mode, detail);
}

/** Resumen para consola o depuración */
function getDataSourceSummary() {
  const p = DATA_SOURCES.pokemon.mode || '—';
  const t = DATA_SOURCES.trainers.mode || '—';
  return {
    apiReachable: DATA_SOURCES.apiReachable,
    apiBase: getApiBase(),
    pokemon: p,
    trainers: t,
    usingApi: useApi(),
  };
}

function ensureBadgeContainer() {
  let el = document.getElementById('data-source-badges');
  if (el) return el;
  const bar = document.getElementById('status-bar');
  if (!bar) return null;
  el = document.createElement('div');
  el.id = 'data-source-badges';
  el.className = 'data-source-badges pokeweb-temp-data-source';
  el.setAttribute('data-pokeweb-temp', 'data-source-indicator');
  el.setAttribute('aria-label', 'Origen de los datos (indicador temporal)');
  bar.insertAdjacentElement('afterend', el);
  return el;
}

function renderOneBadge(part, mode, detail) {
  const meta = SOURCE_LABELS[mode] || SOURCE_LABELS.none;
  const partName = PART_LABELS[part] || part;
  const title = [meta.title, detail, partName].filter(Boolean).join(' · ');
  return `<span class="data-source-badge data-source-${mode}" data-pokeweb-temp="data-source-indicator" title="${title.replace(/"/g, '&quot;')}">` +
    `<span class="ds-part">${partName}</span>${meta.short}<span class="ds-temp-tag" aria-hidden="true"> · temp</span></span>`;
}

/** Pinta badges bajo la barra de estado. parts = ['pokemon'] o ['pokemon','trainers'] */
function updateDataSourceUI(parts = null) {
  const container = ensureBadgeContainer();
  if (!container) return;

  const show = parts || ['pokemon', 'trainers'].filter(k => DATA_SOURCES[k]?.mode);
  if (!show.length) {
    container.hidden = true;
    return;
  }

  const html = show
    .map(key => {
      const s = DATA_SOURCES[key];
      if (!s?.mode) return '';
      return renderOneBadge(key, s.mode, s.detail);
    })
    .filter(Boolean)
    .join('');

  if (!html) {
    container.hidden = true;
    return;
  }
  container.innerHTML = html;
  container.hidden = false;
}

async function loadPokemonDbFromApi() {
  return fetchApi('/db/pokemon');
}

window.getApiBase = getApiBase;
window.fetchApi = fetchApi;
window.checkApiAvailable = checkApiAvailable;
window.useApi = useApi;
window.loadPokemonDbFromApi = loadPokemonDbFromApi;
window.setPokemonDataSource = setPokemonDataSource;
window.setTrainersDataSource = setTrainersDataSource;
window.updateDataSourceUI = updateDataSourceUI;
window.getDataSourceSummary = getDataSourceSummary;
window.POKEWEB_DATA_SOURCES = DATA_SOURCES;
// ── fin POKEWEB-TEMP-DATA-SOURCE-INDICATOR ──
