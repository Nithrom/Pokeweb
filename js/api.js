// ══════════════════════════════════════════════════════
//  api.js — Cliente REST → API Flask (Supabase / PostgreSQL o MariaDB local)
// ══════════════════════════════════════════════════════

let _apiBase = null;
let _useApi = null;

/** API en producción (Railway); override con window.POKEWEB_API_BASE si cambia el dominio. */
const POKEWEB_DEFAULT_PROD_API = 'https://api-pokeweb.up.railway.app';

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
  if (hostname === 'localhost' || hostname === '127.0.0.1') {
    _apiBase = 'http://127.0.0.1:5000';
    return _apiBase;
  }
  if (hostname.includes('railway.app')) {
    _apiBase = POKEWEB_DEFAULT_PROD_API;
    return _apiBase;
  }
  if (port === '8080' || port === '80') {
    _apiBase = '/api';
    return _apiBase;
  }
  _apiBase = POKEWEB_DEFAULT_PROD_API;
  return _apiBase;
}

function apiUrl(path) {
  const base = getApiBase();
  const p = path.startsWith('/') ? path : `/${path}`;
  return base ? `${base}${p}` : p;
}

async function fetchApi(path, options = {}) {
  const url = apiUrl(path);
  let res;
  try {
    res = await fetch(url, {
      ...options,
      headers: { Accept: 'application/json', ...(options.headers || {}) },
    });
  } catch (e) {
    const err = new Error(`Red: ${url} — ${e.message || e}`);
    err.cause = e;
    throw err;
  }
  if (!res.ok) {
    const err = new Error(`API ${res.status}: ${url}`);
    err.status = res.status;
    throw err;
  }
  const data = await res.json();
  if (!Array.isArray(data) && path.includes('/trainers') && data?.error) {
    throw new Error(data.error);
  }
  return data;
}

async function checkApiAvailable() {
  if (_useApi !== null) return _useApi;
  try {
    const h = await fetch(apiUrl('/health'), { signal: AbortSignal.timeout(12000) });
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

async function loadPokemonDbFromApi(opts = {}) {
  const lite = opts.lite ? '?lite=1' : '';
  return fetchApi(`/db/pokemon${lite}`);
}

window.getApiBase = getApiBase;
window.fetchApi = fetchApi;
window.checkApiAvailable = checkApiAvailable;
window.useApi = useApi;
window.loadPokemonDbFromApi = loadPokemonDbFromApi;
