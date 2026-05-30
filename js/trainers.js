// ══════════════════════════════════════════════════════
//  trainers.js — Batalla contra entrenadores
//  Depende de teams.js (ya cargado antes)
// ══════════════════════════════════════════════════════

let TRAINERS_DB = null;

// ── Carga de datos ────────────────────────────────────
async function initTrainers(){
  IS_TRAINER_PAGE = true; // bloquear edición equipo rival
  // teams.js ya cargó DB y allPokemon, esperamos si no está listo
  let tries = 0;
  while((!DB || !allPokemon.length) && tries < 30){
    await new Promise(r=>setTimeout(r,200));
    tries++;
  }

  try{
    const res = await fetch('data/trainers_db.json');
    if(!res.ok) throw new Error('No trainers DB');
    TRAINERS_DB = await res.json();
    buildGenSelector();
    document.getElementById('status-bar').innerHTML =
      `<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px">
       <span>${allPokemon.length} Pokémon · ${TRAINERS_DB.meta.total_trainers} entrenadores</span>`;
  }catch(e){
    document.getElementById('status-bar').textContent = 'Sin DB de entrenadores.';
  }

  // Lado B: openPokeModal bloqueado via IS_TRAINER_PAGE flag en teams.js
}

// ── Selectores ────────────────────────────────────────
function buildGenSelector(){
  const selGen = document.getElementById('sel-gen');
  // Obtener gens únicas
  const gens = [...new Set(TRAINERS_DB.games.map(g=>g.gen))].sort((a,b)=>a-b);
  selGen.innerHTML = '<option value="">— Gen —</option>' +
    gens.map(g=>`<option value="${g}">Generación ${g}</option>`).join('');
  selGen.disabled = false;
  selGen.onchange = onGenChange;
}

function onGenChange(){
  const gen = parseInt(document.getElementById('sel-gen').value);
  const selGame = document.getElementById('sel-game');
  const selTrainer = document.getElementById('sel-trainer');
  selTrainer.innerHTML = '<option value="">— Entrenador —</option>';
  selTrainer.disabled = true;
  document.getElementById('btn-load-trainer').disabled = true;

  if(!gen){ selGame.innerHTML='<option value="">— Juego —</option>'; selGame.disabled=true; return; }

  const games = TRAINERS_DB.games.filter(g=>g.gen===gen);
  selGame.innerHTML = '<option value="">— Juego —</option>' +
    games.map(g=>`<option value="${g.slug}">${g.name}</option>`).join('');
  selGame.disabled = false;
  selGame.value = '';
  selGame.onchange = onGameChange;
}

function onGameChange(){
  const slug = document.getElementById('sel-game').value;
  const selTrainer = document.getElementById('sel-trainer');
  document.getElementById('btn-load-trainer').disabled = true;

  if(!slug){ selTrainer.innerHTML='<option value="">— Entrenador —</option>'; selTrainer.disabled=true; return; }

  const trainers = TRAINERS_DB.trainers[slug] || [];
  // Ordenar: gym primero (por order), luego elite4 (por order), luego champion
  const sorted = [...trainers].sort((a,b)=>{
    const typeOrder = {gym:0, trial:0, kahuna:0, elite4:1, champion:2, other:3};
    const ta = typeOrder[a.type]??3, tb = typeOrder[b.type]??3;
    if(ta !== tb) return ta-tb;
    return (a.order||0)-(b.order||0);
  });

  selTrainer.innerHTML = '<option value="">— Entrenador —</option>';
  let lastType = '';
  sorted.forEach((t,i)=>{
    const typeLabel = {gym:'🏟 Líder', trial:'🏝 Capitán', kahuna:'🌺 Kahuna', elite4:'🏆 Alto Mando', champion:'👑 Campeón', other:'⚔ Otro'}[t.type]||'';
    if(t.type !== lastType){
      const og = document.createElement('optgroup');
      og.label = {gym:'── Líderes de Gimnasio ──', trial:'── Capitanes de Prueba ──', kahuna:'── Kahunas ──', elite4:'── Alto Mando ──', champion:'── Campeón ──', other:'── Otros ──'}[t.type]||t.type;
      selTrainer.appendChild(og);
      lastType = t.type;
    }
    const opt = document.createElement('option');
    opt.value = i; // índice en sorted
    opt.textContent = `${typeLabel} ${t.name}${t.location?' — '+t.location:''}`;
    opt.dataset.idx = trainers.indexOf(t); // índice en array original
    selTrainer.appendChild(opt);
  });

  selTrainer.disabled = false;
  selTrainer.value = '';
  selTrainer._sorted = sorted;
  selTrainer.onchange = ()=>{
    document.getElementById('btn-load-trainer').disabled = !selTrainer.value && selTrainer.value!=='0';
  };
}

// ── Cargar entrenador al lado B ───────────────────────
function loadTrainer(){
  const slug = document.getElementById('sel-game').value;
  const selTrainer = document.getElementById('sel-trainer');
  const idx = parseInt(selTrainer.value);
  if(!slug || isNaN(idx)) return;

  const sorted = selTrainer._sorted;
  const trainer = sorted[idx];
  if(!trainer) return;

  const gameName = document.getElementById('sel-game').options[document.getElementById('sel-game').selectedIndex].text;

  // Actualizar cabecera rival
  document.getElementById('trainer-b-name').textContent = trainer.name || 'Rival';
  document.getElementById('trainer-b-game').textContent = gameName;
  const tnb=document.getElementById('team-name-b'); if(tnb) tnb.value!==undefined ? tnb.value=trainer.name||'Rival' : tnb.textContent=trainer.name||'Rival';

  // Limpiar slots B
  for(let i=0;i<6;i++){
    teams.b[i]=null;
    const st=slotSt('b',i);
    st.shiny=false; st.stats=false;
  }

  // Renderizar sprite del entrenador arriba del lado B
  renderTrainerSprite(trainer, 'b');

  // Rellenar equipo B con los pokémon del entrenador
  trainer.team.forEach((tp, i)=>{
    if(i>=6) return;
    const pData = allPokemon.find(p=>p.name===tp.name);
    if(!pData) return;

    // Moves por nivel: filtrar los que aprende hasta el nivel del pokémon en el entrenador
    const level = tp.level || 100;
    const movesForLevel = getMovesForLevel(pData, level);

    teams.b[i] = {
      ...pData,
      moves: movesForLevel,
      trainerLevel: level,
    };
    slotSt('b',i).shiny=false;
    slotSt('b',i).stats=false;
  });

  renderAllSlots('b');
  // Añadir badge de nivel tras render
  setTimeout(()=>addLevelBadges(), 60);

  showToast(`Equipo de ${trainer.name} cargado.`, 'ok');
}

function getMovesForLevel(pData, level){
  // Obtener moves aprendidos por nivel hasta 'level', tomar los últimos 4
  const byLevel = (pData.allMoves||[])
    .filter(m => m.byLevel && m.level > 0 && m.level <= level && m.detail?.power)
    .sort((a,b) => b.level - a.level);

  // Tomar hasta 4 únicos por tipo/categoría para variedad
  const selected = [];
  const usedNames = new Set();
  for(const m of byLevel){
    if(usedNames.has(m.name)) continue;
    usedNames.add(m.name);
    selected.push(m);
    if(selected.length>=4) break;
  }
  // Si hay menos de 4, rellenar con moves de estado o sin daño
  if(selected.length < 4){
    const statusMoves = (pData.allMoves||[])
      .filter(m => m.byLevel && m.level>0 && m.level<=level && !usedNames.has(m.name))
      .sort((a,b)=>b.level-a.level);
    for(const m of statusMoves){
      if(selected.length>=4) break;
      if(usedNames.has(m.name)) continue;
      usedNames.add(m.name);
      selected.push(m);
    }
  }
  return selected;
}

function renderTrainerSprite(trainer, team){
  // Insertar sprite del entrenador antes de los slots
  const container = document.getElementById(`slots-${team}`);
  let wrap = document.getElementById('trainer-sprite-block');
  if(wrap) wrap.remove();
  if(!trainer.sprite) return;
  wrap = document.createElement('div');
  wrap.id = 'trainer-sprite-block';
  wrap.className = 'trainer-sprite-wrap';
  wrap.innerHTML = `
    <img class="trainer-sprite" src="${trainer.sprite}" alt="${trainer.name}" onerror="this.style.display='none'">
    <div class="trainer-sprite-name">${trainer.name}</div>
    ${trainer.specialty?`<div class="trainer-sprite-type">Tipo: ${trainer.specialty}</div>`:''}
    ${trainer.badge?`<div class="trainer-sprite-badge">${trainer.badge}</div>`:''}
  `;
  container.parentElement.insertBefore(wrap, container);
}

function addLevelBadges(){
  for(let i=0;i<6;i++){
    const p = teams.b[i];
    if(!p) continue;
    const slotEl = document.getElementById(`poke-row-b-${i}`);
    if(!slotEl) continue;
    const filled = slotEl.querySelector('.poke-slot-filled');
    if(filled && p.trainerLevel){
      if(!filled.querySelector('.rival-level-badge')){
        const badge = document.createElement('div');
        badge.className='rival-level-badge';
        badge.textContent=`Nv.${p.trainerLevel}`;
        filled.appendChild(badge);
      }
    }
  }
}

function clearTrainer(){
  showConfirm('¿Limpiar el equipo rival?', ()=>{
    for(let i=0;i<6;i++){
      teams.b[i]=null;
      const st=slotSt('b',i);
      st.shiny=false; st.stats=false;
    }
    const sprite = document.getElementById('trainer-sprite-block');
    if(sprite) sprite.remove();
    document.getElementById('trainer-b-name').textContent='Rival';
    document.getElementById('trainer-b-game').textContent='';
    const tnb2=document.getElementById('team-name-b'); if(tnb2) tnb2.value!==undefined ? tnb2.value='Rival' : tnb2.textContent='Rival';
    document.getElementById('sel-trainer').value='';
    document.getElementById('btn-load-trainer').disabled=true;
    renderAllSlots('b');
    showToast('Equipo rival limpiado.','info');
  });
}

// ── Sobreescribir openPokeModal para solo abrir en equipo A ───
const _origOpenPokeModal = window.openPokeModal;
window.openPokeModal = function(team){
  if(team === 'b') return; // bloquear edición del rival
  _origOpenPokeModal(team);
};

// ── Init ──────────────────────────────────────────────
initTrainers();
