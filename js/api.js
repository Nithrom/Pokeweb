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
  if (port === '8080' || port === '80' || port === '') {
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

function setStatusLoading(msg) {
  const bar = document.getElementById('status-bar');
  if (bar) bar.innerHTML = `<span class="spinner"></span> ${msg}`;
}

async function fetchApi(path, options = {}) {
  const timeoutMs = options.timeout ?? 30000;
  const { timeout: _t, ...fetchOpts } = options;
  const res = await fetch(apiUrl(path), {
    ...fetchOpts,
    headers: { Accept: 'application/json', ...(fetchOpts.headers || {}) },
    signal: AbortSignal.timeout(timeoutMs),
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

async function loadPokemonDbFromApi() {
  return fetchApi('/db/pokemon', { timeout: 300000 });
}

window.getApiBase = getApiBase;
window.fetchApi = fetchApi;
window.checkApiAvailable = checkApiAvailable;
window.useApi = useApi;
window.setStatusLoading = setStatusLoading;
window.loadPokemonDbFromApi = loadPokemonDbFromApi;
