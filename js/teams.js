// teams.js — Battle Teams

// ══════════════════════════════════════
// DATOS BASE (copiados de app.js)
// ══════════════════════════════════════
const TIPOS_ES={normal:'Normal',fighting:'Lucha',flying:'Volador',poison:'Veneno',ground:'Tierra',rock:'Roca',bug:'Bicho',ghost:'Fantasma',steel:'Acero',fire:'Fuego',water:'Agua',grass:'Planta',electric:'Eléctrico',psychic:'Psíquico',ice:'Hielo',dragon:'Dragón',dark:'Siniestro',fairy:'Hada'};
const TYPE_CLASS={normal:'t-normal',fighting:'t-fighting',flying:'t-flying',poison:'t-poison',ground:'t-ground',rock:'t-rock',bug:'t-bug',ghost:'t-ghost',steel:'t-steel',fire:'t-fire',water:'t-water',grass:'t-grass',electric:'t-electric',psychic:'t-psychic',ice:'t-ice',dragon:'t-dragon',dark:'t-dark',fairy:'t-fairy'};
const CAT_IMG={physical:'img/cat_physical.png',special:'img/cat_special.png',status:'img/cat_status.png'};

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

function calcDefense(types){const r={4:[],2:[],1:[],0.5:[],0.25:[],0:[]};for(const a of Object.keys(EFF)){let m=1;for(const d of types)m*=(EFF[a][d]??1);const k=Math.round(m*100)/100;if(r[k]!==undefined)r[k].push(a);else if(k>=3)r[4].push(a);else r[1].push(a);}return r;}
function multLabel(m){if(m>=4)return{txt:'×4',cls:'rm-4'};if(m>=2)return{txt:'×2',cls:'rm-2'};if(m>=1)return{txt:'×1',cls:'rm-1'};if(m>=0.5)return{txt:'×½',cls:'rm-05'};if(m>0)return{txt:'×¼',cls:'rm-025'};return{txt:'×0',cls:'rm-0'};}

const STAT_KEYS=[
  {key:'hp',label:'PS',cls:'sb-hp'},
  {key:'attack',label:'ATQ',cls:'sb-atk'},
  {key:'defense',label:'DEF',cls:'sb-def'},
  {key:'sp_attack',label:'ATQE',cls:'sb-spa'},
  {key:'sp_defense',label:'DEFE',cls:'sb-spd'},
  {key:'speed',label:'VEL',cls:'sb-spe'},
];
const STAT_MAX=255;
const RADAR_COLORS={a:{fill:'rgba(74,158,255,0.20)',stroke:'#4a9eff'},b:{fill:'rgba(255,170,51,0.20)',stroke:'#ffaa33'}};

// ══════════════════════════════════════
// ESTADO
// ══════════════════════════════════════
let DB=null;
let allPokemon=[];

// teams[team][slot] = {name, shiny, selectedMoves:[]} | null
const teams={a:Array(6).fill(null),b:Array(6).fill(null)};

// Modal
let activeSlot={team:null,slot:null};
let activeMovesSlot={team:null,slot:null};
let modalFiltered=[];
let modalPage=0;
const MODAL_PAGE_SIZE=50;
let modalTypeFilter=[];     // hasta 2 tipos
let modalLegendFilter='all';
let modalStyleFilter='all';
let modalSearchQ='';

// ══════════════════════════════════════
// CARGA POKÉDEX
// ══════════════════════════════════════
async function loadPokedex(){
  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      DB=await res.json();
      allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({name,id:p.id})).sort((a,b)=>a.id-b.id);
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon disponibles</span>`;
    }
  }catch(e){
    document.getElementById('status-bar').textContent='Error cargando Pokédex';
  }
  initSlots();
  buildTypeFilterGrid();
}

// ══════════════════════════════════════
// SLOTS
// ══════════════════════════════════════
function initSlots(){
  renderTeam('a');
  renderTeam('b');
}

function renderTeam(team){
  const container=document.getElementById(`slots-${team}`);
  container.innerHTML='';
  for(let i=0;i<6;i++){
    container.appendChild(buildSlotEl(team,i));
  }
}

function buildSlotEl(team,slot){
  const poke=teams[team][slot];
  const wrap=document.createElement('div');
  wrap.className='slot-row';
  wrap.dataset.team=team;
  wrap.dataset.slot=slot;

  if(!poke){
    // Slot vacío
    wrap.innerHTML=`
      <div class="slot-main">
        <div class="slot-poke" onclick="openModal('${team}',${slot})">
          <div class="slot-empty">
            <div class="slot-empty-num">SLOT ${slot+1}</div>
            <div class="slot-empty-icon">＋</div>
            <div class="slot-empty-text">Click para añadir</div>
          </div>
        </div>
        <div class="slot-moves" style="align-items:center;justify-content:center;">
          <div class="slot-move-empty">— Sin Pokémon —</div>
        </div>
      </div>`;
    return wrap;
  }

  const pdata=DB?.pokemon?.[poke.name]||{};
  const types=pdata.types||[];
  const sprite=poke.shiny
    ?`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/${pdata.id}.png`
    :(pdata.sprite||`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pdata.id}.png`);

  const typesBadges=types.map(t=>`<span class="type-badge ${TYPE_CLASS[t]||''}">${TIPOS_ES[t]||t}</span>`).join('');

  // Moves seleccionados
  const selMoves=poke.selectedMoves||[];
  const movesHtml=buildMovesListHtml(poke.name,selMoves);

  // Franja tipos: débil a / fuerte contra
  const defenses=calcDefense(types);
  const weakTo=(defenses[4]||[]).concat(defenses[2]||[]);
  const resistTo=(defenses[0.5]||[]).concat(defenses[0.25]||[]);
  const immuneTo=defenses[0]||[];
  const weakHtml=weakTo.slice(0,6).map(t=>`<span class="type-badge ${TYPE_CLASS[t]||''}">${TIPOS_ES[t]||t}</span>`).join('');
  const resistHtml=resistTo.slice(0,6).map(t=>`<span class="type-badge ${TYPE_CLASS[t]||''}">${TIPOS_ES[t]||t}</span>`).join('');

  wrap.innerHTML=`
    <div class="slot-main">
      <div class="slot-poke" onclick="openModal('${team}',${slot})">
        <button class="slot-shiny-btn" onclick="event.stopPropagation();toggleSlotShiny('${team}',${slot})" title="Shiny">✨</button>
        <button class="slot-stats-btn" id="sstats-${team}-${slot}" onclick="event.stopPropagation();toggleSlotStats('${team}',${slot})" title="Stats">STATS</button>
        <div class="slot-filled" id="sfilled-${team}-${slot}">
          <img id="simg-${team}-${slot}" src="${sprite}" alt="${poke.name}" loading="lazy">
          <div class="slot-poke-name">${pdata.name_es||poke.name}</div>
          <div class="slot-poke-num">N.º ${pdata.id||''}</div>
          <div class="slot-types-row">${typesBadges}</div>
        </div>
        <div class="slot-radar-wrap" id="sradar-${team}-${slot}" style="display:none"></div>
      </div>
      <div class="slot-moves">
        <div class="slot-moves-header">
          <span>MOVES</span>
          <button class="slot-edit-moves-btn" onclick="openMovesModal('${team}',${slot})">✏ Editar</button>
        </div>
        <div class="slot-moves-list">${movesHtml}</div>
      </div>
    </div>
    <div class="slot-types-bar">
      <div class="slot-types-section"><span class="slot-types-section-label">⚠ Débil a:</span>${weakHtml||'<span style="color:#444;font-size:.5rem">ninguna</span>'}</div>
      <div class="slot-types-section"><span class="slot-types-section-label">🛡 Resiste:</span>${resistHtml||'<span style="color:#444;font-size:.5rem">ninguna</span>'}</div>
    </div>
    <button class="slot-clear-btn" onclick="clearSlot('${team}',${slot})">🗑 Eliminar Pokémon</button>`;

  return wrap;
}

function buildMovesListHtml(pokeName,selMoves){
  if(!selMoves||selMoves.length===0){
    return `<div class="slot-move-empty">Sin moves seleccionados</div>`;
  }
  return selMoves.map(mname=>{
    const pdata=DB?.pokemon?.[pokeName];
    const moveData=pdata?.moves?.find(m=>m.name===mname);
    const det=moveData?.detail||(DB?.moves?.[mname])||{};
    const typeClass=TYPE_CLASS[det.type]||'';
    const catImg=det.category&&CAT_IMG[det.category]?`<img src="${CAT_IMG[det.category]}" class="mv-cat-img" title="${det.category}">`:'';
    const pow=det.power?`<span class="slot-move-power">${det.power}</span>`:'';
    return `<div class="slot-move-item">
      <span class="mv-type-badge ${typeClass}">${TIPOS_ES[det.type]||det.type||'?'}</span>
      ${catImg}
      <span class="slot-move-name">${mname}</span>
      ${pow}
    </div>`;
  }).join('');
}

function clearSlot(team,slot){
  teams[team][slot]=null;
  renderSlot(team,slot);
  hideAnalysis();
}

function renderSlot(team,slot){
  const container=document.getElementById(`slots-${team}`);
  const old=container.children[slot];
  const newEl=buildSlotEl(team,slot);
  container.replaceChild(newEl,old);
}

function toggleSlotShiny(team,slot){
  if(!teams[team][slot])return;
  teams[team][slot].shiny=!teams[team][slot].shiny;
  const img=document.getElementById(`simg-${team}-${slot}`);
  if(!img)return;
  const pdata=DB?.pokemon?.[teams[team][slot].name]||{};
  img.src=teams[team][slot].shiny
    ?`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/shiny/${pdata.id}.png`
    :(pdata.sprite||`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pdata.id}.png`);
}

function toggleSlotStats(team,slot){
  const btn=document.getElementById(`sstats-${team}-${slot}`);
  const filled=document.getElementById(`sfilled-${team}-${slot}`);
  const radarWrap=document.getElementById(`sradar-${team}-${slot}`);
  if(!btn||!filled||!radarWrap)return;

  const showing=btn.classList.contains('active');
  if(showing){
    btn.classList.remove('active');
    btn.textContent='STATS';
    filled.style.display='flex';
    radarWrap.style.display='none';
  }else{
    btn.classList.add('active');
    btn.textContent='SPRITE';
    filled.style.display='none';
    radarWrap.style.display='flex';
    renderSlotStats(team,slot,radarWrap);
  }
}

function renderSlotStats(team,slot,container){
  const poke=teams[team][slot];
  if(!poke)return;
  const pdata=DB?.pokemon?.[poke.name]||{};
  const hasStats=pdata.hp||pdata.attack||pdata.speed;

  if(!hasStats){
    container.innerHTML='<div style="color:#444;font-size:.54rem;padding:10px;text-align:center">Stats no disponibles</div>';
    return;
  }

  const size=96;
  container.innerHTML=`<canvas id="sradar-canvas-${team}-${slot}" width="${size}" height="${size}"></canvas><div class="slot-mini-bars" id="sminibars-${team}-${slot}"></div>`;

  // Dibujar radar
  const canvas=document.getElementById(`sradar-canvas-${team}-${slot}`);
  const ctx=canvas.getContext('2d');
  const W=canvas.width,H=canvas.height;
  const cx=W/2,cy=H/2;
  const R=Math.min(W,H)/2-16;
  const N=6;
  const ao=-Math.PI/2;
  const col=RADAR_COLORS[team]||RADAR_COLORS.a;
  const vals=STAT_KEYS.map(s=>(pdata[s.key]||0)/STAT_MAX);

  // Telaraña
  for(const lvl of [0.25,0.5,0.75,1]){
    ctx.beginPath();
    for(let i=0;i<N;i++){const a=ao+(2*Math.PI*i)/N;const[x,y]=[cx+R*lvl*Math.cos(a),cy+R*lvl*Math.sin(a)];i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}
    ctx.closePath();ctx.strokeStyle='rgba(255,255,255,0.07)';ctx.lineWidth=1;ctx.stroke();
  }
  // Polígono
  ctx.beginPath();
  for(let i=0;i<N;i++){const a=ao+(2*Math.PI*i)/N;const r=R*vals[i];const[x,y]=[cx+r*Math.cos(a),cy+r*Math.sin(a)];i===0?ctx.moveTo(x,y):ctx.lineTo(x,y);}
  ctx.closePath();ctx.fillStyle=col.fill;ctx.fill();ctx.strokeStyle=col.stroke;ctx.lineWidth=1.5;ctx.stroke();

  // Mini barras
  const barsEl=document.getElementById(`sminibars-${team}-${slot}`);
  barsEl.innerHTML=STAT_KEYS.map(s=>{
    const val=pdata[s.key]||0;
    const pct=Math.round((val/STAT_MAX)*100);
    return `<div class="slot-mini-bar-row ${s.cls}">
      <span class="slot-mini-bar-label">${s.label}</span>
      <span class="slot-mini-bar-val">${val}</span>
      <div class="slot-mini-bar-track"><div class="slot-mini-bar-fill" style="width:${pct}%;background:currentColor"></div></div>
    </div>`;
  }).join('');
}

// ══════════════════════════════════════
// MODAL BÚSQUEDA
// ══════════════════════════════════════
function openModal(team,slot){
  activeSlot={team,slot};
  document.getElementById('modal-title').textContent=`ELIGE EL POKÉMON — SLOT ${slot+1}`;
  document.getElementById('modal-search').value='';
  modalSearchQ='';
  modalPage=0;
  document.getElementById('modal-overlay').style.display='flex';
  applyModalFilters();
  document.getElementById('modal-search').focus();
}

function closeModal(e){
  if(e.target===document.getElementById('modal-overlay'))closeModalBtn();
}
function closeModalBtn(){
  document.getElementById('modal-overlay').style.display='none';
}

function buildTypeFilterGrid(){
  const grid=document.getElementById('type-filter-grid');
  const types=Object.keys(EFF);
  grid.innerHTML=types.map(t=>`
    <button class="type-filter-btn ${TYPE_CLASS[t]||''}" data-type="${t}" onclick="toggleTypeFilter('${t}')">${TIPOS_ES[t]||t}</button>
  `).join('');
}

function toggleTypeFilter(type){
  const idx=modalTypeFilter.indexOf(type);
  if(idx>=0){
    modalTypeFilter.splice(idx,1);
  }else{
    if(modalTypeFilter.length>=2)return; // máximo 2
    modalTypeFilter.push(type);
  }
  // Actualizar botones
  document.querySelectorAll('.type-filter-btn').forEach(b=>{
    b.classList.toggle('active',modalTypeFilter.includes(b.dataset.type));
  });
  modalPage=0;
  applyModalFilters();
}

// Filtro legendario
document.addEventListener('click',e=>{
  const btn=e.target.closest('#legend-filter .filter-btn');
  if(btn){
    document.querySelectorAll('#legend-filter .filter-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    modalLegendFilter=btn.dataset.val;
    modalPage=0;
    applyModalFilters();
  }
  const btn2=e.target.closest('#style-filter .filter-btn');
  if(btn2){
    document.querySelectorAll('#style-filter .filter-btn').forEach(b=>b.classList.remove('active'));
    btn2.classList.add('active');
    modalStyleFilter=btn2.dataset.val;
    modalPage=0;
    applyModalFilters();
  }
});

document.getElementById('modal-search').addEventListener('input',e=>{
  modalSearchQ=e.target.value.toLowerCase().trim();
  modalPage=0;
  applyModalFilters();
});

function applyModalFilters(){
  if(!DB){modalFiltered=[];renderModalGrid();return;}
  modalFiltered=allPokemon.filter(({name})=>{
    const pdata=DB.pokemon[name];
    if(!pdata)return false;
    // Nombre
    if(modalSearchQ&&!name.includes(modalSearchQ)&&!(pdata.name_es||'').toLowerCase().includes(modalSearchQ))return false;
    // Tipos
    if(modalTypeFilter.length>0){
      for(const t of modalTypeFilter)if(!(pdata.types||[]).includes(t))return false;
    }
    // Legendario
    if(modalLegendFilter==='legendary'&&!pdata.is_legendary)return false;
    if(modalLegendFilter==='normal'&&pdata.is_legendary)return false;
    // Estilo (físico/especial: el mayor de attack vs sp_attack)
    if(modalStyleFilter!=='all'){
      const atk=pdata.attack||0,spa=pdata.sp_attack||0;
      if(modalStyleFilter==='physical'&&spa>atk)return false;
      if(modalStyleFilter==='special'&&atk>=spa)return false;
    }
    return true;
  });
  renderModalGrid();
}

function renderModalGrid(){
  const grid=document.getElementById('modal-grid');
  const page=modalFiltered.slice(0,MODAL_PAGE_SIZE*(modalPage+1));
  grid.innerHTML=page.map(({name})=>{
    const pdata=DB.pokemon[name];
    const types=(pdata.types||[]).map(t=>`<span class="type-badge ${TYPE_CLASS[t]||''}">${TIPOS_ES[t]||t}</span>`).join('');
    const sprite=pdata.sprite||`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${pdata.id}.png`;
    return `<div class="modal-poke-card" onclick="addToSlot('${name}')">
      <img src="${sprite}" alt="${name}" loading="lazy" width="80" height="80">
      <div class="modal-poke-name">${pdata.name_es||name}</div>
      <div class="modal-poke-num">N.º ${pdata.id}</div>
      <div class="modal-poke-types">${types}</div>
      <button class="modal-add-btn" onclick="event.stopPropagation();addToSlot('${name}')">+ AÑADIR</button>
    </div>`;
  }).join('');

  const loadMore=document.getElementById('modal-load-more');
  loadMore.style.display=modalFiltered.length>MODAL_PAGE_SIZE*(modalPage+1)?'block':'none';
}

function loadMoreModal(){
  modalPage++;
  renderModalGrid();
}

function addToSlot(name){
  const {team,slot}=activeSlot;
  if(!team&&team!==0)return;
  teams[team][slot]={name,shiny:false,selectedMoves:[]};
  renderSlot(team,slot);
  closeModalBtn();
  hideAnalysis();
}

// ══════════════════════════════════════
// MODAL MOVES
// ══════════════════════════════════════
function openMovesModal(team,slot){
  const poke=teams[team][slot];
  if(!poke)return;
  activeMovesSlot={team,slot};

  document.getElementById('moves-modal-title').textContent=`MOVES — ${(DB?.pokemon?.[poke.name]?.name_es||poke.name).toUpperCase()}`;
  document.getElementById('moves-modal-search').value='';
  document.getElementById('moves-modal-overlay').style.display='flex';
  renderMovesModal(poke,'');
  document.getElementById('moves-modal-search').focus();
}

function renderMovesModal(poke,filter){
  const pdata=DB?.pokemon?.[poke.name];
  if(!pdata){document.getElementById('moves-modal-body').innerHTML='<tr><td colspan="6">Sin datos</td></tr>';return;}

  let moves=pdata.moves||[];
  if(filter)moves=moves.filter(m=>m.name.includes(filter.toLowerCase()));

  const selMoves=poke.selectedMoves||[];

  document.getElementById('moves-modal-body').innerHTML=moves.map(m=>{
    const det=m.detail||(DB?.moves?.[m.name])||{};
    const isStatus=!det.power||det.category==='status';
    const checked=selMoves.includes(m.name);
    const typeClass=TYPE_CLASS[det.type]||'';
    const catImg=det.category&&CAT_IMG[det.category]?`<img src="${CAT_IMG[det.category]}" style="width:32px;height:auto" title="${det.category}">`:'';
    return `<tr class="${checked?'mv-selected':''}" onclick="toggleMoveSelect('${m.name}')">
      <td><input type="checkbox" class="mv-check" ${checked?'checked':''} onclick="event.stopPropagation();toggleMoveSelect('${m.name}')"></td>
      <td style="font-weight:700;white-space:nowrap">${m.name}</td>
      <td><span class="mv-type-badge ${typeClass}">${TIPOS_ES[det.type]||det.type||'?'}</span></td>
      <td>${catImg}</td>
      <td style="text-align:center;font-weight:800;color:${isStatus?'#444':'#ffa502'}">${det.power||'—'}</td>
      <td style="text-align:center;color:#888">${det.accuracy||'—'}</td>
    </tr>`;
  }).join('');
}

function toggleMoveSelect(moveName){
  const {team,slot}=activeMovesSlot;
  const poke=teams[team][slot];
  if(!poke)return;
  const sel=poke.selectedMoves||[];
  const idx=sel.indexOf(moveName);
  if(idx>=0){
    sel.splice(idx,1);
  }else{
    if(sel.length>=4)return; // máx 4
    sel.push(moveName);
  }
  poke.selectedMoves=sel;
  // Refrescar tabla
  const filter=document.getElementById('moves-modal-search').value;
  renderMovesModal(poke,filter);
}

document.getElementById('moves-modal-search').addEventListener('input',e=>{
  const {team,slot}=activeMovesSlot;
  const poke=teams[team][slot];
  if(poke)renderMovesModal(poke,e.target.value);
});

function closeMovesModal(e){
  if(e.target===document.getElementById('moves-modal-overlay'))closeMovesModalBtn();
}
function closeMovesModalBtn(){
  document.getElementById('moves-modal-overlay').style.display='none';
  // Actualizar la lista de moves visible en el slot
  const {team,slot}=activeMovesSlot;
  if(team){
    const poke=teams[team][slot];
    if(poke){
      const movesList=document.querySelector(`#slots-${team}>div:nth-child(${slot+1}) .slot-moves-list`);
      if(movesList)movesList.innerHTML=buildMovesListHtml(poke.name,poke.selectedMoves);
    }
  }
  hideAnalysis();
}

// ══════════════════════════════════════
// ANÁLISIS
// ══════════════════════════════════════
function analyzeTeams(){
  const teamA=teams.a.filter(Boolean);
  const teamB=teams.b.filter(Boolean);
  if(!teamA.length||!teamB.length){
    alert('Cada equipo debe tener al menos 1 Pokémon');return;
  }

  renderAnalysis('a',teamA,teamB);
  renderAnalysis('b',teamB,teamA);

  document.getElementById('analysis-a').style.display='block';
  document.getElementById('analysis-b').style.display='block';

  // Scroll suave al análisis
  document.getElementById('analysis-a').scrollIntoView({behavior:'smooth',block:'nearest'});
}

function hideAnalysis(){
  document.getElementById('analysis-a').style.display='none';
  document.getElementById('analysis-b').style.display='none';
}

// Calcula el mejor multiplicador que puede hacer myPoke contra rival
// considerando los moves seleccionados (o tipos si no hay moves)
function bestMultiplierAgainst(myPoke,rivalTypes){
  const sel=myPoke.selectedMoves||[];
  const pdata=DB?.pokemon?.[myPoke.name]||{};
  const myTypes=pdata.types||[];

  let best=0;

  if(sel.length>0){
    for(const mname of sel){
      const moveData=pdata.moves?.find(m=>m.name===mname);
      const det=moveData?.detail||(DB?.moves?.[mname])||{};
      if(!det.power||det.category==='status')continue;
      let mult=1;
      for(const rt of rivalTypes)mult*=(EFF[det.type]?.[rt]??1);
      best=Math.max(best,Math.round(mult*100)/100);
    }
  }else{
    // Sin moves: usar tipos propios como atacante
    for(const myT of myTypes){
      let mult=1;
      for(const rt of rivalTypes)mult*=(EFF[myT]?.[rt]??1);
      best=Math.max(best,Math.round(mult*100)/100);
    }
  }
  return best;
}

// Multiplicador defensivo: cuánto daño recibe myPoke de rivalPoke
function worstMultiplierReceived(myPoke,rivalPoke){
  const myPdata=DB?.pokemon?.[myPoke.name]||{};
  const myTypes=myPdata.types||[];
  const rivalPdata=DB?.pokemon?.[rivalPoke.name]||{};
  const rivalTypes=rivalPdata.types||[];
  const rivalSel=rivalPoke.selectedMoves||[];

  let worst=0;
  if(rivalSel.length>0){
    for(const mname of rivalSel){
      const moveData=rivalPdata.moves?.find(m=>m.name===mname);
      const det=moveData?.detail||(DB?.moves?.[mname])||{};
      if(!det.power||det.category==='status')continue;
      let mult=1;
      for(const mt of myTypes)mult*=(EFF[det.type]?.[mt]??1);
      worst=Math.max(worst,Math.round(mult*100)/100);
    }
  }else{
    for(const rt of rivalTypes){
      let mult=1;
      for(const mt of myTypes)mult*=(EFF[rt]?.[mt]??1);
      worst=Math.max(worst,Math.round(mult*100)/100);
    }
  }
  return worst;
}

function renderAnalysis(mySide,myTeam,rivalTeam){
  const summaryEl=document.getElementById(`summary-${mySide}`);
  const matchupEl=document.getElementById(`matchup-${mySide}`);

  // ── Resumen ──
  // Amenazas: rivales que hacen ×2 o más a alguno de mis pokémon
  const threats=[];
  for(const rival of rivalTeam){
    const rivalPdata=DB?.pokemon?.[rival.name]||{};
    let maxDmg=0;
    for(const mine of myTeam)maxDmg=Math.max(maxDmg,worstMultiplierReceived(mine,rival));
    if(maxDmg>=2)threats.push({name:rivalPdata.name_es||rival.name,mult:maxDmg});
  }

  // Cobertura: tipos que cubren mis moves ofensivos
  const coveredTypes=new Set();
  for(const mine of myTeam){
    const pdata=DB?.pokemon?.[mine.name]||{};
    const sel=mine.selectedMoves||[];
    if(sel.length>0){
      for(const mname of sel){
        const moveData=pdata.moves?.find(m=>m.name===mname);
        const det=moveData?.detail||(DB?.moves?.[mname])||{};
        if(det.type&&det.power)coveredTypes.add(det.type);
      }
    }else{
      for(const t of pdata.types||[])coveredTypes.add(t);
    }
  }
  const allTypes=Object.keys(EFF);
  const uncovered=allTypes.filter(t=>!coveredTypes.has(t));

  summaryEl.innerHTML=`
    <div class="summary-card">
      <div class="summary-card-title">⚠ AMENAZAS RIVALES</div>
      <div class="summary-card-content">
        ${threats.length===0
          ?'<span class="threat-tag threat-ok">Sin amenazas ×2</span>'
          :threats.map(t=>`<span class="threat-tag threat-danger">${t.name} (×${t.mult})</span>`).join('')}
      </div>
    </div>
    <div class="summary-card">
      <div class="summary-card-title">🗺 COBERTURA</div>
      <div class="summary-card-content">
        ${uncovered.length===0
          ?'<span class="threat-tag threat-ok">Cobertura total</span>'
          :`<span style="color:#666;font-size:.56rem">Sin cubrir: </span>${uncovered.slice(0,8).map(t=>`<span class="threat-tag threat-neutral"><span class="type-badge ${TYPE_CLASS[t]||''}" style="font-size:.46rem">${TIPOS_ES[t]||t}</span></span>`).join('')}`}
      </div>
    </div>`;

  // ── Tabla matchups ──
  // Filas = mis pokémon / Columnas = rival
  const colHeaders=rivalTeam.map(p=>{
    const pd=DB?.pokemon?.[p.name]||{};
    return `<th>${pd.name_es||p.name}</th>`;
  }).join('');

  const rows=myTeam.map(mine=>{
    const minePd=DB?.pokemon?.[mine.name]||{};
    const cells=rivalTeam.map(rival=>{
      const rivalPd=DB?.pokemon?.[rival.name]||{};
      const rivalTypes=rivalPd.types||[];
      const mult=bestMultiplierAgainst(mine,rivalTypes);
      const {txt,cls}=multLabel(mult);
      return `<td><span class="matchup-cell ${cls}" title="Mi ${minePd.name_es||mine.name} vs ${rivalPd.name_es||rival.name}">${txt}</span></td>`;
    }).join('');
    return `<tr><td class="td-label">${minePd.name_es||mine.name}</td>${cells}</tr>`;
  }).join('');

  matchupEl.innerHTML=`
    <table class="matchup-table">
      <thead><tr><th class="th-row-label">Mi equipo \\ Rival</th>${colHeaders}</tr></thead>
      <tbody>${rows}</tbody>
    </table>`;
}

// ══════════════════════════════════════
// INIT
// ══════════════════════════════════════
loadPokedex();
