// ══════════════════════════════════════════════════════
//  teams.js — Batalla por equipos v2
// ══════════════════════════════════════════════════════

const TIPOS_ES={normal:'Normal',fighting:'Lucha',flying:'Volador',poison:'Veneno',ground:'Tierra',rock:'Roca',bug:'Bicho',ghost:'Fantasma',steel:'Acero',fire:'Fuego',water:'Agua',grass:'Planta',electric:'Eléctrico',psychic:'Psíquico',ice:'Hielo',dragon:'Dragón',dark:'Siniestro',fairy:'Hada'};
const TYPE_CLASS={normal:'t-normal',fighting:'t-fighting',flying:'t-flying',poison:'t-poison',ground:'t-ground',rock:'t-rock',bug:'t-bug',ghost:'t-ghost',steel:'t-steel',fire:'t-fire',water:'t-water',grass:'t-grass',electric:'t-electric',psychic:'t-psychic',ice:'t-ice',dragon:'t-dragon',dark:'t-dark',fairy:'t-fairy'};
const CAT_IMG={physical:'img/cat_physical.png',special:'img/cat_special.png',status:'img/cat_status.png'};
const STAT_KEYS=[{key:'hp',label:'PS',cls:'sb-hp'},{key:'attack',label:'ATQ',cls:'sb-atk'},{key:'defense',label:'DEF',cls:'sb-def'},{key:'sp_attack',label:'ATQE',cls:'sb-spa'},{key:'sp_defense',label:'DEFE',cls:'sb-spd'},{key:'speed',label:'VEL',cls:'sb-spe'}];
const ALL_TYPES=Object.keys(TIPOS_ES);
const TYPE_ES_EN={normal:'normal',lucha:'fighting',volador:'flying',veneno:'poison',tierra:'ground',roca:'rock',bicho:'bug',fantasma:'ghost',acero:'steel',fuego:'fire',agua:'water',planta:'grass','eléctrico':'electric',electrico:'electric','psíquico':'psychic',psiquico:'psychic',hielo:'ice','dragón':'dragon',dragon:'dragon',siniestro:'dark',hada:'fairy'};
const CAT_ES={'físico':'physical','fisico':'physical','especial':'special','estado':'status'};

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
function powerClass(p){if(!p)return'pow-none';if(p>=100)return'pow-high';if(p>=60)return'pow-mid';return'pow-low';}

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

function bestMult(attacker,defender){
  const off=attacker.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status');
  const src=off.length>0?off.map(m=>m.detail.type):attacker.types;
  let best=0;
  for(const at of src){let m=1;for(const dt of defender.types)m*=(EFF[at]?.[dt]??1);m=Math.round(m*100)/100;if(m>best)best=m;}
  return best;
}

// ── Estado global ──
let DB=null, allPokemon=[];
const teams={a:Array(6).fill(null),b:Array(6).fill(null)};
const _slotState={};
function slotSt(team,idx){const k=`${team}-${idx}`;if(!_slotState[k])_slotState[k]={shiny:false,stats:false};return _slotState[k];}

// Modal pokémon
const _mP={team:null,typeFilters:[],flags:{legendary:false,physical:false,special:false},filtered:[],shown:0};
const BATCH=50;

// Modal moves
const _mM={team:null,idx:null,selected:new Set(),sort:'default',allMoves:[]};

// ══════════════════════════════
//  INIT
// ══════════════════════════════
async function init(){
  renderAllSlots('a'); renderAllSlots('b');
  buildTypeFilterRow();
  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      DB=await res.json();
      allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({
        name,id:p.id,types:p.types,sprite:p.sprite,
        is_legendary:!!p.is_legendary,
        hp:p.hp||0,attack:p.attack||0,defense:p.defense||0,
        sp_attack:p.sp_attack||0,sp_defense:p.sp_defense||0,speed:p.speed||0,
        allMoves:(p.moves||[]).map(m=>({name:m.name,byLevel:m.byLevel,level:m.level,
          detail:m.detail||(DB.moves&&DB.moves[m.name])||{type:'normal',category:'status',power:null,accuracy:null,pp:null}}))
      })).sort((a,b)=>a.id-b.id);
      document.getElementById('status-bar').innerHTML=
        `<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"><span>${allPokemon.length} Pokémon disponibles</span>`;
    }
  }catch(e){document.getElementById('status-bar').textContent='Sin DB local.';}
}

// ══════════════════════════════
//  RENDER SLOTS
// ══════════════════════════════
function renderAllSlots(team){
  const c=document.getElementById(`slots-${team}`);
  c.innerHTML='';
  for(let i=0;i<6;i++)c.appendChild(buildSlotEl(team,i));
}

function refreshSlot(team,idx){
  const old=document.getElementById(`poke-row-${team}-${idx}`);
  if(old)old.parentNode.replaceChild(buildSlotEl(team,idx),old);
}

function buildSlotEl(team,idx){
  const wrap=document.createElement('div');
  wrap.className='poke-row'; wrap.id=`poke-row-${team}-${idx}`;
  const p=teams[team][idx];
  if(!p){
    // Slot vacío
    const emptyLeft=`<div class="poke-slot-empty" onclick="openPokeModal('${team}')">
      <div class="slot-empty-plus">＋</div>
      <div class="slot-empty-label">Slot ${idx+1} — Vacío</div>
    </div>`;
    const emptyRight=`<div style="display:flex;align-items:center;justify-content:center;padding:16px;">
      <span style="color:#9090a8;font-size:.7rem">Sin pokémon</span>
    </div>`;
    wrap.innerHTML=`<div class="poke-row-top">${team==='a'?emptyLeft+emptyRight:emptyRight+emptyLeft}</div>`;
    return wrap;
  }

  const st=slotSt(team,idx);
  const def=calcDefense(p.types);
  const weakTo=(def[4]||[]).concat(def[2]||[]);
  const resistTo=(def[0]||[]).concat(def[0.25]||[]).concat(def[0.5]||[]);

  // Radar + barras stats
  const radarId=`radar-${team}-${idx}`;
  const statsBars=STAT_KEYS.map(s=>{
    const v=p[s.key]||0,pct=Math.round(v/255*100);
    return`<div class="mini-stat-row">
      <span class="mini-stat-label">${s.label}</span>
      <div class="mini-stat-bar-bg"><div class="mini-stat-bar ${s.cls}" style="width:${pct}%"></div></div>
      <span class="mini-stat-val">${v}</span>
    </div>`;
  }).join('');

  const imgSrc=st.shiny
    ?`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/${p.id}.png`
    :p.sprite;

  // Moves
  const movesHtml=p.moves.length>0
    ?p.moves.map(m=>{const d=m.detail||{};return`<div class="move-entry">
      <span class="move-entry-name">${formatName(m.name)}</span>
      <span class="move-entry-type ${tc(d.type)}">${tn(d.type)}</span>
      <img class="move-entry-cat" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt="">
      <span class="move-entry-pow ${powerClass(d.power)}">${d.power??'—'}</span>
      <span class="move-entry-acc">${d.accuracy!=null?d.accuracy+'%':'—'}</span>
    </div>`;}).join('')
    :`<div class="no-moves-label">Sin moves seleccionados</div>`;

  const slotContent=`
    <div class="poke-slot-filled">
      <img class="slot-img" id="slot-img-${team}-${idx}" src="${imgSrc}" alt="${p.name}"
        style="${st.stats?'display:none':''}" onerror="this.src='${p.sprite}'">
      <div class="slot-stats-wrap${st.stats?' open':''}" id="stats-wrap-${team}-${idx}">
        <canvas class="radar-canvas" id="${radarId}" width="160" height="130"></canvas>
        <div class="slot-stats-bars">${statsBars}</div>
      </div>
      <div class="slot-poke-name">${formatName(p.name)}</div>
      <div class="slot-type-row">${p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
      <div class="slot-btns">
        <button class="slot-btn${st.shiny?' active':''}" onclick="toggleShiny('${team}',${idx})">✨</button>
        <button class="slot-btn${st.stats?' active':''}" onclick="toggleStats('${team}',${idx})">${st.stats?'SPRITE':'STATS'}</button>
      </div>
    </div>`;

  const movesPanel=`
    <div class="poke-moves-panel">
      <div class="moves-panel-label">MOVIMIENTOS</div>
      ${movesHtml}
      <button class="btn-edit-moves" onclick="openMovesModal('${team}',${idx})">
        ${p.moves.length>0?'✏ Editar moves':'＋ Añadir moves'}
      </button>
    </div>`;

  wrap.innerHTML=`
    <div class="poke-row-top">${team==='a'?slotContent+movesPanel:movesPanel+slotContent}</div>
    <div class="poke-row-types">
      ${weakTo.length?`<span class="type-info-chip"><span class="chip-label">Débil a:</span><span class="badge-group">${weakTo.slice(0,8).map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</span></span>`:''}
      ${resistTo.length?`<span class="type-info-chip"><span class="chip-label">Resiste:</span><span class="badge-group">${resistTo.slice(0,8).map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</span></span>`:''}
    </div>
    <div class="poke-row-clear"><button class="btn-remove-slot" onclick="removeSlot('${team}',${idx})">✕ Eliminar</button></div>`;

  // Dibujar radar tras insertar en DOM
  if(st.stats) setTimeout(()=>drawRadar(radarId,p,team),50);
  return wrap;
}

// ── Radar hexagonal ──
function drawRadar(canvasId,p,team){
  const canvas=document.getElementById(canvasId);if(!canvas)return;
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height,cx=W/2,cy=H/2,r=Math.min(W,H)/2-16;
  const vals=STAT_KEYS.map(s=>p[s.key]||0);
  const maxV=255;
  const colors={a:'#4a9eff',b:'#ffaa33'};
  const col=colors[team]||'#4a9eff';
  ctx.clearRect(0,0,W,H);
  const angle=i=>Math.PI/2+i*(2*Math.PI/6);
  // Grid
  for(let ring=1;ring<=4;ring++){
    ctx.beginPath();
    for(let i=0;i<6;i++){const a=angle(i),rr=r*ring/4;ctx.lineTo(cx+rr*Math.cos(a),cy-rr*Math.sin(a));}
    ctx.closePath();ctx.strokeStyle='rgba(255,255,255,.1)';ctx.lineWidth=1;ctx.stroke();
  }
  // Axes
  for(let i=0;i<6;i++){const a=angle(i);ctx.beginPath();ctx.moveTo(cx,cy);ctx.lineTo(cx+r*Math.cos(a),cy-r*Math.sin(a));ctx.strokeStyle='rgba(255,255,255,.15)';ctx.stroke();}
  // Data
  ctx.beginPath();
  for(let i=0;i<6;i++){const a=angle(i),rr=r*(vals[i]/maxV);ctx.lineTo(cx+rr*Math.cos(a),cy-rr*Math.sin(a));}
  ctx.closePath();ctx.fillStyle=col.replace(')',',0.25)').replace('rgb','rgba');ctx.fill();
  ctx.strokeStyle=col;ctx.lineWidth=2;ctx.stroke();
  // Labels
  ctx.fillStyle='#b0b0c0';ctx.font='bold 8px Nunito';ctx.textAlign='center';ctx.textBaseline='middle';
  for(let i=0;i<6;i++){const a=angle(i),lr=r+12;ctx.fillText(STAT_KEYS[i].label,cx+lr*Math.cos(a),cy-lr*Math.sin(a));}
}

// ── Acciones slot ──
function removeSlot(team,idx){teams[team][idx]=null;slotSt(team,idx).shiny=false;slotSt(team,idx).stats=false;refreshSlot(team,idx);}
function clearTeam(team){if(!confirm('¿Vaciar el equipo?'))return;for(let i=0;i<6;i++){teams[team][i]=null;_slotState[`${team}-${i}`]={shiny:false,stats:false};}renderAllSlots(team);}

function toggleShiny(team,idx){
  const st=slotSt(team,idx);st.shiny=!st.shiny;
  const p=teams[team][idx];if(!p)return;
  const img=document.getElementById(`slot-img-${team}-${idx}`);
  if(img){
    if(st.shiny){img.src=`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/${p.id}.png`;img.onerror=()=>{img.onerror=null;img.src=p.sprite;st.shiny=false;};}
    else img.src=p.sprite;
  }
  // Solo actualizar botones sin re-render completo
  refreshSlot(team,idx);
}

function toggleStats(team,idx){
  const st=slotSt(team,idx);st.stats=!st.stats;
  refreshSlot(team,idx);
}

// ══════════════════════════════
//  MODAL BÚSQUEDA POKÉMON
// ══════════════════════════════
function buildTypeFilterRow(){
  const row=document.getElementById('type-filter-row');
  row.innerHTML=`<span class="filter-label">Tipo:</span>`+
    ALL_TYPES.map(t=>`<button class="type-filter-btn ${tc(t)}" data-type="${t}" onclick="toggleTypeFilter('${t}')">${tn(t)}</button>`).join('');
}

function toggleTypeFilter(type){
  const idx=_mP.typeFilters.indexOf(type);
  if(idx>-1)_mP.typeFilters.splice(idx,1);
  else if(_mP.typeFilters.length<2)_mP.typeFilters.push(type);
  document.querySelectorAll('#type-filter-row .type-filter-btn').forEach(b=>b.classList.toggle('selected',_mP.typeFilters.includes(b.dataset.type)));
  applyPokeFilters();
}

function toggleFilter(flag){
  _mP.flags[flag]=!_mP.flags[flag];
  document.getElementById(`filter-${flag}`).classList.toggle('active',_mP.flags[flag]);
  applyPokeFilters();
}

function openPokeModal(team){
  _mP.team=team;_mP.typeFilters=[];_mP.flags={legendary:false,physical:false,special:false};
  document.querySelectorAll('#type-filter-row .type-filter-btn').forEach(b=>b.classList.remove('selected'));
  ['legendary','physical','special'].forEach(f=>document.getElementById(`filter-${f}`).classList.remove('active'));
  document.getElementById('modal-name-filter').value='';
  const box=document.getElementById('modal-poke-box');
  box.className=`modal-poke-box${team==='b'?' team-b':''}`;
  const tname=document.getElementById(`team-name-${team}`).value;
  document.getElementById('modal-poke-title').textContent=`ELIGE UN POKÉMON PARA EL ${tname.toUpperCase()}`;
  document.getElementById('modal-poke-overlay').classList.add('open');
  document.getElementById('modal-name-filter').oninput=applyPokeFilters;
  applyPokeFilters();
}

function applyPokeFilters(){
  const q=document.getElementById('modal-name-filter').value.toLowerCase().trim();
  _mP.filtered=allPokemon.filter(p=>{
    if(q&&!p.name.includes(q)&&!formatName(p.name).toLowerCase().includes(q))return false;
    if(_mP.typeFilters.length>0&&!_mP.typeFilters.every(t=>p.types.includes(t)))return false;
    if(_mP.flags.legendary&&!p.is_legendary)return false;
    if(_mP.flags.physical){const mv=p.allMoves||[];const ph=mv.filter(m=>m.detail?.category==='physical'&&m.detail?.power).length;const sp=mv.filter(m=>m.detail?.category==='special'&&m.detail?.power).length;if(ph<=sp)return false;}
    if(_mP.flags.special){const mv=p.allMoves||[];const ph=mv.filter(m=>m.detail?.category==='physical'&&m.detail?.power).length;const sp=mv.filter(m=>m.detail?.category==='special'&&m.detail?.power).length;if(sp<=ph)return false;}
    return true;
  });
  _mP.shown=BATCH;
  document.getElementById('modal-result-count').textContent=`${_mP.filtered.length} pokémon`;
  renderPokeGrid();
}

function renderPokeGrid(){
  const grid=document.getElementById('modal-poke-grid');
  const team=_mP.team;
  // Nombres ya en el equipo (para marcar como chosen)
  const inTeam=new Set(teams[team].filter(Boolean).map(p=>p.name));
  const slice=_mP.filtered.slice(0,_mP.shown);
  grid.innerHTML=slice.map(p=>{
    const chosen=inTeam.has(p.name);
    const statsBars=STAT_KEYS.map(s=>{const v=p[s.key]||0,pct=Math.round(v/255*100);
      return`<div class="mini-stat-row"><span class="mini-stat-label">${s.label}</span><div class="mini-stat-bar-bg"><div class="mini-stat-bar ${s.cls}" style="width:${pct}%"></div></div><span class="mini-stat-val">${v}</span></div>`;
    }).join('');
    return`<div class="modal-poke-card${chosen?' chosen':''}" onclick="addFromModal('${p.name}')">
      <img class="modal-poke-img" src="${p.sprite}" alt="${p.name}" loading="lazy">
      <div class="modal-poke-num">N.º${p.id}</div>
      <div class="modal-poke-name">${formatName(p.name)}</div>
      <div class="modal-poke-types">${p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
      ${p.is_legendary?'<div class="modal-poke-legendary">⭐ Legendario</div>':''}
      <button class="btn-modal-stats" onclick="event.stopPropagation();toggleModalStats(this)">STATS</button>
      <div class="modal-stats-wrap"><div class="slot-stats-bars">${statsBars}</div></div>
    </div>`;
  }).join('');
  document.getElementById('modal-load-more-wrap').style.display=_mP.shown<_mP.filtered.length?'block':'none';
}

function toggleModalStats(btn){
  const w=btn.nextElementSibling;w.classList.toggle('open');
  btn.textContent=w.classList.contains('open')?'SPRITE':'STATS';
}

function loadMorePokemon(){_mP.shown+=BATCH;renderPokeGrid();}

function addFromModal(name){
  const team=_mP.team;
  const p=allPokemon.find(x=>x.name===name);if(!p)return;
  // Buscar primer slot vacío
  const idx=teams[team].findIndex(s=>s===null);
  if(idx===-1){alert('El equipo ya está lleno (6 pokémon).');return;}
  teams[team][idx]={...p,moves:[]};
  refreshSlot(team,idx);
  // Marcar como chosen en el grid (sin re-render completo)
  const cards=document.querySelectorAll(`#modal-poke-grid .modal-poke-card`);
  cards.forEach(c=>{
    if(c.querySelector('.modal-poke-name')?.textContent===formatName(name))c.classList.add('chosen');
  });
  // No cerrar el modal
}

function closePokeModal(){document.getElementById('modal-poke-overlay').classList.remove('open');}

// ══════════════════════════════
//  MODAL MOVES
// ══════════════════════════════
function openMovesModal(team,idx){
  const p=teams[team][idx];if(!p)return;
  _mM.team=team;_mM.idx=idx;_mM.selected=new Set(p.moves.map(m=>m.name));
  _mM.sort='default';_mM.allMoves=p.allMoves;
  const box=document.getElementById('modal-moves-box');
  box.className=`modal-moves-box${team==='b'?' team-b':''}`;
  document.getElementById('modal-moves-title').textContent=formatName(p.name).toUpperCase();
  document.getElementById('modal-moves-filter-input').value='';
  document.getElementById('modal-moves-overlay').classList.add('open');
  renderMovesTable();
  document.getElementById('modal-moves-filter-input').oninput=renderMovesTable;
  // Sort click handlers
  document.querySelectorAll('#modal-moves-table thead th[data-sort]').forEach(th=>{
    th.onclick=()=>handleMoveSort(th.dataset.sort,th);
  });
}

function handleMoveSort(key,th){
  const asc=`${key}-asc`,desc=`${key}-desc`;
  if(_mM.sort===asc)_mM.sort=desc;
  else _mM.sort=asc;
  document.querySelectorAll('#modal-moves-table thead th .sort-arrow-m').forEach(a=>a.textContent='↕');
  th.querySelector('.sort-arrow-m').textContent=_mM.sort.endsWith('-asc')?'↑':'↓';
  renderMovesTable();
}

function renderMovesTable(){
  const q=document.getElementById('modal-moves-filter-input').value.toLowerCase().trim();
  const nSel=_mM.selected.size;
  document.getElementById('modal-moves-count').textContent=nSel;
  const typeQ=TYPE_ES_EN[q]||null;
  const catQ=CAT_ES[q]||null;
  const numQ=q&&!isNaN(parseInt(q))?parseInt(q):null;

  let list=_mM.allMoves.filter(m=>{
    if(!q)return true;
    const d=m.detail||{};
    if(typeQ)return d.type===typeQ;
    if(catQ)return d.category===catQ;
    if(numQ!==null)return d.power===numQ||d.accuracy===numQ;
    return m.name.includes(q)||formatName(m.name).toLowerCase().includes(q)||tn(d.type||'').toLowerCase().includes(q);
  });

  // Sort
  const s=_mM.sort;
  if(s==='name-asc')list=[...list].sort((a,b)=>a.name.localeCompare(b.name));
  else if(s==='name-desc')list=[...list].sort((a,b)=>b.name.localeCompare(a.name));
  else if(s==='type-asc')list=[...list].sort((a,b)=>(a.detail?.type||'').localeCompare(b.detail?.type||''));
  else if(s==='type-desc')list=[...list].sort((a,b)=>(b.detail?.type||'').localeCompare(a.detail?.type||''));
  else if(s==='cat-asc'){const o={physical:0,special:1,status:2};list=[...list].sort((a,b)=>o[a.detail?.category||'status']-o[b.detail?.category||'status']);}
  else if(s==='cat-desc'){const o={physical:0,special:1,status:2};list=[...list].sort((a,b)=>o[b.detail?.category||'status']-o[a.detail?.category||'status']);}
  else if(s==='pow-asc')list=[...list].sort((a,b)=>(a.detail?.power||0)-(b.detail?.power||0));
  else if(s==='pow-desc')list=[...list].sort((a,b)=>(b.detail?.power||0)-(a.detail?.power||0));
  else if(s==='acc-asc')list=[...list].sort((a,b)=>(a.detail?.accuracy||0)-(b.detail?.accuracy||0));
  else if(s==='acc-desc')list=[...list].sort((a,b)=>(b.detail?.accuracy||0)-(a.detail?.accuracy||0));

  document.getElementById('modal-moves-tbody').innerHTML=list.map(m=>{
    const d=m.detail||{};
    const sel=_mM.selected.has(m.name);
    const dis=!sel&&nSel>=4;
    return`<tr class="modal-move-row${sel?' selected':''}${dis?' disabled':''}" onclick="toggleMove('${m.name}',${dis})">
      <td class="mm-chk"><input type="checkbox" class="modal-move-chk" ${sel?'checked':''} readonly onclick="event.stopPropagation()"></td>
      <td class="mm-name">${formatName(m.name)}</td>
      <td><span class="mm-type-badge ${tc(d.type)}">${tn(d.type)}</span></td>
      <td><img class="mm-cat-img" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt=""></td>
      <td class="mm-pow ${powerClass(d.power)}">${d.power??'—'}</td>
      <td class="mm-acc">${d.accuracy!=null?d.accuracy+'%':'—'}</td>
    </tr>`;
  }).join('');
}

function toggleMove(name,disabled){
  if(disabled)return;
  if(_mM.selected.has(name))_mM.selected.delete(name);else if(_mM.selected.size<4)_mM.selected.add(name);
  renderMovesTable();
}

function confirmMoves(){
  const p=teams[_mM.team][_mM.idx];if(!p)return;
  p.moves=_mM.allMoves.filter(m=>_mM.selected.has(m.name));
  closeMovesModal();refreshSlot(_mM.team,_mM.idx);
}

function closeMovesModal(){document.getElementById('modal-moves-overlay').classList.remove('open');}

// ══════════════════════════════
//  ANÁLISIS
// ══════════════════════════════
function analyzeBattle(){
  const tA=teams.a.filter(Boolean),tB=teams.b.filter(Boolean);
  if(!tA.length&&!tB.length){alert('Añade pokémon a al menos un equipo.');return;}
  const nameA=document.getElementById('team-name-a').value;
  const nameB=document.getElementById('team-name-b').value;
  document.getElementById('modal-analysis-title').textContent=`⚡ ${nameA.toUpperCase()} VS ${nameB.toUpperCase()}`;
  document.getElementById('modal-analysis-body').innerHTML=
    buildAnalysisSection('a',tA,tB,nameA,nameB)+
    buildAnalysisSection('b',tB,tA,nameB,nameA);
  document.getElementById('modal-analysis-overlay').classList.add('open');
}

function buildAnalysisSection(side,myTeam,rivalTeam,myName,rivalName){
  if(!myTeam.length)return`<div style="color:#9090a8;font-size:.7rem;padding:12px">${myName} está vacío.</div>`;

  // Cobertura ofensiva
  const covered=new Set();
  for(const p of myTeam){
    const off=p.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status');
    const src=off.length>0?[...new Set(off.map(m=>m.detail.type))]:p.types;
    for(const at of src)for(const[dt,m]of Object.entries(EFF[at]||{}))if(m>=2)covered.add(dt);
  }
  const covBadges=ALL_TYPES.map(t=>`<span class="type-badge ${tc(t)} cov-badge${covered.has(t)?' covered':''}">${tn(t)}</span>`).join('');

  // Amenazas
  let threatHtml='';
  if(rivalTeam.length){
    const threats=rivalTeam.map(rival=>{
      const victims=myTeam.map(me=>({me,mult:bestMult(rival,me)})).filter(x=>x.mult>=2);
      return{rival,victims};
    }).filter(t=>t.victims.length>0);
    threatHtml=threats.length
      ?threats.map(t=>`<div class="threat-row">
          <img class="threat-img" src="${t.rival.sprite}">
          <span class="threat-name">${formatName(t.rival.name)}</span>
          <span class="threat-victims">${t.victims.map(v=>{const{txt}=multLabel(v.mult);return`${formatName(v.me.name)} ${txt}`;}).join(', ')}</span>
        </div>`).join('')
      :`<div class="no-threats">✓ Sin amenazas claras</div>`;
  }else threatHtml=`<div style="color:#9090a8;font-size:.6rem">Rival vacío</div>`;

  // Tabla matchups
  let tableHTML='';
  if(rivalTeam.length){
    let thead=`<thead><tr><th></th>`;
    for(const r of rivalTeam)thead+=`<th><div class="matchup-th-rival"><img src="${r.sprite}"><span>${formatName(r.name)}</span></div></th>`;
    thead+=`</tr></thead>`;
    let tbody=`<tbody>`;
    for(let i=0;i<myTeam.length;i++){
      const me=myTeam[i];
      tbody+=`<tr><th class="matchup-th-me"><div style="display:flex;align-items:center;gap:4px"><img src="${me.sprite}" style="width:26px;height:26px"> ${formatName(me.name)}</div></th>`;
      for(let j=0;j<rivalTeam.length;j++){
        const mult=bestMult(me,rivalTeam[j]);
        const{txt,mc}=multLabel(mult);
        tbody+=`<td><div class="mc ${mc}" onclick="showDetail('${side}',${i},${j})">${txt}</div></td>`;
      }
      tbody+=`</tr>`;
    }
    tbody+=`</tbody>`;
    tableHTML=`<div class="matchup-wrap"><table class="matchup-table">${thead}${tbody}</table></div>`;
  }

  // Detalle (inicialmente oculto)
  const detailId=`matchup-detail-${side}`;

  // Pokémon recomendados vs el rival
  const recsHTML=buildRecs(myTeam,rivalTeam,side);

  return`<div class="analysis-team-section analysis-team-${side}" id="analysis-section-${side}"
    data-my='${JSON.stringify(myTeam.map(p=>p.name))}' data-rival='${JSON.stringify(rivalTeam.map(p=>p.name))}'>
    <div class="analysis-team-title">📊 ${myName.toUpperCase()} VS ${rivalName.toUpperCase()}</div>
    <div class="dash-grid">
      <div class="dash-card"><div class="dash-card-title">COBERTURA OFENSIVA</div><div class="coverage-types">${covBadges}</div></div>
      <div class="dash-card"><div class="dash-card-title">⚠ AMENAZAS DEL RIVAL</div><div class="threat-list">${threatHtml}</div></div>
    </div>
    ${tableHTML}
    <div class="matchup-detail" id="${detailId}"></div>
    ${recsHTML}
    <hr style="border-color:#1a1a2e;margin:18px 0">
  </div>`;
}

function buildRecs(myTeam,rivalTeam,side){
  if(!rivalTeam.length)return'';
  // Tipos del rival combinados — buscar pokémon fuertes contra ellos
  const rivalTypes=[...new Set(rivalTeam.flatMap(p=>p.types))];
  // Tipos que son fuertes contra los tipos del rival
  const goodTypes=[];
  for(const at of ALL_TYPES){
    let totalMult=0;
    for(const rt of rivalTypes) totalMult+=(EFF[at]?.[rt]??1);
    if(totalMult/rivalTypes.length>1)goodTypes.push({type:at,score:totalMult});
  }
  goodTypes.sort((a,b)=>b.score-a.score);
  const topTypes=goodTypes.slice(0,4).map(x=>x.type);

  // Buscar pokémon de esos tipos (de la DB, excluyendo los ya en ambos equipos)
  const inUse=new Set([...teams.a,...teams.b].filter(Boolean).map(p=>p.name));
  const recs=[];
  if(allPokemon.length>0){
    for(const t of topTypes){
      for(const p of allPokemon){
        if(recs.length>=8)break;
        if(inUse.has(p.name))continue;
        if(!p.types.includes(t))continue;
        if(recs.some(r=>r.name===p.name))continue;
        recs.push(p);
      }
      if(recs.length>=8)break;
    }
  }
  if(!recs.length)return'';

  const recsHTML=recs.map(p=>{
    const def=calcDefense(p.types);
    const w4=def[4]||[],w2=def[2]||[];
    const weakBadges=[...w4.slice(0,2).map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×4</span>`),
      ...w2.slice(0,3-w4.length).map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×2</span>`)].join('');
    return`<div class="rec-row">
      <img class="rec-row-img" src="${p.sprite}" alt="${p.name}">
      <div class="rec-row-info">
        <div class="rec-row-name">${formatName(p.name)}</div>
        <div class="rec-row-types">${p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
        ${weakBadges?`<div class="rec-why-row"><span class="rec-why-label">Débil a:</span>${weakBadges}</div>`:''}
      </div>
    </div>`;
  }).join('');

  return`<div class="recs-section">
    <div class="recs-title">POKÉMON RECOMENDADOS CONTRA EL RIVAL</div>
    <div class="recs-grid">${recsHTML}</div>
  </div>`;
}

// Detalle al hacer click en celda de la tabla
function showDetail(side,myIdx,rivalIdx){
  const section=document.getElementById(`analysis-section-${side}`);
  const myNames=JSON.parse(section.dataset.my);
  const rivalNames=JSON.parse(section.dataset.rival);
  const me=allPokemon.find(p=>p.name===myNames[myIdx])||(teams[side==='a'?'a':'b'].filter(Boolean)[myIdx]);
  const rival=allPokemon.find(p=>p.name===rivalNames[rivalIdx])||(teams[side==='a'?'b':'a'].filter(Boolean)[rivalIdx]);
  if(!me||!rival)return;
  // Buscar moves del equipo actual
  const meFull=teams[side].filter(Boolean)[myIdx]||me;
  const rivalFull=teams[side==='a'?'b':'a'].filter(Boolean)[rivalIdx]||rival;

  const buildRows=(atk,def)=>{
    const off=(atk.moves||[]).filter(m=>m.detail?.power&&m.detail?.category!=='status');
    if(!off.length)return`<div style="color:#9090a8;font-size:.58rem">Sin moves ofensivos</div>`;
    return off.map(m=>{let mult=1;for(const dt of def.types)mult*=(EFF[m.detail.type]?.[dt]??1);mult=Math.round(mult*100)/100;
      const{txt,cls}=multLabel(mult);
      return`<div class="detail-move-row"><span class="type-badge ${tc(m.detail.type)}">${tn(m.detail.type)}</span><span class="detail-move-name">${formatName(m.name)}</span><span class="detail-mult ${cls}">${txt}</span></div>`;
    }).join('');
  };

  const detail=document.getElementById(`matchup-detail-${side}`);
  detail.className='matchup-detail open';
  detail.innerHTML=`
    <div class="detail-header">
      <img src="${meFull.sprite}" style="width:30px;height:30px">
      ${formatName(meFull.name)}
      <span class="detail-vs-label">VS</span>
      <img src="${rivalFull.sprite}" style="width:30px;height:30px">
      ${formatName(rivalFull.name)}
    </div>
    <div class="detail-cols">
      <div><div class="detail-col-title">Mis moves → ${formatName(rivalFull.name)}</div>${buildRows(meFull,rivalFull)}</div>
      <div><div class="detail-col-title">Sus moves → ${formatName(meFull.name)}</div>${buildRows(rivalFull,meFull)}</div>
    </div>`;
}

function closeAnalysisModal(){document.getElementById('modal-analysis-overlay').classList.remove('open');}

// ══════════════════════════════
//  MENÚ NAV
// ══════════════════════════════
document.getElementById('nav-btn').addEventListener('click',e=>{e.stopPropagation();document.getElementById('nav-dropdown').classList.toggle('open');});
document.addEventListener('click',()=>document.getElementById('nav-dropdown').classList.remove('open'));
document.getElementById('modal-poke-overlay').addEventListener('click',e=>{if(e.target===document.getElementById('modal-poke-overlay'))closePokeModal();});
document.getElementById('modal-moves-overlay').addEventListener('click',e=>{if(e.target===document.getElementById('modal-moves-overlay'))closeMovesModal();});
document.getElementById('modal-analysis-overlay').addEventListener('click',e=>{if(e.target===document.getElementById('modal-analysis-overlay'))closeAnalysisModal();});

init();
