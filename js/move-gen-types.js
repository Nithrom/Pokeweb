// Tipos de movimiento según la generación del juego (no el catálogo moderno).
(function (global) {
  /** throughGen: aplica si gameGen <= N; fromGen: aplica si gameGen >= N (el más alto gana). */
  const MOVE_TYPE_THRESHOLDS = {
    bite: [
      { throughGen: 1, type: 'normal' },
      { fromGen: 2, type: 'dark' },
    ],
    gust: [
      { throughGen: 1, type: 'normal' },
      { fromGen: 2, type: 'flying' },
    ],
    'karate-chop': [
      { throughGen: 1, type: 'normal' },
      { fromGen: 2, type: 'fighting' },
    ],
    'sand-attack': [
      { throughGen: 1, type: 'normal' },
      { fromGen: 2, type: 'ground' },
    ],
    charm: [
      { throughGen: 5, type: 'normal' },
      { fromGen: 6, type: 'fairy' },
    ],
    moonlight: [
      { throughGen: 5, type: 'normal' },
      { fromGen: 6, type: 'fairy' },
    ],
    'sweet-kiss': [
      { throughGen: 5, type: 'normal' },
      { fromGen: 6, type: 'fairy' },
    ],
    curse: [
      { throughGen: 4, type: 'unknown' },
      { fromGen: 5, type: 'ghost' },
    ],
  };

  function resolveMoveType(moveSlug, gameGen, catalogType) {
    const slug = String(moveSlug || '').toLowerCase();
    const gen = Number(gameGen) || 0;
    const fallback = catalogType || 'normal';
    const rules = MOVE_TYPE_THRESHOLDS[slug];
    if (!rules || gen < 1) return fallback;

    let resolved = fallback;
    for (const r of rules) {
      if (r.throughGen != null && gen <= r.throughGen) return r.type;
      if (r.fromGen != null && gen >= r.fromGen) resolved = r.type;
    }
    return resolved;
  }

  function detailForGen(detail, moveSlug, gameGen) {
    if (!detail) return detail;
    return {
      ...detail,
      type: resolveMoveType(moveSlug, gameGen, detail.type),
    };
  }

  global.PokeMoveGenTypes = {
    MOVE_TYPE_THRESHOLDS,
    resolveMoveType,
    detailForGen,
  };
})(typeof window !== 'undefined' ? window : globalThis);
