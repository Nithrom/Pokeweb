// ══════════════════════════════════════════════════════
//  api.js — Cliente REST → API Flask (Supabase)
// ══════════════════════════════════════════════════════

let _apiBase = null;
let _useApi = null;

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
      return false;
    }
    const data = await h.json();
    _useApi = data.status === 'ok' && data.db === 'connected';
  } catch {
    _useApi = false;
  }
  return _useApi;
}

function useApi() {
  return _useApi === true;
}

async function loadPokemonDbFromApi() {
  return fetchApi('/db/pokemon');
}

window.getApiBase = getApiBase;
window.fetchApi = fetchApi;
window.checkApiAvailable = checkApiAvailable;
window.useApi = useApi;
window.loadPokemonDbFromApi = loadPokemonDbFromApi;
