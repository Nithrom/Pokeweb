// Tipos de movimiento por generación (debe coincidir con api/move_gen_types.py)
(function () {
  const RULES = {
    bite: [[1, 1, 'normal'], [2, null, 'dark']],
    gust: [[1, 1, 'normal'], [2, null, 'flying']],
    'karate-chop': [[1, 1, 'normal'], [2, null, 'fighting']],
    'sand-attack': [[1, 1, 'normal'], [2, null, 'ground']],
    curse: [[2, 4, 'unknown'], [5, null, 'ghost']],
    charm: [[2, 5, 'normal'], [6, null, 'fairy']],
    moonlight: [[2, 5, 'normal'], [6, null, 'fairy']],
    'sweet-kiss': [[2, 5, 'normal'], [6, null, 'fairy']],
  };

  const ALIASES = {
    'karate chop': 'karate-chop',
    'sand attack': 'sand-attack',
    'sweet kiss': 'sweet-kiss',
  };

  function normalizeSlug(name) {
    if (!name) return '';
    const key = String(name).trim().toLowerCase().replace(/_/g, '-');
    return ALIASES[key] || key.replace(/\s+/g, '-');
  }

  function typeForGen(moveName, gameGen, defaultType) {
    const def = defaultType || 'normal';
    const gen = Number(gameGen);
    if (!Number.isFinite(gen) || gen < 1) return def;
    const rules = RULES[normalizeSlug(moveName)];
    if (!rules) return def;
    for (const [min, max, type] of rules) {
      if (gen < min) continue;
      if (max !== null && gen > max) continue;
      return type;
    }
    return def;
  }

  function detailForGen(detail, moveName, gameGen) {
    const d = detail || {};
    const type = typeForGen(moveName, gameGen, d.type || 'normal');
    return { ...d, type };
  }

  window.PokeMoveGenTypes = { normalizeSlug, typeForGen, detailForGen, RULES };
})();
