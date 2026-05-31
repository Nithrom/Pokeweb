// ══════════════════════════════════════════════════════
//  trainers.js — Batalla contra entrenadores
//  Depende de teams.js (ya cargado antes)
// ══════════════════════════════════════════════════════

let TRAINERS_DB = null;

// Iniciales por generación (tu elección → equipo rival según el juego)
const GEN_STARTERS={
  1:[{id:'bulbasaur',label:'Bulbasaur'},{id:'charmander',label:'Charmander'},{id:'squirtle',label:'Squirtle'}],
  2:[{id:'chikorita',label:'Chikorita'},{id:'cyndaquil',label:'Cyndaquil'},{id:'totodile',label:'Totodile'}],
  3:[{id:'treecko',label:'Treecko'},{id:'torchic',label:'Torchic'},{id:'mudkip',label:'Mudkip'}],
  4:[{id:'turtwig',label:'Turtwig'},{id:'chimchar',label:'Chimchar'},{id:'piplup',label:'Piplup'}],
  5:[{id:'snivy',label:'Snivy'},{id:'tepig',label:'Tepig'},{id:'oshawott',label:'Oshawott'}],
  6:[{id:'chespin',label:'Chespin'},{id:'fennekin',label:'Fennekin'},{id:'froakie',label:'Froakie'}],
  7:[{id:'rowlet',label:'Rowlet'},{id:'litten',label:'Litten'},{id:'popplio',label:'Popplio'}],
  8:[{id:'grookey',label:'Grookey'},{id:'scorbunny',label:'Scorbunny'},{id:'sobble',label:'Sobble'}],
  9:[{id:'sprigatito',label:'Sprigatito'},{id:'fuecoco',label:'Fuecoco'},{id:'quaxly',label:'Quaxly'}],
};

// Evoluciones finales de los iniciales (para detectar variantes en el JSON)
const STARTER_FINALS_BY_GEN={
  1:['venusaur','charizard','blastoise'],
  2:['meganium','typhlosion','feraligatr'],
  3:['sceptile','blaziken','swampert'],
  4:['torterra','infernape','empoleon'],
  5:['serperior','emboar','samurott'],
  6:['chesnaught','delphox','greninja'],
  7:['decidueye','incineroar','primarina'],
  8:['rillaboom','cinderace','inteleon'],
  9:['meowscarada','skeledirge','quaquaval'],
};

/** Pokémon final que lleva el rival si tú eliges ese inicial (ventaja de tipo). */
const RIVAL_COUNTER_BY_GEN={
  1:{bulbasaur:'charizard',charmander:'blastoise',squirtle:'venusaur'},
  2:{chikorita:'typhlosion',cyndaquil:'feraligatr',totodile:'meganium'},
  3:{treecko:'swampert',torchic:'sceptile',mudkip:'blaziken'},
  4:{turtwig:'infernape',chimchar:'empoleon',piplup:'torterra'},
  5:{snivy:'emboar',tepig:'samurott',oshawott:'serperior'},
  6:{chespin:'delphox',fennekin:'greninja',froakie:'chesnaught'},
  7:{rowlet:'incineroar',litten:'primarina',popplio:'decidueye'},
  8:{grookey:'cinderace',scorbunny:'inteleon',sobble:'rillaboom'},
  9:{sprigatito:'skeledirge',fuecoco:'quaquaval',quaxly:'meowscarada'},
};

/** Hau (USUM): Eevee evoluciona a la ventaja sobre tu inicial. */
const HAU_EEVEELUTION={rowlet:'flareon',litten:'vaporeon',popplio:'leafeon'};
const EEVEELUTIONS=new Set(['vaporeon','jolteon','flareon','espeon','umbreon','leafeon','glaceon','sylveon']);

const MAX_TEAM=6;

function getGameGen(slug){
  return TRAINERS_DB?.games?.find(g=>g.slug===slug)?.gen||0;
}

function updateLoadTrainerButton(){
  const slug=document.getElementById('sel-game').value;
  const trainerVal=document.getElementById('sel-trainer').value;
  const starterEl=document.getElementById('sel-starter');
  const gen=getGameGen(slug);
  const needsStarter=!!slug&&!!GEN_STARTERS[gen];
  const starterOk=!needsStarter||!!starterEl.value;
  const trainerOk=trainerVal!==''&&!isNaN(parseInt(trainerVal));
  document.getElementById('btn-load-trainer').disabled=!(slug&&trainerOk&&starterOk);
}

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
    buildGameSelector();
    resetStarterSelector();
    document.getElementById('status-bar').innerHTML =
      `<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px">
       <span>${allPokemon.length} Pokémon · ${TRAINERS_DB.meta.total_trainers} entrenadores</span>`;
  }catch(e){
    document.getElementById('status-bar').textContent = 'Sin DB de entrenadores.';
  }

  // Lado B: openPokeModal bloqueado via IS_TRAINER_PAGE flag en teams.js
}

// ── Selectores ────────────────────────────────────────
function buildGameSelector(){
  const selGame = document.getElementById('sel-game');
  const gens = [...new Set(TRAINERS_DB.games.map(g=>g.gen))].sort((a,b)=>a-b);
  selGame.innerHTML = '<option value="">— Juego —</option>';
  gens.forEach(gen=>{
    const og = document.createElement('optgroup');
    og.label = `Gen ${gen}`;
    TRAINERS_DB.games.filter(g=>g.gen===gen).forEach(g=>{
      const opt = document.createElement('option');
      opt.value = g.slug;
      opt.textContent = `- ${g.name}`;
      og.appendChild(opt);
    });
    selGame.appendChild(og);
  });
  selGame.disabled = false;
  selGame.onchange = onGameChange;
}

function resetStarterSelector(){
  const sel=document.getElementById('sel-starter');
  sel.innerHTML='<option value="">— Elige juego —</option>';
  sel.disabled=true;
  sel.value='';
  sel.onchange=updateLoadTrainerButton;
}

function buildStarterSelector(slug){
  const sel=document.getElementById('sel-starter');
  const gen=getGameGen(slug);
  const starters=GEN_STARTERS[gen];

  if(!slug||!starters){
    resetStarterSelector();
    return;
  }

  sel.innerHTML=starters.map(s=>`<option value="${s.id}">${s.label}</option>`).join('');
  sel.disabled=false;
  sel.value=starters[0].id;
  sel.onchange=updateLoadTrainerButton;
}

function onGameChange(){
  const slug = document.getElementById('sel-game').value;
  const selTrainer = document.getElementById('sel-trainer');
  updateLoadTrainerButton();

  if(!slug){
    selTrainer.innerHTML='<option value="">— Entrenador —</option>';
    selTrainer.disabled=true;
    buildStarterSelector('');
    return;
  }

  buildStarterSelector(slug);

  const trainers = TRAINERS_DB.trainers[slug] || [];
  // Ordenar: gym/kahuna → elite4 → champion → captain (Alola)
  const sorted = [...trainers].sort((a,b)=>{
    const typeOrder = {gym:0, kahuna:0, elite4:1, champion:2, captain:3, other:4};
    const ta = typeOrder[a.type]??4, tb = typeOrder[b.type]??4;
    if(ta !== tb) return ta-tb;
    return (a.order||0)-(b.order||0);
  });

  selTrainer.innerHTML = '<option value="">— Entrenador —</option>';
  let lastType = '';
  sorted.forEach((t,i)=>{
    const typeLabel = {gym:'🏟 Líder', kahuna:'🌺 Kahuna', captain:'🏝 Capitán', elite4:'🏆 Alto Mando', champion:'👑 Campeón', other:'⚔ Otro'}[t.type]||'';
    if(t.type !== lastType){
      const og = document.createElement('optgroup');
      og.label = {gym:'── Líderes de Gimnasio ──', kahuna:'── Kahunas ──', captain:'── Capitanes ──', elite4:'── Alto Mando ──', champion:'── Campeón ──', other:'── Otros ──'}[t.type]||t.type;
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
  selTrainer.onchange = updateLoadTrainerButton;
  updateLoadTrainerButton();
}

/** Quita variantes de iniciales rivales y fusiones de combates duplicados en el scrape. */
function resolveTrainerTeam(trainer, slug, starterId){
  let team=[...(trainer.team||[])];
  const gen=getGameGen(slug);
  const finals=STARTER_FINALS_BY_GEN[gen]||[];
  const keepFinal=RIVAL_COUNTER_BY_GEN[gen]?.[starterId];
  const finalsInTeam=finals.filter(f=>team.some(p=>p.name===f));

  // Hau (USUM): primero Eeveelución según tu inicial, luego la final de Alola
  if(trainer.name==='Hau'&&slug.includes('ultra')){
    const keepEevee=HAU_EEVEELUTION[starterId];
    team=team.filter(p=>!EEVEELUTIONS.has(p.name)||p.name===keepEevee);
  }

  if(finalsInTeam.length>=2&&keepFinal){
    const nonFinal=team.filter(p=>!finals.includes(p.name));
    const kept=team.find(p=>p.name===keepFinal);
    if(kept)team=[...nonFinal.slice(0,MAX_TEAM-1),kept];
    else team=nonFinal.slice(0,MAX_TEAM);
  }

  if(team.length>MAX_TEAM)team=trimTeamByLevelCluster(team,trainer.type);
  if(team.length>MAX_TEAM)team=team.slice(0,MAX_TEAM);
  return team;
}

function trimTeamByLevelCluster(team,trainerType){
  if(team.length<=MAX_TEAM)return team;
  const clusters=[];
  let cur=[team[0]];
  for(let i=1;i<team.length;i++){
    const prev=team[i-1].level||0;
    const lv=team[i].level||0;
    if(Math.abs(lv-prev)>=12){
      clusters.push(cur);
      cur=[team[i]];
    }else cur.push(team[i]);
  }
  clusters.push(cur);
  if(clusters.length<=1)return team.slice(0,MAX_TEAM);
  const preferHigh=['elite4','champion','kahuna'].includes(trainerType);
  const pick=preferHigh?clusters[clusters.length-1]:clusters[0];
  return pick.length<=MAX_TEAM?pick:pick.slice(0,MAX_TEAM);
}

// ── Resolver nombre de pokémon del entrenador → pokemon_db ──
function resolveTrainerPokemon(tp){
  if(!tp?.name)return null;
  let p=allPokemon.find(x=>x.name===tp.name);
  if(p)return p;

  const display=(tp.name_display||'').toLowerCase();
  if(tp.name==='lycanroc'){
    if(display.includes('midnight'))return allPokemon.find(x=>x.name==='lycanroc-midnight');
    if(display.includes('dusk'))return allPokemon.find(x=>x.name==='lycanroc-dusk');
    if(display.includes('midday'))return allPokemon.find(x=>x.name==='lycanroc-midday');
    return allPokemon.find(x=>x.name==='lycanroc-midday');
  }
  if(display.includes('alolan')){
    p=allPokemon.find(x=>x.name===`${tp.name}-alola`);
    if(p)return p;
  }
  if(display.includes('galarian')){
    p=allPokemon.find(x=>x.name===`${tp.name}-galar`);
    if(p)return p;
  }
  return null;
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
  const starterId=document.getElementById('sel-starter').value;
  const resolvedTeam=resolveTrainerTeam(trainer,slug,starterId);
  const starterLabel=document.getElementById('sel-starter').selectedOptions[0]?.textContent||'';

  document.getElementById('trainer-b-name').textContent = trainer.name || 'Rival';
  document.getElementById('trainer-b-game').textContent =
    starterLabel?`${gameName} · Inicial: ${starterLabel}`:gameName;
  const tnb=document.getElementById('team-name-b'); if(tnb) tnb.value!==undefined ? tnb.value=trainer.name||'Rival' : tnb.textContent=trainer.name||'Rival';

  for(let i=0;i<MAX_TEAM;i++){
    teams.b[i]=null;
    const st=slotSt('b',i);
    st.shiny=false; st.stats=false;
  }

  renderTrainerSprite(trainer, 'b');

  let skipped=0;
  resolvedTeam.forEach((tp,i)=>{
    if(i>=MAX_TEAM)return;
    const pData=resolveTrainerPokemon(tp);
    if(!pData){ skipped++; return; }

    const level = tp.level || 100;
    const moves = resolveTrainerMoves(pData, tp);

    teams.b[i] = {
      ...pData,
      moves,
      trainerLevel: level,
    };
    slotSt('b',i).shiny=false;
    slotSt('b',i).stats=false;
  });

  renderAllSlots('b');
  setTimeout(()=>addLevelBadges(), 60);

  const loaded=resolvedTeam.length-skipped;
  const msg=skipped
    ? `Equipo de ${trainer.name}: ${loaded}/${resolvedTeam.length} Pokémon (${skipped} sin datos en la DB).`
    : `Equipo de ${trainer.name} cargado (${loaded} Pokémon).`;
  showToast(msg, skipped?'warn':'ok');
}

/** Movimientos del JSON (Bulbapedia) o inferidos por nivel si faltan. */
function resolveTrainerMoves(pData, tp){
  const raw = tp.moves || [];
  if(!raw.length) return getMovesForLevel(pData, tp.level || 100);

  const out = [];
  for(const m of raw.slice(0, 4)){
    const name = typeof m === 'string' ? m : m.name;
    if(!name) continue;
    const fromSlot = pData.allMoves?.find(x => x.name === name);
    const global = DB?.moves?.[name];
    const detail = fromSlot?.detail || global || {
      type: 'normal', category: 'status', power: null, accuracy: null, pp: null,
    };
    out.push({
      name,
      byLevel: false,
      level: 0,
      detail: {
        type: detail.type || 'normal',
        category: detail.category || 'status',
        power: detail.power ?? null,
        accuracy: detail.accuracy ?? null,
        pp: detail.pp ?? null,
      },
    });
  }
  if(out.length) return out;
  return getMovesForLevel(pData, tp.level || 100);
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

    ${trainer.badge?`<div class="trainer-sprite-badge">${trainer.badge}</div>`:''}
  `;
  container.parentElement.insertBefore(wrap, container);
}

function addLevelBadges(){
  for(let i=0;i<MAX_TEAM;i++){
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
    for(let i=0;i<MAX_TEAM;i++){
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

// ── Radar 20% más pequeño en trainers ────────────────
const _origDrawRadar2=drawRadar;
drawRadar=function(canvasId,p,team){
  const canvas=document.getElementById(canvasId);if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height,r=Math.min(W,H)/2-28;
  ctx.clearRect(0,0,W,H);
  _drawRadarCore(ctx,W/2,H/2,r,STAT_KEYS.map(s=>p[s.key]||0),(team==='b')?'#ffaa33':'#4a9eff',0.8);
};
const _origDrawRadarOnCanvas2=drawRadarOnCanvas;
drawRadarOnCanvas=function(canvasId,p,team){
  const canvas=document.getElementById(canvasId);if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height,r=Math.min(W,H)/2-28;
  ctx.clearRect(0,0,W,H);
  _drawRadarCore(ctx,W/2,H/2,r,STAT_KEYS.map(s=>p[s.key]||0),(team==='b')?'#ffaa33':'#4a9eff',0.8);
};

// ── Init ──────────────────────────────────────────────
initTrainers();
