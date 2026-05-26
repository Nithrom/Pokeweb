// ══════════════════════════════════════════════════════
//  teams.js — Página de batalla por equipos
// ══════════════════════════════════════════════════════

const TIPOS_ES={normal:'Normal',fighting:'Lucha',flying:'Volador',poison:'Veneno',ground:'Tierra',rock:'Roca',bug:'Bicho',ghost:'Fantasma',steel:'Acero',fire:'Fuego',water:'Agua',grass:'Planta',electric:'Eléctrico',psychic:'Psíquico',ice:'Hielo',dragon:'Dragón',dark:'Siniestro',fairy:'Hada'};
const TYPE_CLASS={normal:'t-normal',fighting:'t-fighting',flying:'t-flying',poison:'t-poison',ground:'t-ground',rock:'t-rock',bug:'t-bug',ghost:'t-ghost',steel:'t-steel',fire:'t-fire',water:'t-water',grass:'t-grass',electric:'t-electric',psychic:'t-psychic',ice:'t-ice',dragon:'t-dragon',dark:'t-dark',fairy:'t-fairy'};
const CAT_IMG={physical:'img/cat_physical.png',special:'img/cat_special.png',status:'img/cat_status.png'};
const STAT_KEYS=[{key:'hp',label:'PS',cls:'sb-hp'},{key:'attack',label:'ATQ',cls:'sb-atk'},{key:'defense',label:'DEF',cls:'sb-def'},{key:'sp_attack',label:'ATQE',cls:'sb-spa'},{key:'sp_defense',label:'DEFE',cls:'sb-spd'},{key:'speed',label:'VEL',cls:'sb-spe'}];
const ALL_TYPES=Object.keys(TIPOS_ES);

const EFF={
  normal:{normal:1,fighting:1,flying:1,poison:1,ground:1,rock:0.5,bug:1,ghost:0,steel:0.5,fire:1,water:1,grass:1,electric:1,psychic:1,ice:1,dragon:1,dark:1,fairy:1},
  fighting:{normal:2,fighting:1,flying:0.5,poison:0.5,ground:1,rock:2,bug:0.5,ghost:0,steel:2,fire:1,water:1,grass:1,electric:1,psychic:0.5,ice:2,dragon:1,dark:2,fairy:0.5},
  flying:{normal:1,fighting:2,flying:1,poison:1,ground:1,rock:0.5,bug:2,ghost:1,steel:0.5,fire:1,water:1,grass:2,electric:0.5,psychic:1,ice:1,dragon:1,dark:1,fairy:1},
  poison:{normal:1,fighting:1,flying:1,poison:0.5,ground:0.5,rock:0.5,bug:1,ghost:0.5,steel:0,fire:1,water:1,grass:2,electric:1,psychic:1,ice:1,dragon:1,dark:1,fairy:2},
  ground:{normal:1,fighting:1,flying:0,poison:2,ground:1,rock:2,bug:0.5,ghost:1,steel:2,fire:2,water:1,grass:0.5,electric:2,psychic:1,ice:1,dragon:1,dark:1,fairy:1},
  rock:{normal:1,fighting:0.5,flying:2,poison:1,ground:0.5,rock:1,bug:2,ghost:1,steel:0.5,fire:2,water:1,grass:1,electric:1,psychic:1,ice:2,dragon:1,dark:1,fairy:1},
  bug:{normal:1,fighting:0.5,flying:0.5,poison:0.5,ground:1,rock:1,bug:1,ghost:0.5,steel:0.5,fire:0.5,water:1,grass:2,electric:1,psychic:2,ice:1,dragon:1,dark:2,fairy:0.5},
  ghost:{normal:0,fighting:1,flying:1,poison:1,ground:1,rock:1,bug:1,ghost:2,steel:1,fire:1,water:1,grass:1,electric:1,psychic:2,ice:1,dragon:1,dark:0.5,fairy:1},
  steel:{normal:1,fighting:1,flying:1,poison:1,ground:1,rock:2,bug:1,ghost:1,steel:0.5,fire:0.5,water:0.5,grass:1,electric:0.5,psychic:1,ice:2,dragon:1,dark:1,fairy:2},
  fire:{normal:1,fighting:1,flying:1,poison:1,ground:1,rock:0.5,bug:2,ghost:1,steel:2,fire:0.5,water:0.5,grass:2,electric:1,psychic:1,ice:2,dragon:0.5,dark:1,fairy:1},
  water:{normal:1,fighting:1,flying:1,poison:1,ground:2,rock:2,bug:1,ghost:1,steel:1,fire:2,water:0.5,grass:0.5,electric:1,psychic:1,ice:1,dragon:0.5,dark:1,fairy:1},
  grass:{normal:1,fighting:1,flying:0.5,poison:0.5,ground:2,rock:2,bug:0.5,ghost:1,steel:0.5,fire:0.5,water:2,grass:0.5,electric:1,psychic:1,ice:1,dragon:0.5,dark:1,fairy:1},
  electric:{normal:1,fighting:1,flying:2,poison:1,ground:0,rock:1,bug:1,ghost:1,steel:1,fire:1,water:2,grass:0.5,electric:0.5,psychic:1,ice:1,dragon:0.5,dark:1,fairy:1},
  psychic:{normal:1,fighting:2,flying:1,poison:2,ground:1,rock:1,bug:1,ghost:1,steel:0.5,fire:1,water:1,grass:1,electric:1,psychic:0.5,ice:1,dragon:1,dark:0,fairy:1},
  ice:{normal:1,fighting:1,flying:2,poison:1,ground:2,rock:1,bug:1,ghost:1,steel:0.5,fire:0.5,water:0.5,grass:2,electric:1,psychic:1,ice:0.5,dragon:2,dark:1,fairy:1},
  dragon:{normal:1,fighting:1,flying:1,poison:1,ground:1,rock:1,bug:1,ghost:1,steel:0.5,fire:1,water:1,grass:1,electric:1,psychic:1,ice:1,dragon:2,dark:1,fairy:0},
  dark:{normal:1,fighting:0.5,flying:1,poison:1,ground:1,rock:1,bug:1,ghost:2,steel:1,fire:1,water:1,grass:1,electric:1,psychic:2,ice:1,dragon:1,dark:0.5,fairy:0.5},
  fairy:{normal:1,fighting:2,flying:1,poison:0.5,ground:1,rock:1,bug:1,ghost:1,steel:0.5,fire:0.5,water:1,grass:1,electric:1,psychic:1,ice:1,dragon:2,dark:2,fairy:1}
};

function tc(t){return TYPE_CLASS[t]||'t-normal';}
function tn(t){return TIPOS_ES[t]||t;}
function formatName(n){return n.split('-').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');}

function multLabel(m){
  if(m>=4)return{txt:'×4',cls:'rm-4',mc:'mc-4'};
  if(m>=2)return{txt:'×2',cls:'rm-2',mc:'mc-2'};
  if(m>=1)return{txt:'×1',cls:'rm-1',mc:'mc-1'};
  if(m>0) return{txt:'×½',cls:'rm-05',mc:'mc-05'};
  return{txt:'×0',cls:'rm-0',mc:'mc-0'};
}

function calcDefense(types){
  const r={4:[],2:[],1:[],0.5:[],0.25:[],0:[]};
  for(const a of ALL_TYPES){
    let m=1;for(const d of types)m*=(EFF[a][d]??1);
    const k=Math.round(m*100)/100;
    if(r[k]!==undefined)r[k].push(a);else if(k>=3)r[4].push(a);else r[1].push(a);
  }
  return r;
}

function bestMult(attacker, defender){
  // attacker: {moves:[{detail:{type,power,category}}], types:[]}
  // Usa moves si hay ofensivos, si no usa tipos del atacante
  const offMoves=attacker.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status');
  const sources=offMoves.length>0?offMoves.map(m=>m.detail.type):attacker.types;
  let best=0;
  for(const atkType of sources){
    let m=1;for(const dt of defender.types)m*=(EFF[atkType]?.[dt]??1);
    m=Math.round(m*100)/100;if(m>best)best=m;
  }
  return best;
}

function powerClass(p){if(!p)return'pow-none';if(p>=100)return'pow-high';if(p>=60)return'pow-mid';return'pow-low';}

// ── Estado global ──────────────────────────────────────
let DB=null;
let allPokemon=[];  // [{name,id,types,sprite,is_legendary,allMoves}]

// 2 equipos × 6 slots
const teams={a:Array(6).fill(null),b:Array(6).fill(null)};

// ── Estado modal pokémon ──
const _mPoke={team:null,slotIdx:null,filtered:[],shown:0,typeFilters:[],flags:{legendary:false,physical:false,special:false}};
const BATCH=50;

// ── Estado modal moves ──
const _mMoves={team:null,slotIdx:null,selected:new Set()};

// ── Estado stats shiny ──
const _slotState={};// key: "a-0" → {shiny:false,statsOpen:false}
function slotState(team,idx){const k=`${team}-${idx}`;if(!_slotState[k])_slotState[k]={shiny:false,statsOpen:false};return _slotState[k];}

// ══════════════════════════════════════════════════════
//  INIT
// ══════════════════════════════════════════════════════
async function init(){
  // Generar slots vacíos
  renderAllSlots('a');
  renderAllSlots('b');
  buildTypeFilterRow();

  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      DB=await res.json();
      // Construir lista plana con stats y moves ya disponibles
      allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({
        name,id:p.id,types:p.types,sprite:p.sprite,
        is_legendary:p.is_legendary||false,
        hp:p.hp||0,attack:p.attack||0,defense:p.defense||0,
        sp_attack:p.sp_attack||0,sp_defense:p.sp_defense||0,speed:p.speed||0,
        allMoves:(p.moves||[]).map(m=>({
          name:m.name,byLevel:m.byLevel,level:m.level,
          detail:m.detail||(DB.moves&&DB.moves[m.name])||{type:'normal',category:'status',power:null,accuracy:null,pp:null}
        }))
      })).sort((a,b)=>a.id-b.id);
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"><span>${allPokemon.length} Pokémon disponibles</span>`;
    }
  }catch(e){
    document.getElementById('status-bar').textContent='Sin DB local — algunas funciones limitadas.';
  }
}

// ══════════════════════════════════════════════════════
//  RENDER DE SLOTS
// ══════════════════════════════════════════════════════
function renderAllSlots(team){
  const container=document.getElementById(`slots-${team}`);
  container.innerHTML='';
  for(let i=0;i<6;i++) container.appendChild(buildSlotEl(team,i));
}

function buildSlotEl(team,idx){
  const wrap=document.createElement('div');
  wrap.className='poke-row';
  wrap.id=`poke-row-${team}-${idx}`;
  const p=teams[team][idx];
  if(!p){
    wrap.innerHTML=`
      <div class="poke-row-top">
        <div class="poke-slot-empty" onclick="openPokeModal('${team}',${idx})">
          <div class="slot-empty-plus">＋</div>
          <div class="slot-empty-label">Slot ${idx+1} — Vacío</div>
        </div>
        <div style="display:flex;align-items:center;justify-content:center;padding:12px;color:#606070;font-size:.58rem">Sin pokémon</div>
      </div>`;
    return wrap;
  }

  const st=slotState(team,idx);
  const def=calcDefense(p.types);
  const weakTo=(def[4]||[]).concat(def[2]||[]);
  const resistTo=(def[0]||[]).concat(def[0.25]||[]).concat(def[0.5]||[]);
  const weakBadges=weakTo.slice(0,8).map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('');
  const resBadges=resistTo.slice(0,8).map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('');

  // Stats bars
  const maxStat=255;
  const statsBars=STAT_KEYS.map(s=>{
    const val=p[s.key]||0;
    const pct=Math.round(val/maxStat*100);
    return`<div class="mini-stat-row">
      <span class="mini-stat-label">${s.label}</span>
      <div class="mini-stat-bar-bg"><div class="mini-stat-bar ${s.cls}" style="width:${pct}%"></div></div>
      <span class="mini-stat-val" style="color:var(--c,#eaeaea)">${val}</span>
    </div>`;
  }).join('');

  // Moves seleccionados
  const movesHtml=p.moves.length>0
    ?p.moves.map(m=>{
      const d=m.detail||{};
      return`<div class="move-entry">
        <span class="move-entry-name">${formatName(m.name)}</span>
        <span class="move-entry-type ${tc(d.type)}">${tn(d.type)}</span>
        <img class="move-entry-cat" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt="">
        <span class="move-entry-pow ${powerClass(d.power)}">${d.power??'—'}</span>
        <span class="move-entry-acc">${d.accuracy!=null?d.accuracy+'%':'—'}</span>
      </div>`;
    }).join('')
    :`<div style="color:#606070;font-size:.55rem;padding:4px 0">Sin moves seleccionados</div>`;

  const imgSrc=st.shiny
    ?`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/${p.id}.png`
    :p.sprite;

  wrap.innerHTML=`
    <div class="poke-row-top">
      <!-- Slot izquierdo -->
      <div class="poke-slot-filled">
        <img class="slot-img" id="slot-img-${team}-${idx}" src="${imgSrc}" alt="${p.name}"
          onerror="this.src='${p.sprite}'">
        <div class="slot-poke-name">${formatName(p.name)}</div>
        <div class="slot-type-row">${p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
        <div class="slot-btns">
          <button class="slot-btn${st.shiny?' active':''}" onclick="toggleShiny('${team}',${idx})">✨</button>
          <button class="slot-btn${st.statsOpen?' active':''}" onclick="toggleStats('${team}',${idx})">${st.statsOpen?'SPRITE':'STATS'}</button>
        </div>
        <div class="slot-stats-wrap" id="stats-wrap-${team}-${idx}" style="display:${st.statsOpen?'block':'none'}">
          <div class="slot-stats-bars">${statsBars}</div>
        </div>
      </div>
      <!-- Moves derecha -->
      <div class="poke-moves-panel">
        <div class="moves-panel-label">MOVIMIENTOS</div>
        ${movesHtml}
        <button class="btn-edit-moves" onclick="openMovesModal('${team}',${idx})">
          ${p.moves.length>0?'✏ Editar moves':'＋ Añadir moves'}
        </button>
      </div>
    </div>
    <!-- Tipos -->
    <div class="poke-row-types">
      ${weakTo.length?`<span class="type-info-chip"><span class="chip-label">Débil a:</span><span class="badge-group">${weakBadges}</span></span>`:''}
      ${resistTo.length?`<span class="type-info-chip"><span class="chip-label">Resiste:</span><span class="badge-group">${resBadges}</span></span>`:''}
    </div>
    <!-- Botón limpiar -->
    <div class="poke-row-clear">
      <button class="btn-remove-slot" onclick="removeSlot('${team}',${idx})">✕ Eliminar</button>
    </div>`;
  return wrap;
}

function refreshSlot(team,idx){
  const old=document.getElementById(`poke-row-${team}-${idx}`);
  const newEl=buildSlotEl(team,idx);
  old.parentNode.replaceChild(newEl,old);
}

// ══════════════════════════════════════════════════════
//  ACCIONES DE SLOT
// ══════════════════════════════════════════════════════
function removeSlot(team,idx){
  teams[team][idx]=null;
  slotState(team,idx).shiny=false;
  slotState(team,idx).statsOpen=false;
  refreshSlot(team,idx);
}

function clearTeam(team){
  if(!confirm('¿Vaciar todo el equipo?'))return;
  for(let i=0;i<6;i++){teams[team][i]=null;slotState(team,i).shiny=false;slotState(team,i).statsOpen=false;}
  renderAllSlots(team);
  document.getElementById(`analysis-${team}`).style.display='none';
}

function toggleShiny(team,idx){
  const st=slotState(team,idx);
  st.shiny=!st.shiny;
  const p=teams[team][idx];if(!p)return;
  const img=document.getElementById(`slot-img-${team}-${idx}`);
  if(st.shiny){
    img.src=`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/${p.id}.png`;
    img.onerror=()=>{img.onerror=null;img.src=p.sprite;st.shiny=false;};
  }else{img.src=p.sprite;}
  // Actualizar botón sin re-render completo
  refreshSlot(team,idx);
}

function toggleStats(team,idx){
  const st=slotState(team,idx);
  st.statsOpen=!st.statsOpen;
  refreshSlot(team,idx);
}

// ══════════════════════════════════════════════════════
//  MODAL BÚSQUEDA DE POKÉMON
// ══════════════════════════════════════════════════════
function buildTypeFilterRow(){
  const row=document.getElementById('type-filter-row');
  const btns=ALL_TYPES.map(t=>
    `<button class="type-filter-btn ${tc(t)}" data-type="${t}" onclick="toggleTypeFilter('${t}')">${tn(t)}</button>`
  ).join('');
  row.innerHTML=`<span class="filter-label">Tipo:</span>${btns}`;
}

function toggleTypeFilter(type){
  const idx=_mPoke.typeFilters.indexOf(type);
  if(idx>-1){_mPoke.typeFilters.splice(idx,1);}
  else if(_mPoke.typeFilters.length<2){_mPoke.typeFilters.push(type);}
  // Actualizar visual
  document.querySelectorAll('#type-filter-row .type-filter-btn').forEach(b=>{
    b.classList.toggle('selected',_mPoke.typeFilters.includes(b.dataset.type));
  });
  applyPokeFilters();
}

function toggleFilter(flag){
  _mPoke.flags[flag]=!_mPoke.flags[flag];
  document.getElementById(`filter-${flag}`).classList.toggle('active',_mPoke.flags[flag]);
  applyPokeFilters();
}

function openPokeModal(team,idx){
  _mPoke.team=team;_mPoke.slotIdx=idx;
  _mPoke.typeFilters=[];_mPoke.flags={legendary:false,physical:false,special:false};
  // Reset filtros visuales
  document.querySelectorAll('#type-filter-row .type-filter-btn').forEach(b=>b.classList.remove('selected'));
  ['legendary','physical','special'].forEach(f=>document.getElementById(`filter-${f}`).classList.remove('active'));
  document.getElementById('modal-name-filter').value='';

  const box=document.getElementById('modal-poke-box');
  box.className=`modal-search-poke${team==='b'?' team-b':''}`;
  document.getElementById('modal-poke-title').textContent=`ELIGE EL POKÉMON — Slot ${idx+1}`;
  document.getElementById('modal-poke-overlay').classList.add('open');

  applyPokeFilters();

  document.getElementById('modal-name-filter').oninput=applyPokeFilters;
}

function applyPokeFilters(){
  const q=document.getElementById('modal-name-filter').value.toLowerCase().trim();
  const {typeFilters,flags}=_mPoke;

  _mPoke.filtered=allPokemon.filter(p=>{
    if(q&&!p.name.includes(q)&&!formatName(p.name).toLowerCase().includes(q))return false;
    if(typeFilters.length>0&&!typeFilters.every(t=>p.types.includes(t)))return false;
    if(flags.legendary&&!p.is_legendary)return false;
    if(flags.physical){
      // Pokémon que tiene más moves físicos que especiales
      const moves=p.allMoves||[];
      const phys=moves.filter(m=>m.detail?.category==='physical'&&m.detail?.power).length;
      const spec=moves.filter(m=>m.detail?.category==='special'&&m.detail?.power).length;
      if(phys<=spec)return false;
    }
    if(flags.special){
      const moves=p.allMoves||[];
      const phys=moves.filter(m=>m.detail?.category==='physical'&&m.detail?.power).length;
      const spec=moves.filter(m=>m.detail?.category==='special'&&m.detail?.power).length;
      if(spec<=phys)return false;
    }
    return true;
  });

  _mPoke.shown=BATCH;
  document.getElementById('modal-result-count').textContent=`${_mPoke.filtered.length} pokémon`;
  renderPokeGrid();
}

function renderPokeGrid(){
  const grid=document.getElementById('modal-poke-grid');
  const slice=_mPoke.filtered.slice(0,_mPoke.shown);
  const team=_mPoke.team;
  const inTeam=new Set(teams[team].filter(Boolean).map(p=>p.name));

  grid.innerHTML=slice.map(p=>{
    const already=inTeam.has(p.name);
    const legendBadge=p.is_legendary?`<div class="modal-poke-legendary">⭐ Legendario</div>`:'';
    const statsBars=STAT_KEYS.map(s=>{
      const val=p[s.key]||0;const pct=Math.round(val/255*100);
      return`<div class="mini-stat-row"><span class="mini-stat-label">${s.label}</span><div class="mini-stat-bar-bg"><div class="mini-stat-bar ${s.cls}" style="width:${pct}%"></div></div><span class="mini-stat-val">${val}</span></div>`;
    }).join('');

    return`<div class="modal-poke-card">
      <img class="modal-poke-img" src="${p.sprite}" alt="${p.name}" loading="lazy">
      <div class="modal-poke-num">N.º${p.id}</div>
      <div class="modal-poke-name">${formatName(p.name)}</div>
      <div class="modal-poke-types">${p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
      ${legendBadge}
      <div class="modal-poke-btns">
        <button class="btn-modal-stats" onclick="toggleModalStats(this)">STATS</button>
        <button class="btn-modal-add" ${already?'disabled':''} onclick="addFromModal('${p.name}')">${already?'Ya en equipo':'Añadir'}</button>
      </div>
      <div class="modal-stats-wrap"><div class="slot-stats-bars">${statsBars}</div></div>
    </div>`;
  }).join('');

  document.getElementById('modal-load-more-wrap').style.display=_mPoke.shown<_mPoke.filtered.length?'block':'none';
}

function toggleModalStats(btn){
  const wrap=btn.closest('.modal-poke-card').querySelector('.modal-stats-wrap');
  wrap.classList.toggle('open');
  btn.textContent=wrap.classList.contains('open')?'SPRITE':'STATS';
}

function loadMorePokemon(){
  _mPoke.shown+=BATCH;
  renderPokeGrid();
}

function addFromModal(name){
  const p=allPokemon.find(x=>x.name===name);if(!p)return;
  const team=_mPoke.team,idx=_mPoke.slotIdx;
  teams[team][idx]={...p,moves:[]};
  closePokeModal();
  refreshSlot(team,idx);
}

function closePokeModal(){
  document.getElementById('modal-poke-overlay').classList.remove('open');
}

// ══════════════════════════════════════════════════════
//  MODAL DE MOVES
// ══════════════════════════════════════════════════════
const TYPE_ES_EN={normal:'normal',lucha:'fighting',volador:'flying',veneno:'poison',tierra:'ground',roca:'rock',bicho:'bug',fantasma:'ghost',acero:'steel',fuego:'fire',agua:'water',planta:'grass','eléctrico':'electric',electrico:'electric','psíquico':'psychic',psiquico:'psychic',hielo:'ice','dragón':'dragon',dragon:'dragon',siniestro:'dark',hada:'fairy'};
const CAT_ES={'físico':'physical','fisico':'physical','especial':'special','estado':'status'};

function openMovesModal(team,idx){
  const p=teams[team][idx];if(!p)return;
  _mMoves.team=team;_mMoves.slotIdx=idx;
  _mMoves.selected=new Set(p.moves.map(m=>m.name));

  const box=document.getElementById('modal-moves-box');
  box.className=`modal-moves-box${team==='b'?' team-b':''}`;
  document.getElementById('modal-moves-title').textContent=formatName(p.name).toUpperCase();
  document.getElementById('modal-moves-filter-input').value='';
  document.getElementById('modal-moves-overlay').classList.add('open');
  renderMovesList(p.allMoves,'');
  document.getElementById('modal-moves-filter-input').oninput=e=>renderMovesList(p.allMoves,e.target.value.toLowerCase().trim());
}

function renderMovesList(allMoves,q){
  const nSel=_mMoves.selected.size;
  document.getElementById('modal-moves-count').textContent=nSel;
  let list=allMoves;
  if(q){
    const typeQ=TYPE_ES_EN[q]||null;
    const catQ=CAT_ES[q]||null;
    const numQ=!isNaN(parseInt(q))&&q!==''?parseInt(q):null;
    list=allMoves.filter(m=>{
      const d=m.detail||{};
      if(typeQ)return d.type===typeQ;
      if(catQ)return d.category===catQ;
      if(numQ!==null)return d.power===numQ||d.accuracy===numQ;
      return m.name.includes(q)||formatName(m.name).toLowerCase().includes(q)||tn(d.type||'').toLowerCase().includes(q);
    });
  }
  document.getElementById('modal-moves-list').innerHTML=list.map(m=>{
    const d=m.detail||{};
    const sel=_mMoves.selected.has(m.name);
    const dis=!sel&&nSel>=4;
    return`<div class="modal-move-row${sel?' selected':''}${dis?' disabled':''}" onclick="toggleMove('${m.name}',${dis})">
      <input type="checkbox" class="modal-move-chk" ${sel?'checked':''} readonly>
      <span class="modal-move-name">${formatName(m.name)}</span>
      <span class="modal-move-type ${tc(d.type)}">${tn(d.type)}</span>
      <img class="modal-move-cat" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt="">
      <span class="modal-move-pow ${powerClass(d.power)}">${d.power??'—'}</span>
      <span class="modal-move-acc">${d.accuracy!=null?d.accuracy+'%':'—'}</span>
    </div>`;
  }).join('');
}

function toggleMove(name,disabled){
  if(disabled)return;
  if(_mMoves.selected.has(name))_mMoves.selected.delete(name);
  else if(_mMoves.selected.size<4)_mMoves.selected.add(name);
  const p=teams[_mMoves.team][_mMoves.slotIdx];
  const q=document.getElementById('modal-moves-filter-input').value.toLowerCase().trim();
  renderMovesList(p.allMoves,q);
}

function confirmMoves(){
  const p=teams[_mMoves.team][_mMoves.slotIdx];if(!p)return;
  p.moves=p.allMoves.filter(m=>_mMoves.selected.has(m.name));
  closeMovesModal();
  refreshSlot(_mMoves.team,_mMoves.slotIdx);
}

function closeMovesModal(){
  document.getElementById('modal-moves-overlay').classList.remove('open');
}

// ══════════════════════════════════════════════════════
//  ANÁLISIS DE BATALLA
// ══════════════════════════════════════════════════════
function analyzeBattle(){
  const teamA=teams.a.filter(Boolean);
  const teamB=teams.b.filter(Boolean);
  if(!teamA.length&&!teamB.length){alert('Añade pokémon a al menos un equipo.');return;}

  ['a','b'].forEach(t=>{
    const myTeam=teams[t].filter(Boolean);
    const rivalTeam=teams[t==='a'?'b':'a'].filter(Boolean);
    const section=document.getElementById(`analysis-${t}`);
    if(!myTeam.length){section.style.display='none';return;}
    section.style.display='block';
    const rivalName=document.getElementById(`team-name-${t==='a'?'b':'a'}`).value;
    document.getElementById(`analysis-title-${t}`).textContent=`ANÁLISIS VS ${rivalName.toUpperCase()}`;
    document.getElementById(`analysis-content-${t}`).innerHTML=buildAnalysisHTML(t,myTeam,rivalTeam);
  });
}

function buildAnalysisHTML(side,myTeam,rivalTeam){
  const covered=new Set();
  for(const p of myTeam){
    const src=p.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status');
    const atkTypes=src.length>0?[...new Set(src.map(m=>m.detail.type))]:p.types;
    for(const at of atkTypes)for(const[dt,mult]of Object.entries(EFF[at]||{}))if(mult>=2)covered.add(dt);
  }
  const covBadges=ALL_TYPES.map(t=>
    `<span class="type-badge ${tc(t)} cov-badge${covered.has(t)?' covered':''}">${tn(t)}</span>`
  ).join('');

  // Amenazas del rival
  let threatHtml='';
  if(rivalTeam.length){
    const threats=[];
    for(const rival of rivalTeam){
      const victims=myTeam.map(me=>({me,mult:bestMult(rival,me)})).filter(x=>x.mult>=2);
      if(victims.length)threats.push({rival,victims});
    }
    threatHtml=threats.length
      ?threats.map(t=>`<div class="threat-row">
          <img class="threat-img" src="${t.rival.sprite}" alt="${t.rival.name}">
          <span class="threat-name">${formatName(t.rival.name)}</span>
          <span class="threat-victims">${t.victims.map(v=>{const{txt}=multLabel(v.mult);return`${formatName(v.me.name)} ${txt}`;}).join(', ')}</span>
        </div>`).join('')
      :`<div class="no-threats">✓ Sin amenazas claras del equipo rival</div>`;
  }else{
    threatHtml=`<div style="color:#606070;font-size:.58rem">Equipo rival vacío</div>`;
  }

  // Tabla matchups
  let tableHTML='';
  if(rivalTeam.length){
    // Cabecera: pokémon del rival
    let thead=`<thead><tr><th></th>`;
    for(const r of rivalTeam)thead+=`<th><div class="matchup-th-rival"><img src="${r.sprite}"><span>${formatName(r.name)}</span></div></th>`;
    thead+=`</tr></thead>`;

    let tbody=`<tbody>`;
    for(let i=0;i<myTeam.length;i++){
      const me=myTeam[i];
      tbody+=`<tr><th class="matchup-th-me">${formatName(me.name)}</th>`;
      for(let j=0;j<rivalTeam.length;j++){
        const mult=bestMult(me,rivalTeam[j]);
        const{txt,mc}=multLabel(mult);
        tbody+=`<td><div class="mc ${mc}" onclick="showDetail('${side}',${i},${j})">${txt}</div></td>`;
      }
      tbody+=`</tr>`;
    }
    tbody+=`</tbody>`;
    tableHTML=`<div class="matchup-wrap"><table class="matchup-table">${thead}${tbody}</table></div>`;
    // Guardar referencias para el detalle
    setTimeout(()=>{
      const section=document.getElementById(`analysis-${side}`);
      section._myTeam=myTeam;section._rivalTeam=rivalTeam;
    },0);
  }

  return`
    <div class="dashboard-grid">
      <div class="dash-card">
        <div class="dash-card-title">COBERTURA OFENSIVA</div>
        <div class="coverage-types">${covBadges}</div>
      </div>
      <div class="dash-card">
        <div class="dash-card-title">⚠ AMENAZAS DEL RIVAL</div>
        <div class="threat-list">${threatHtml}</div>
      </div>
    </div>
    ${tableHTML}
    <div class="matchup-detail" id="matchup-detail-${side}"></div>`;
}

function showDetail(side,myIdx,rivalIdx){
  const section=document.getElementById(`analysis-${side}`);
  const me=section._myTeam[myIdx];
  const rival=section._rivalTeam[rivalIdx];
  const detail=document.getElementById(`matchup-detail-${side}`);

  const buildMoveRows=(attacker,defender)=>{
    const offMoves=attacker.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status');
    if(!offMoves.length)return`<div style="color:#606070;font-size:.55rem">Sin moves ofensivos — cálculo por tipos</div>`;
    return offMoves.map(m=>{
      let mult=1;for(const dt of defender.types)mult*=(EFF[m.detail.type]?.[dt]??1);
      mult=Math.round(mult*100)/100;
      const{txt,cls}=multLabel(mult);
      return`<div class="detail-move-row">
        <span class="type-badge ${tc(m.detail.type)}">${tn(m.detail.type)}</span>
        <span class="detail-move-name">${formatName(m.name)}</span>
        <span class="detail-mult ${cls}">${txt}</span>
      </div>`;
    }).join('');
  };

  detail.className='matchup-detail open';
  detail.innerHTML=`
    <div class="detail-header">
      <img src="${me.sprite}" style="width:28px;height:28px">
      ${formatName(me.name)}
      <span class="detail-vs">VS</span>
      <img src="${rival.sprite}" style="width:28px;height:28px">
      ${formatName(rival.name)}
    </div>
    <div class="detail-cols">
      <div>
        <div class="detail-col-title">Mis moves → ${formatName(rival.name)}</div>
        <div>${buildMoveRows(me,rival)}</div>
      </div>
      <div>
        <div class="detail-col-title">Sus moves → ${formatName(me.name)}</div>
        <div>${buildMoveRows(rival,me)}</div>
      </div>
    </div>`;
}

// ══════════════════════════════════════════════════════
//  MENÚ NAV
// ══════════════════════════════════════════════════════
document.getElementById('nav-btn').addEventListener('click',e=>{
  e.stopPropagation();
  document.getElementById('nav-dropdown').classList.toggle('open');
});
document.addEventListener('click',()=>document.getElementById('nav-dropdown').classList.remove('open'));

// Cerrar modales con overlay
document.getElementById('modal-poke-overlay').addEventListener('click',e=>{
  if(e.target===document.getElementById('modal-poke-overlay'))closePokeModal();
});
document.getElementById('modal-moves-overlay').addEventListener('click',e=>{
  if(e.target===document.getElementById('modal-moves-overlay'))closeMovesModal();
});

init();
