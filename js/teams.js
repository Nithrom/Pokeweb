// ══════════════════════════════════════════════════════
//  teams.js — Página de batalla por equipos
// ══════════════════════════════════════════════════════

// ── Datos compartidos de app.js (duplicados aquí para independencia) ──
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

function tc(t){return TYPE_CLASS[t]||'t-normal';}
function tn(t){return TIPOS_ES[t]||t;}
function formatName(n){return n.split('-').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');}
function multLabel(m){if(m>=4)return{txt:'×4',cls:'rm-4'};if(m>=2)return{txt:'×2',cls:'rm-2'};if(m>=1)return{txt:'×1',cls:'rm-1'};if(m>=0.5)return{txt:'×½',cls:'rm-05'};if(m>0)return{txt:'×¼',cls:'rm-025'};return{txt:'×0',cls:'rm-0'};}

// Calcular el mejor multiplicador que los moves de un atacante hacen sobre los tipos de un defensor
function bestMultiplier(attackerMoves, defenderTypes){
  let best=0;
  for(const m of attackerMoves){
    if(!m.detail||!m.detail.power||m.detail.category==='status')continue;
    let mult=1;
    for(const dt of defenderTypes) mult*=(EFF[m.detail.type]?.[dt]??1);
    mult=Math.round(mult*100)/100;
    if(mult>best)best=mult;
  }
  return best;
}

// Calcular el mejor multiplicador solo por tipos (sin moves)
function bestTypeMultiplier(attackerTypes, defenderTypes){
  let best=0;
  for(const at of attackerTypes){
    let mult=1;
    for(const dt of defenderTypes) mult*=(EFF[at]?.[dt]??1);
    mult=Math.round(mult*100)/100;
    if(mult>best)best=mult;
  }
  return best;
}

// ── Estado global ──
let DB=null;
let allPokemon=[];

// Equipos: array de 6 slots, cada slot = {name, id, types, sprite, moves:[{name,detail}]}
const teams={
  a: Array(6).fill(null),
  b: Array(6).fill(null)
};

// ── Carga inicial ──
async function init(){
  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      DB=await res.json();
      allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({name,id:p.id})).sort((a,b)=>a.id-b.id);
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon disponibles</span>`;
    }
  }catch(e){
    // Fallback API
    try{
      const res=await fetch('https://pokeapi.co/api/v2/pokemon?limit=1025');
      const d=await res.json();
      allPokemon=d.results.map((p,i)=>({name:p.name,id:i+1}));
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon disponibles</span>`;
    }catch(e2){document.getElementById('status-bar').textContent='Error cargando.';}
  }
  document.getElementById('search-a').disabled=false;
  document.getElementById('search-b').disabled=false;
  setupSearch('a');
  setupSearch('b');
}

// ── Buscador ──
function setupSearch(team){
  const input=document.getElementById(`search-${team}`);
  const sug=document.getElementById(`sug-${team}`);
  input.addEventListener('input',()=>{
    const q=input.value.toLowerCase().trim();
    if(q.length<2){sug.style.display='none';return;}
    const matches=allPokemon.filter(p=>p.name.includes(q)).slice(0,8);
    if(!matches.length){sug.style.display='none';return;}
    sug.innerHTML=matches.map(p=>`<div class="sug-item" data-name="${p.name}">
      <img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.id}.png" loading="lazy">
      <span>${formatName(p.name)}</span>
      <span class="sug-num">N.º${p.id}</span>
    </div>`).join('');
    sug.style.display='block';
    sug.querySelectorAll('.sug-item').forEach(el=>el.addEventListener('click',()=>{
      sug.style.display='none';
      input.value='';
      addPokemonToTeam(el.dataset.name, team);
    }));
  });
}

// ── Añadir pokémon al equipo ──
async function addPokemonToTeam(name, team){
  // Buscar slot vacío
  const slotIdx=teams[team].findIndex(s=>s===null);
  if(slotIdx===-1){alert('El equipo ya está lleno (6 pokémon).');return;}
  // Ya en el equipo?
  if(teams[team].some(s=>s&&s.name===name)){alert(`${formatName(name)} ya está en el equipo.`);return;}

  const pdata=DB?DB.pokemon[name]:null;
  let pokemon;
  if(pdata){
    const allMovesRaw=pdata.moves||[];
    // Precargar detalles desde DB.moves
    const allMoves=allMovesRaw.map(m=>({
      name:m.name,
      byLevel:m.byLevel,
      level:m.level,
      detail:m.detail||(DB.moves&&DB.moves[m.name])||{type:'normal',category:'status',power:null,accuracy:null,pp:null}
    }));
    pokemon={name,id:pdata.id,types:pdata.types,sprite:pdata.sprite,allMoves,moves:[]};
  } else {
    // Fallback API
    const res=await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`);
    const d=await res.json();
    pokemon={
      name,id:d.id,
      types:d.types.map(t=>t.type.name),
      sprite:d.sprites.other['official-artwork'].front_default||d.sprites.front_default,
      allMoves:[],moves:[]
    };
  }
  teams[team][slotIdx]=pokemon;
  renderSlot(team, slotIdx);
}

// ── Renderizar slot ──
function renderSlot(team, idx){
  const el=document.getElementById(`slot-${team}-${idx}`);
  const p=teams[team][idx];
  if(!p){
    el.className='slot';
    el.innerHTML=`<div class="slot-empty-icon">＋</div><div class="slot-empty-label">Vacío</div>`;
    el.onclick=()=>slotClick(team,idx);
    return;
  }
  const typeBadges=p.types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('');
  const movesBadges=p.moves.length>0
    ?p.moves.map(m=>`<span class="slot-move-badge active">${tn(m.detail?.type||'normal')} ${formatName(m.name)}</span>`).join('')
    :`<span class="slot-add-moves" onclick="openModal('${team}',${idx});event.stopPropagation()">＋ Añadir moves</span>`;
  el.className='slot filled';
  el.innerHTML=`
    <button class="slot-remove" onclick="removePokemon('${team}',${idx});event.stopPropagation()" title="Quitar">✕</button>
    <img class="slot-img" src="${p.sprite}" alt="${p.name}">
    <div class="slot-name">${formatName(p.name)}</div>
    <div class="slot-types">${typeBadges}</div>
    <div class="slot-moves">${movesBadges}</div>`;
  el.onclick=()=>openModal(team,idx);
}

function slotClick(team,idx){
  if(!teams[team][idx]) document.getElementById(`search-${team}`).focus();
}

function removePokemon(team,idx){
  teams[team][idx]=null;
  renderSlot(team,idx);
}

function clearTeam(team){
  if(!confirm('¿Vaciar el equipo?'))return;
  teams[team]=Array(6).fill(null);
  for(let i=0;i<6;i++)renderSlot(team,i);
  document.getElementById(`analysis-${team}`).style.display='none';
}

// ── Modal de moves ──
let _modal={team:null,idx:null,selected:new Set()};

function openModal(team,idx){
  const p=teams[team][idx];if(!p)return;
  _modal.team=team;_modal.idx=idx;
  _modal.selected=new Set(p.moves.map(m=>m.name));

  const overlay=document.getElementById('modal-overlay');
  const modal=document.getElementById('modal');
  overlay.classList.add('open');
  modal.className=team==='b'?'modal modal-b':'modal';
  document.getElementById('modal-title').textContent=formatName(p.name).toUpperCase();
  document.getElementById('modal-confirm').className=`btn-confirm ${team}`;
  document.getElementById('modal-filter').value='';

  renderModalMoves(p.allMoves,'');
  document.getElementById('modal-filter').oninput=e=>renderModalMoves(p.allMoves,e.target.value.toLowerCase().trim());
}

function renderModalMoves(allMoves, filter){
  const list=document.getElementById('modal-moves-list');
  const nSel=_modal.selected.size;
  document.getElementById('modal-count').textContent=nSel;

  const TYPE_ES_EN={normal:'normal',lucha:'fighting',volador:'flying',veneno:'poison',tierra:'ground',roca:'rock',bicho:'bug',fantasma:'ghost',acero:'steel',fuego:'fire',agua:'water',planta:'grass','eléctrico':'electric',electrico:'electric','psíquico':'psychic',psiquico:'psychic',hielo:'ice','dragón':'dragon',dragon:'dragon',siniestro:'dark',hada:'fairy'};
  const catMap={'físico':'physical','fisico':'physical','especial':'special','estado':'status'};

  let filtered=allMoves;
  if(filter){
    const typeQ=TYPE_ES_EN[filter]||null;
    const catQ=catMap[filter]||null;
    const numQ=!isNaN(parseInt(filter))&&filter!==''?parseInt(filter):null;
    filtered=allMoves.filter(m=>{
      const d=m.detail;
      if(typeQ)return d.type===typeQ;
      if(catQ)return d.category===catQ;
      if(numQ!==null)return d.power===numQ||d.accuracy===numQ;
      return m.name.includes(filter)||formatName(m.name).toLowerCase().includes(filter)||tn(d.type).toLowerCase().includes(filter);
    });
  }

  list.innerHTML=filtered.map(m=>{
    const d=m.detail||{};
    const isSel=_modal.selected.has(m.name);
    const isDisabled=!isSel&&nSel>=4;
    const powClass=d.power>=100?'pow-high':d.power>=60?'pow-mid':d.power?'pow-low':'pow-none';
    return`<div class="modal-move-row${isSel?' selected':''}${isDisabled?' disabled':''}" data-move="${m.name}" onclick="toggleModalMove('${m.name}',${isDisabled})">
      <input type="checkbox" class="modal-move-check" ${isSel?'checked':''} readonly>
      <span class="modal-move-name">${formatName(m.name)}</span>
      <span class="modal-move-type ${tc(d.type)}">${tn(d.type)}</span>
      <img class="modal-move-cat" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt="">
      <span class="modal-move-pow ${powClass}">${d.power??'—'}</span>
    </div>`;
  }).join('');
}

function toggleModalMove(moveName, isDisabled){
  if(isDisabled)return;
  if(_modal.selected.has(moveName)) _modal.selected.delete(moveName);
  else if(_modal.selected.size<4) _modal.selected.add(moveName);
  const p=teams[_modal.team][_modal.idx];
  const filter=document.getElementById('modal-filter').value.toLowerCase().trim();
  renderModalMoves(p.allMoves,filter);
}

function confirmMoves(){
  const p=teams[_modal.team][_modal.idx];if(!p)return;
  p.moves=p.allMoves.filter(m=>_modal.selected.has(m.name));
  renderSlot(_modal.team,_modal.idx);
  closeModal();
}

function closeModal(){
  document.getElementById('modal-overlay').classList.remove('open');
}

// Cerrar modal con overlay
document.getElementById('modal-overlay').addEventListener('click',e=>{
  if(e.target===document.getElementById('modal-overlay'))closeModal();
});

// ── Análisis de batalla ──
function analyzeTeam(team){
  const myTeam=teams[team].filter(Boolean);
  const rivalTeam=teams[team==='a'?'b':'a'].filter(Boolean);

  if(myTeam.length===0){alert('Añade al menos un pokémon a tu equipo.');return;}

  const section=document.getElementById(`analysis-${team}`);
  const vsLabel=document.getElementById(`analysis-vs-label-${team}`);
  vsLabel.textContent=document.getElementById(`team-name-${team==='a'?'b':'a'}`).value;
  section.style.display='block';

  buildMatchupTable(team, myTeam, rivalTeam);
  buildCoverage(team, myTeam);
  buildThreats(team, myTeam, rivalTeam);
}

function multToCellClass(m){
  if(m>=4)return'mc-4';if(m>=2)return'mc-2';if(m>=1)return'mc-1';if(m>0)return'mc-05';return'mc-0';
}

function buildMatchupTable(team, myTeam, rivalTeam){
  const table=document.getElementById(`matchup-table-${team}`);
  if(!rivalTeam.length){
    table.innerHTML=`<tr><td style="padding:12px;color:#606070;font-size:.6rem">El equipo rival está vacío</td></tr>`;
    return;
  }

  // Cabecera: pokémon del rival
  let html=`<thead><tr><th></th>`;
  for(const p of rivalTeam){
    html+=`<th><div class="matchup-th-poke"><img src="${p.sprite}" alt="${p.name}"><span>${formatName(p.name)}</span></div></th>`;
  }
  html+=`</tr></thead><tbody>`;

  // Filas: mis pokémon vs cada rival
  for(let i=0;i<myTeam.length;i++){
    const me=myTeam[i];
    html+=`<tr><th><div class="matchup-th-poke"><img src="${me.sprite}" alt="${me.name}"><span>${formatName(me.name)}</span></div></th>`;
    for(let j=0;j<rivalTeam.length;j++){
      const rival=rivalTeam[j];
      // Multiplicador de mis moves contra el rival
      const mult=me.moves.length>0
        ?bestMultiplier(me.moves,rival.types)
        :bestTypeMultiplier(me.types,rival.types);
      const{txt}=multLabel(mult);
      const cellCls=multToCellClass(mult);
      html+=`<td><div class="matchup-cell ${cellCls}" onclick="showMatchupDetail('${team}',${i},${j})" title="${formatName(me.name)} vs ${formatName(rival.name)}">${txt}</div></td>`;
    }
    html+=`</tr>`;
  }
  html+=`</tbody>`;
  table.innerHTML=html;

  // Guardar datos para el detalle
  table._myTeam=myTeam;
  table._rivalTeam=rivalTeam;
  table._team=team;
}

function showMatchupDetail(team, myIdx, rivalIdx){
  const table=document.getElementById(`matchup-table-${team}`);
  const me=table._myTeam[myIdx];
  const rival=table._rivalTeam[rivalIdx];
  const detail=document.getElementById(`matchup-detail-${team}`);

  // Mis moves contra el rival
  const myMoveRows=me.moves.length>0
    ?me.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status').map(m=>{
      let mult=1;
      for(const dt of rival.types)mult*=(EFF[m.detail.type]?.[dt]??1);
      mult=Math.round(mult*100)/100;
      const{txt,cls}=multLabel(mult);
      return`<div class="detail-move-row">
        <span class="modal-move-type ${tc(m.detail.type)}">${tn(m.detail.type)}</span>
        <span class="detail-move-name">${formatName(m.name)}</span>
        <span class="detail-mult ${cls}">${txt}</span>
      </div>`;
    }).join('')
    :`<div style="color:#606070;font-size:.58rem">Sin moves seleccionados — basado en tipos</div>`;

  // Moves del rival contra mí
  const rivalMoveRows=rival.moves.length>0
    ?rival.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status').map(m=>{
      let mult=1;
      for(const dt of me.types)mult*=(EFF[m.detail.type]?.[dt]??1);
      mult=Math.round(mult*100)/100;
      const{txt,cls}=multLabel(mult);
      return`<div class="detail-move-row">
        <span class="modal-move-type ${tc(m.detail.type)}">${tn(m.detail.type)}</span>
        <span class="detail-move-name">${formatName(m.name)}</span>
        <span class="detail-mult ${cls}">${txt}</span>
      </div>`;
    }).join('')
    :`<div style="color:#606070;font-size:.58rem">Sin moves seleccionados — basado en tipos</div>`;

  detail.className=`matchup-detail open`;
  detail.innerHTML=`
    <div class="detail-title">
      <img src="${me.sprite}" style="width:28px;height:28px"> ${formatName(me.name)}
      <span style="color:#e94560;margin:0 4px">VS</span>
      <img src="${rival.sprite}" style="width:28px;height:28px"> ${formatName(rival.name)}
    </div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
      <div>
        <div style="font-size:.55rem;font-weight:800;color:#a0a0b0;margin-bottom:5px">TUS MOVES CONTRA ${formatName(rival.name).toUpperCase()}</div>
        <div class="detail-moves">${myMoveRows}</div>
      </div>
      <div>
        <div style="font-size:.55rem;font-weight:800;color:#a0a0b0;margin-bottom:5px">SUS MOVES CONTRA ${formatName(me.name).toUpperCase()}</div>
        <div class="detail-moves">${rivalMoveRows}</div>
      </div>
    </div>`;
}

function buildCoverage(team, myTeam){
  const covered=new Set();
  for(const p of myTeam){
    const src=p.moves.length>0?p.moves.filter(m=>m.detail?.power&&m.detail?.category!=='status'):[];
    if(src.length>0){
      for(const m of src){
        for(const [defType] of Object.entries(EFF[m.detail.type]||{})){
          if((EFF[m.detail.type][defType]||1)>=2)covered.add(defType);
        }
      }
    } else {
      // Sin moves: usar tipos del pokémon
      for(const at of p.types){
        for(const[defType,mult]of Object.entries(EFF[at]||{})){
          if(mult>=2)covered.add(defType);
        }
      }
    }
  }
  const allTypes=Object.keys(TIPOS_ES);
  document.getElementById(`coverage-${team}`).innerHTML=allTypes.map(t=>
    `<span class="type-badge ${tc(t)} coverage-badge${covered.has(t)?' covered':''}">${tn(t)}</span>`
  ).join('');
}

function buildThreats(team, myTeam, rivalTeam){
  const container=document.getElementById(`threats-${team}`);
  if(!rivalTeam.length){container.innerHTML='';return;}

  // Pokémon del rival que pueden hacer ×2 o más a algún pokémon mío
  const threats=[];
  for(const rival of rivalTeam){
    const victims=[];
    for(const me of myTeam){
      const mult=rival.moves.length>0
        ?bestMultiplier(rival.moves,me.types)
        :bestTypeMultiplier(rival.types,me.types);
      if(mult>=2)victims.push({name:me.name,mult});
    }
    if(victims.length>0){
      threats.push({rival,victims});
    }
  }

  if(!threats.length){
    container.innerHTML=`<div style="color:#2ed573;font-size:.6rem;margin-top:6px">✓ Ningún pokémon rival representa una amenaza clara</div>`;
    return;
  }

  const rivalName=document.getElementById(`team-name-${team==='a'?'b':'a'}`).value;
  container.innerHTML=`<div style="font-size:.58rem;font-weight:800;color:#ff4757;margin:8px 0 5px">⚠ AMENAZAS DEL ${rivalName.toUpperCase()}</div>`+
    threats.map(t=>{
      const victimStr=t.victims.map(v=>{const{txt}=multLabel(v.mult);return`${formatName(v.name)} ${txt}`;}).join(', ');
      return`<div class="threat-row">
        <img src="${t.rival.sprite}" alt="${t.rival.name}">
        <span class="threat-name">${formatName(t.rival.name)}</span>
        <span class="threat-reason">Amenaza a: ${victimStr}</span>
      </div>`;
    }).join('');
}

// ── Guardar equipo en API ──
async function saveTeam(team){
  const members=teams[team].filter(Boolean);
  if(members.length===0){alert('El equipo está vacío.');return;}
  const name=document.getElementById(`team-name-${team}`).value||`Equipo ${team.toUpperCase()}`;
  try{
    const res=await fetch('/api/teams',{
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body:JSON.stringify({
        name,
        pokemon:members.map(p=>({
          pokemon_id:p.id,
          move_ids:[] // simplificado: IDs no disponibles en frontend sin fetch extra
        }))
      })
    });
    if(res.ok){
      const d=await res.json();
      alert(`✓ Equipo "${name}" guardado (ID: ${d.id})`);
    } else {
      alert('Error guardando el equipo.');
    }
  }catch(e){
    alert('No se pudo conectar con la API. ¿Está corriendo el backend?');
  }
}

// ── Menú hamburguesa ──
document.getElementById('nav-btn').addEventListener('click',e=>{
  e.stopPropagation();
  document.getElementById('nav-dropdown').classList.toggle('open');
});
document.addEventListener('click',()=>document.getElementById('nav-dropdown').classList.remove('open'));

// ── Iniciar ──
document.addEventListener('click',e=>{
  if(!e.target.closest('.search-wrap'))
    document.querySelectorAll('.suggestions').forEach(s=>s.style.display='none');
});

init();
