const TIPOS_ES={normal:'Normal',fighting:'Lucha',flying:'Volador',poison:'Veneno',ground:'Tierra',rock:'Roca',bug:'Bicho',ghost:'Fantasma',steel:'Acero',fire:'Fuego',water:'Agua',grass:'Planta',electric:'Eléctrico',psychic:'Psíquico',ice:'Hielo',dragon:'Dragón',dark:'Siniestro',fairy:'Hada'};
const TYPE_CLASS={normal:'t-normal',fighting:'t-fighting',flying:'t-flying',poison:'t-poison',ground:'t-ground',rock:'t-rock',bug:'t-bug',ghost:'t-ghost',steel:'t-steel',fire:'t-fire',water:'t-water',grass:'t-grass',electric:'t-electric',psychic:'t-psychic',ice:'t-ice',dragon:'t-dragon',dark:'t-dark',fairy:'t-fairy'};

const CAT_IMG={
  physical:'img/cat_physical.png',
  special:'img/cat_special.png',
  status:'img/cat_status.png'
};

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
function calcAttack(types){const r={4:[],2:[],1:[],0.5:[],0.25:[],0:[]};for(const d of Object.keys(EFF[Object.keys(EFF)[0]])){let m=1;for(const a of types)m*=(EFF[a][d]??1);const k=Math.round(m*100)/100;if(r[k]!==undefined)r[k].push(d);else if(k>=3)r[4].push(d);else r[1].push(d);}return r;}
function multLabel(m){if(m>=4)return{txt:'×4',cls:'rm-4'};if(m>=2)return{txt:'×2',cls:'rm-2'};if(m>=1)return{txt:'×1',cls:'rm-1'};if(m>=0.5)return{txt:'×½',cls:'rm-05'};if(m>0)return{txt:'×¼',cls:'rm-025'};return{txt:'×0',cls:'rm-0'};}

const MULT_DEF=[{key:4,label:'×4 Le destroza',cls:'mx4'},{key:2,label:'×2 Supereficaz',cls:'mx2'},{key:1,label:'×1 Normal',cls:'mx1'},{key:0.5,label:'×0,5 Poco eficaz',cls:'mx05'},{key:0.25,label:'×0,25 Muy poco eficaz',cls:'mx025'},{key:0,label:'×0 Inmune',cls:'mx0'}];
const MULT_ATK=[{key:4,label:'×4 Destroza a',cls:'mx4'},{key:2,label:'×2 Supereficaz contra',cls:'mx2'},{key:1,label:'×1 Normal contra',cls:'mx1'},{key:0.5,label:'×0,5 Flojo contra',cls:'mx05'},{key:0.25,label:'×0,25 Muy flojo contra',cls:'mx025'},{key:0,label:'×0 No afecta a',cls:'mx0'}];
const TYPE_POOL={normal:[143,113,241,234,289,446],fighting:[68,107,297,448,534,619],flying:[18,142,277,334,468,561],poison:[34,89,211,454,452,545],ground:[31,75,232,330,443,530],rock:[76,185,219,248,369,411],bug:[123,127,212,214,291,542],ghost:[94,200,302,354,429,477],steel:[81,208,227,376,385,448],fire:[6,38,59,136,157,250],water:[9,54,90,121,131,134],grass:[3,45,103,154,182,254],electric:[26,125,135,181,243,310],psychic:[65,122,196,199,280,376],ice:[87,91,131,144,215,461],dragon:[130,147,230,334,373,445],dark:[197,248,262,359,430,461],fairy:[35,39,176,183,282,468]};

let allPokemon=[],typeCache={},moveDetailCache={};
let DB=null; // pokemon_db.json cargado en memoria

async function loadPokedex(){
  // Intentar cargar base de datos local primero
  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      DB=await res.json();
      // Construir lista de todos los pokémon desde la DB
      allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({name,id:p.id})).sort((a,b)=>a.id-b.id);
      // Pre-poblar caches
      for(const[name,p]of Object.entries(DB.pokemon)){
        // Construir allMoves con detail ya incrustado
        typeCache[name]={types:p.types,sprite:p.sprite,id:p.id,allMoves:p.moves};
      }
      if(DB.moves){
        for(const[mn,detail]of Object.entries(DB.moves)){
          moveDetailCache['__'+mn]=detail;
        }
      }
      document.getElementById('status-bar').innerHTML=`🗄 DB local: <span>${allPokemon.length} Pokémon</span> cargados al instante`;
      document.getElementById('search-def').disabled=false;
      document.getElementById('search-atk').disabled=false;
      return;
    }
  }catch(e){}

  // Fallback: API online
  try{
    const res=await fetch('https://pokeapi.co/api/v2/pokemon?limit=1025');
    const data=await res.json();
    allPokemon=data.results.map((p,i)=>({name:p.name,id:i+1}));
    document.getElementById('status-bar').innerHTML=`🌐 API: <span>${allPokemon.length} Pokémon</span> listos (moves cargan al buscar)`;
    document.getElementById('search-def').disabled=false;
    document.getElementById('search-atk').disabled=false;
  }catch(e){document.getElementById('status-bar').innerHTML='Error cargando la Pokédex.';}
}

function formatName(n){return n.split('-').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');}
function tc(t){return TYPE_CLASS[t]||'t-normal';}
function tn(t){return TIPOS_ES[t]||t;}
function powerClass(p){if(!p)return 'pow-none';if(p>=100)return 'pow-high';if(p>=60)return 'pow-mid';return 'pow-low';}

// Nombres de tipo en español → inglés
const TYPE_ES_EN={normal:'normal',lucha:'fighting',volador:'flying',veneno:'poison',tierra:'ground',roca:'rock',bicho:'bug',fantasma:'ghost',acero:'steel',fuego:'fire',agua:'water',planta:'grass',eléctrico:'electric',electrico:'electric',psíquico:'psychic',psiquico:'psychic',hielo:'ice',dragón:'dragon',dragon:'dragon',siniestro:'dark',hada:'fairy'};

function setupSearch(inputId,sugId,side){
  const input=document.getElementById(inputId),sug=document.getElementById(sugId);
  input.addEventListener('input',()=>{
    const q=input.value.toLowerCase().trim();
    if(!q){sug.style.display='none';return;}
    const isNum=/^\d+$/.test(q);let matches;
    if(isNum){const n=parseInt(q);matches=allPokemon.filter(p=>p.id===n||String(p.id).startsWith(q)).slice(0,8);}
    else{if(q.length<2){sug.style.display='none';return;}matches=allPokemon.filter(p=>p.name.includes(q)).slice(0,8);}
    if(!matches.length){sug.style.display='none';return;}
    sug.innerHTML=matches.map(p=>`<div class="sug-item" data-name="${p.name}"><img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/${p.id}.png" loading="lazy"><span>${formatName(p.name)}</span><span class="sug-num">N.º${p.id}</span></div>`).join('');
    sug.style.display='block';
    sug.querySelectorAll('.sug-item').forEach(el=>el.addEventListener('click',()=>{sug.style.display='none';input.value=formatName(el.dataset.name);selectPokemon(el.dataset.name,side);}));
  });
  // Enter → buscar por tipo si coincide
  input.addEventListener('keydown',e=>{
    if(e.key!=='Enter')return;
    const q=input.value.toLowerCase().trim();
    const typeEn=TYPE_ES_EN[q]||Object.values(TYPE_ES_EN).find(v=>v===q);
    if(typeEn){sug.style.display='none';searchByType(typeEn,side);}
  });
}

async function getMoveDetail(url){
  // Si hay DB local, buscar por nombre (clave '__movename' en moveDetailCache)
  const moveName=url.split('/').slice(-2,-1)[0];
  const dbKey='__'+moveName;
  if(moveDetailCache[dbKey])return moveDetailCache[dbKey];
  if(moveDetailCache[url])return moveDetailCache[url];
  // Intentar desde localStorage
  const lsKey='mv_'+moveName;
  try{const cached=localStorage.getItem(lsKey);if(cached){const r=JSON.parse(cached);moveDetailCache[url]=r;return r;}}catch(e){}
  try{
    const res=await fetch(url);const d=await res.json();
    const r={type:d.type?.name||'normal',category:d.damage_class?.name||'status',power:d.power||null,pp:d.pp||null,accuracy:d.accuracy||null};
    moveDetailCache[url]=r;
    try{localStorage.setItem(lsKey,JSON.stringify(r));}catch(e){}
    return r;
  }catch(e){return{type:'normal',category:'status',power:null,pp:null,accuracy:null};}
}

async function getPokemonData(name){
  if(typeCache[name]){
    // Si los moves ya tienen 'detail' incrustado (desde DB), no hay que volver a fetchear
    const cached=typeCache[name];
    if(cached.allMoves&&cached.allMoves.length>0&&cached.allMoves[0].detail)return cached;
    // Si vienen de DB pero sin detail aún, añadirlo desde DB.moves
    if(DB&&DB.moves&&cached.allMoves){
      cached.allMoves=cached.allMoves.map(m=>({...m,detail:DB.moves[m.name]||{type:'normal',category:'status',power:null,pp:null,accuracy:null}}));
      return cached;
    }
    if(cached.allMoves&&cached.allMoves.length>0)return cached;
  }
  const res=await fetch(`https://pokeapi.co/api/v2/pokemon/${name}`);
  const data=await res.json();
  const levelSet=new Map();
  for(const m of data.moves)for(const vd of m.version_group_details)if(vd.move_learn_method.name==='level-up'){if(!levelSet.has(m.move.name))levelSet.set(m.move.name,{url:m.move.url,level:vd.level_learned_at});break;}
  const levelMoves=[];
  for(const[n,info]of levelSet)levelMoves.push({name:n,url:info.url,level:info.level,byLevel:true});
  levelMoves.sort((a,b)=>a.level-b.level||a.name.localeCompare(b.name));
  const otherMoves=[];
  for(const m of data.moves)if(!levelSet.has(m.move.name))otherMoves.push({name:m.move.name,url:m.move.url,level:null,byLevel:false});
  otherMoves.sort((a,b)=>a.name.localeCompare(b.name));
  const result={types:data.types.map(t=>t.type.name),sprite:data.sprites.other['official-artwork'].front_default||data.sprites.front_default,id:data.id,allMoves:[...levelMoves,...otherMoves]};
  typeCache[name]=result;return result;
}

async function getRecsForTypes(goodTypes,count=8){
  const ids=new Set();
  for(const t of goodTypes){for(const id of(TYPE_POOL[t]||[])){ids.add(id);if(ids.size>=count)break;}if(ids.size>=count)break;}
  const results=[];
  for(const id of[...ids].slice(0,count)){
    try{const d=await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);const p=await d.json();results.push({name:p.name,id:p.id,types:p.types.map(t=>t.type.name),sprite:p.sprites.other['official-artwork'].front_default||p.sprites.front_default});}
    catch(e){}
  }
  return results;
}

function recRow(p,moveTypes,side){
  const def=calcDefense(p.types);
  let rightHtml='';
  if(moveTypes&&moveTypes.length>0){
    const effects=moveTypes.map(a=>{let m=1;for(const d of p.types)m*=(EFF[a]?.[d]??1);return{type:a,mult:Math.round(m*100)/100};}).sort((a,b)=>b.mult-a.mult);
    const{txt,cls}=multLabel(effects[0].mult);
    const detail=effects.map(e=>{const{txt:mt,cls:mc}=multLabel(e.mult);return`<span class="rec-move-eff"><span class="rec-badge ${tc(e.type)}">${tn(e.type)}</span><span class="rec-mult-pill ${mc}">${mt}</span></span>`;}).join('');
    rightHtml=`<div class="rec-best-mult ${cls}">${txt}</div><div class="rec-moves-detail">${detail}</div>`;
  }else{
    const w4=def[4]||[],w2=def[2]||[],imm=def[0]||[],res=(def[0.25]||[]).concat(def[0.5]||[]);
    if(w4.length||w2.length){rightHtml+=`<div class="rec-why-row"><span class="rec-why-label">Débil a:</span>${w4.map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×4</span>`).join('')}${w2.slice(0,3-w4.length).map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×2</span>`).join('')}</div>`;}
    if(imm.length||res.length){rightHtml+=`<div class="rec-why-row"><span class="rec-why-label">Aguanta:</span>${imm.slice(0,2).map(t=>`<span class="rec-weak-tag rwt-immune">${tn(t)} ×0</span>`).join('')}${res.slice(0,3-imm.length).map(t=>`<span class="rec-weak-tag rwt-resist">${tn(t)}</span>`).join('')}</div>`;}
  }
  return`<div class="rec-row" data-poke="${p.name}" data-side="${side}" style="cursor:pointer"><div class="rec-img-wrap"><img class="rec-row-img" src="${p.sprite}" alt="${p.name}" loading="lazy"></div><div class="rec-row-info"><div class="rec-row-name">${formatName(p.name)}</div><div class="rec-row-types">${p.types.map(t=>`<span class="rec-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>${rightHtml}</div></div>`;
}

function moveRow(m,isSelected,side){
  const d=m.detail;
  const catTitle=d.category==='physical'?'Físico':d.category==='special'?'Especial':'Estado';
  const tipData=`data-tip="${tn(d.type)}|${catTitle}|${d.power??'—'}|${d.accuracy??'—'}|${d.pp??'—'}"`;
  return`<tr${isSelected?' class="mv-selected"':''} data-move="${m.name}">
    <td><input type="checkbox" class="mv-check" data-side="${side}" data-move="${m.name}"${isSelected?' checked':''}></td>
    <td class="mv-name" ${tipData} style="cursor:help">${formatName(m.name)}</td>
    <td><span class="mv-type-badge ${tc(d.type)}">${tn(d.type)}</span></td>
    <td title="${catTitle}"><img class="mv-cat-img" src="${CAT_IMG[d.category]||CAT_IMG.status}" alt="${catTitle}"></td>
    <td class="mv-power ${powerClass(d.power)}">${d.power??'—'}</td>
    <td class="mv-power">${d.accuracy!=null?d.accuracy+'%':'—'}</td>
  </tr>`;
}

function renderMovesTable(side){
  const data=window._movesData?.[side];if(!data)return;
  const isLeft=side==='def';
  const movesList=document.getElementById(isLeft?'moves-list-def':'moves-list-atk');
  const movesCount=document.getElementById(isLeft?'moves-count-def':'moves-count-atk');
  const selInfo=document.getElementById(isLeft?'moves-sel-info-def':'moves-sel-info-atk');
  const source=data.filter?data.all.filter(m=>m.name.includes(data.filter)||formatName(m.name).toLowerCase().includes(data.filter)):data.all;
  movesCount.textContent=`${source.length}${data.filter?` de ${data.all.length}`:''} movs.`;
  movesList.innerHTML=source.length?source.map(m=>moveRow(m,data.selected.has(m.name),side)).join(''):`<tr><td colspan="6" class="moves-empty">Sin resultados</td></tr>`;
  const nSel=data.selected.size;
  selInfo.style.display=nSel>0?'block':'none';
  if(nSel>0)selInfo.textContent=`${nSel} movimiento${nSel>1?'s':''} seleccionado${nSel>1?'s':''} — click para limpiar`;
}

document.addEventListener('change',e=>{
  const cb=e.target.closest('.mv-check');if(!cb)return;
  const side=cb.dataset.side,data=window._movesData?.[side];if(!data)return;
  if(cb.checked)data.selected.add(cb.dataset.move);else data.selected.delete(cb.dataset.move);
  cb.closest('tr').classList.toggle('mv-selected',cb.checked);
  const isLeft=side==='def',selInfo=document.getElementById(isLeft?'moves-sel-info-def':'moves-sel-info-atk');
  const nSel=data.selected.size;
  selInfo.style.display=nSel>0?'block':'none';
  if(nSel>0)selInfo.textContent=`${nSel} movimiento${nSel>1?'s':''} seleccionado${nSel>1?'s':''} — click para limpiar`;
  updateRecsFromMoves(side);
});

document.addEventListener('click',e=>{
  const info=e.target.closest('.moves-selected-info');if(!info)return;
  const side=info.id.includes('def')?'def':'atk',data=window._movesData?.[side];if(!data)return;
  data.selected.clear();renderMovesTable(side);restoreDefaultRecs(side);
});

function getSelectedMoveTypes(side){
  const data=window._movesData?.[side];if(!data||data.selected.size===0)return[];
  // Solo moves con potencia (no estado) cuentan para daño
  return[...new Set(data.all.filter(m=>data.selected.has(m.name)&&m.detail.power&&m.detail.category!=='status').map(m=>m.detail.type))];
}

async function updateRecsFromMoves(side){
  const moveTypes=getSelectedMoveTypes(side);
  if(!moveTypes.length){restoreDefaultRecs(side);return;}
  const isLeft=side==='def';
  const recList=document.getElementById(isLeft?'rec-def':'rec-atk');
  const recLabel=document.getElementById(isLeft?'rec-label-def':'rec-label-atk');
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  recLabel.style.display='block';
  recLabel.textContent=isLeft?'COUNTERS (por movimientos)':'DÉBILES A TUS MOVIMIENTOS';
  recList.innerHTML=`<div class="loading"><span class="${spinCls}"></span></div>`;
  function scoreTypes(fn){return Object.keys(EFF).map(d=>{let s=0;for(const a of moveTypes)s+=fn(EFF[a]?.[d]??1);return{type:d,score:s};}).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,4).map(x=>x.type);}
  const tgt=isLeft?scoreTypes(m=>m<=0.5?2:m===0?3:m>=2?-2:0):scoreTypes(m=>m>=4?4:m>=2?2:m<=0.5?-1:0);
  const recs=await getRecsForTypes(tgt.length?tgt:moveTypes,8);
  recList.innerHTML=recs.map(p=>recRow(p,moveTypes,side)).join('')||'<div class="loading">Sin resultados</div>';
}

async function restoreDefaultRecs(side){
  const pokeName=window._currentPokemon?.[side];if(!pokeName)return;
  const isLeft=side==='def',{types}=await getPokemonData(pokeName);
  const eff=isLeft?calcDefense(types):calcAttack(types),goodTypes=eff[4].concat(eff[2]);
  const recList=document.getElementById(isLeft?'rec-def':'rec-atk');
  const recLabel=document.getElementById(isLeft?'rec-label-def':'rec-label-atk');
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  recLabel.textContent=isLeft?'COUNTERS RECOMENDADOS':'POKÉMON DÉBILES';
  if(goodTypes.length>0){
    recList.innerHTML=`<div class="loading"><span class="${spinCls}"></span></div>`;
    const recs=await getRecsForTypes(goodTypes,8);
    recList.innerHTML=recs.map(p=>recRow(p,[],side)).join('');
  }
}

async function selectPokemon(name,side){
  const isLeft=side==='def';
  const cardEl=document.getElementById(isLeft?'card-def':'card-atk');
  const recList=document.getElementById(isLeft?'rec-def':'rec-atk');
  const recLabel=document.getElementById(isLeft?'rec-label-def':'rec-label-atk');
  const typesPanel=document.getElementById(isLeft?'types-panel-def':'types-panel-atk');
  const typesTitle=document.getElementById(isLeft?'types-title-def':'types-title-atk');
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  cardEl.style.display='none';recLabel.style.display='none';recList.innerHTML='';
  typesTitle.style.display='none';
  document.getElementById(isLeft?'output-left-def':'output-left-atk').innerHTML='';
  document.getElementById(isLeft?'output-right-def':'output-right-atk').innerHTML='';

  const movesSec=document.getElementById(isLeft?'moves-section-def':'moves-section-atk');
  movesSec.style.display='none';

  try{
    const{types,sprite,id,allMoves}=await getPokemonData(name);
    document.getElementById(isLeft?'img-def':'img-atk').src=sprite;
    document.getElementById(isLeft?'name-def':'name-atk').textContent=formatName(name);
    document.getElementById(isLeft?'id-def':'id-atk').textContent=id;
    document.getElementById(isLeft?'types-def':'types-atk').innerHTML=types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('');
    cardEl.style.display='block';

    // Movimientos
    const cacheKey=isLeft?'def':'atk';
    window._movesData=window._movesData||{};window._currentPokemon=window._currentPokemon||{};
    window._currentPokemon[cacheKey]=name;
    window._movesData[cacheKey]={all:[],filter:'',selected:new Set()};
    movesSec.style.display='flex';
    const movesList=document.getElementById(isLeft?'moves-list-def':'moves-list-atk');
    const movesFilter=document.getElementById(isLeft?'moves-filter-def':'moves-filter-atk');
    movesFilter.value='';
    movesList.innerHTML=`<tr><td colspan="6" class="moves-empty"><span class="${spinCls}"></span> Cargando...</td></tr>`;
    const movesWithDetail=[];
    // Si los moves ya tienen detail incrustado (DB local), usarlos directamente
    if(allMoves.length>0&&allMoves[0].detail){
      movesWithDetail.push(...allMoves);
    } else {
      for(let i=0;i<allMoves.length;i+=20){
        const batch=allMoves.slice(i,i+20);
        const details=await Promise.all(batch.map(m=>getMoveDetail(m.url)));
        batch.forEach((m,j)=>movesWithDetail.push({...m,detail:details[j]}));
      }
    }
    window._movesData[cacheKey].all=movesWithDetail;
    movesFilter.oninput=()=>{window._movesData[cacheKey].filter=movesFilter.value.trim().toLowerCase();renderMovesTable(cacheKey);};
    renderMovesTable(cacheKey);

    // Tipos — dos columnas: ofensivos (4,2,1) izquierda / defensivos (0.5,0.25,0) derecha
    typesTitle.style.display='block';
    const eff=isLeft?calcDefense(types):calcAttack(types);
    const config=isLeft?MULT_DEF:MULT_ATK;
    const left=config.slice(0,3),right=config.slice(3);
    const buildCol=cfgs=>cfgs.map(cfg=>{const list=eff[cfg.key]||[];return`<div class="mult-group"><div class="mult-label ${cfg.cls}">${cfg.label} (${list.length})</div><div class="types-grid">${list.length?list.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join(''):'<span class="none-text">Ninguno</span>'}</div></div>`;}).join('');
    document.getElementById(isLeft?'output-left-def':'output-left-atk').innerHTML=buildCol(left);
    document.getElementById(isLeft?'output-right-def':'output-right-atk').innerHTML=buildCol(right);

    // Recomendados
    const goodTypes=eff[4].concat(eff[2]);
    if(goodTypes.length>0){
      recLabel.style.display='block';recLabel.textContent=isLeft?'COUNTERS RECOMENDADOS':'POKÉMON DÉBILES';
      recList.innerHTML=`<div class="loading"><span class="${spinCls}"></span></div>`;
      const recs=await getRecsForTypes(goodTypes,8);
      recList.innerHTML=recs.map(p=>recRow(p,[],side)).join('');
    }
  }catch(e){console.error(e);}
}

// Tooltip: hover sobre el NOMBRE del movimiento
const _gtt=document.getElementById('mv-global-tooltip');
document.addEventListener('mouseover',e=>{
  const nm=e.target.closest('.mv-name[data-tip]');if(!nm)return;
  const[tipo,cat,pot,prec,pp]=nm.dataset.tip.split('|');
  _gtt.innerHTML=`Tipo: <b>${tipo}</b><br>Cat.: <b>${cat}</b><br>Potencia: <b>${pot}</b><br>Precisión: <b>${prec}</b><br>PP: <b>${pp}</b>`;
  _gtt.style.display='block';
});
document.addEventListener('mousemove',e=>{
  if(_gtt.style.display==='none')return;
  const x=e.clientX+16,y=e.clientY+16;
  _gtt.style.left=Math.min(x,window.innerWidth-_gtt.offsetWidth-8)+'px';
  _gtt.style.top=Math.min(y,window.innerHeight-_gtt.offsetHeight-8)+'px';
});
document.addEventListener('mouseout',e=>{if(e.target.closest('.mv-name[data-tip]'))_gtt.style.display='none';});

// Click en recomendado → carga en el lado CONTRARIO
document.addEventListener('click',e=>{
  const row=e.target.closest('.rec-row[data-poke]');if(!row)return;
  const poke=row.dataset.poke;
  const side=row.dataset.side;
  const oppSide=side==='def'?'atk':'def';
  const input=document.getElementById(oppSide==='def'?'search-def':'search-atk');
  input.value=formatName(poke);
  selectPokemon(poke,oppSide);
});

// ── Búsqueda por tipo ──
async function searchByType(typeEn, side){
  const isLeft=side==='def';
  const container=document.getElementById(isLeft?'type-results-def':'type-results-atk');
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  container.style.display='block';
  container.innerHTML=`<div class="loading"><span class="${spinCls}"></span> Buscando pokémon de tipo ${tn(typeEn)}...</div>`;

  // ── Ficha del tipo con TODOS los multiplicadores ──
  const atkEff=EFF[typeEn]||{};
  // Ataque: cómo afecta este tipo a los demás
  const atk4=Object.entries(atkEff).filter(([,v])=>v>=4).map(([k])=>k);
  const atk2=Object.entries(atkEff).filter(([,v])=>v>=2&&v<4).map(([k])=>k);
  const atk1=Object.entries(atkEff).filter(([,v])=>v===1).map(([k])=>k);
  const atk05=Object.entries(atkEff).filter(([,v])=>v>0&&v<1).map(([k])=>k);
  const atk0=Object.entries(atkEff).filter(([,v])=>v===0).map(([k])=>k);
  // Defensa: cómo le afectan los demás a este tipo
  const defEff=calcDefense([typeEn]);
  const def4=defEff[4]||[];
  const def2=defEff[2]||[];
  const def1=defEff[1]||[];
  const def05=(defEff[0.5]||[]).concat(defEff[0.25]||[]);
  const def0=defEff[0]||[];

  // Badge con data-typeinfo para que sea clickable
  const badgeRow=(arr,clickable=true)=>arr.length
    ?arr.map(t=>`<span class="type-badge ${tc(t)}"${clickable?` data-typeinfo="${t}" data-side="${side}"`:''}>${tn(t)}</span>`).join('')
    :'<span class="none-text">—</span>';

  const multRow=(label,cls,arr)=>arr.length?`<div class="type-info-row"><div class="type-info-label ${cls}">${label}</div><div class="type-info-badges">${badgeRow(arr)}</div></div>`:'';

  const infoBox=`<div class="type-info-box">
    <div class="type-info-name"><span class="type-badge ${tc(typeEn)}">${tn(typeEn)}</span></div>
    <div class="type-info-cols">
      <div>
        <div class="type-info-section-label">⚔ Ataque</div>
        ${multRow('×4 Destroza a:','mx4',atk4)}
        ${multRow('×2 Fuerte contra:','mx2',atk2)}
        ${multRow('×1 Normal contra:','mx1',atk1)}
        ${multRow('×½ Flojo contra:','mx05',atk05)}
        ${multRow('×0 No afecta a:','mx0',atk0)}
      </div>
      <div>
        <div class="type-info-section-label">🛡 Defensa</div>
        ${multRow('×4 Le destroza:','mx4',def4)}
        ${multRow('×2 Débil a:','mx2',def2)}
        ${multRow('×1 Normal:','mx1',def1)}
        ${multRow('×½ Resiste:','mx05',def05)}
        ${multRow('×0 Inmune a:','mx0',def0)}
      </div>
    </div>
  </div>`;

  // ── Todos los pokémon de ese tipo ──
  let pokemons=[];

  if(DB&&DB.pokemon){
    // DB local: filtrar todos los que tengan ese tipo (principal o secundario)
    pokemons=Object.entries(DB.pokemon)
      .filter(([,p])=>p.types.includes(typeEn))
      .map(([name,p])=>({name,id:p.id,types:p.types,sprite:p.sprite}))
      .sort((a,b)=>a.id-b.id);
  } else {
    // API: endpoint /type/{typeEn} devuelve todos los pokémon de ese tipo
    try{
      const r=await fetch(`https://pokeapi.co/api/v2/type/${typeEn}`);
      const d=await r.json();
      const ids=d.pokemon
        .map(p=>{const parts=p.pokemon.url.split('/');return{name:p.pokemon.name,id:parseInt(parts[parts.length-2])};})
        .filter(p=>p.id<=1025)
        .sort((a,b)=>a.id-b.id);
      // Fetch en paralelo de todos (en batches para no saturar)
      for(let i=0;i<ids.length;i+=20){
        const batch=ids.slice(i,i+20);
        const results=await Promise.all(batch.map(async({name,id})=>{
          // Intentar desde typeCache primero
          if(typeCache[name])return{name,id:typeCache[name].id,types:typeCache[name].types,sprite:typeCache[name].sprite};
          try{
            const res=await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);
            const p=await res.json();
            return{name:p.name,id:p.id,types:p.types.map(t=>t.type.name),sprite:p.sprites.other['official-artwork'].front_default||p.sprites.front_default};
          }catch(e){return null;}
        }));
        pokemons.push(...results.filter(Boolean));
        // Actualizar UI parcialmente mientras carga
        if(i===0){
          container.innerHTML=`<div class="type-search-title">TIPO: ${tn(typeEn).toUpperCase()} <span style="font-size:.6em;color:#606070">(${ids.length} pokémon)</span></div>${infoBox}<div class="loading"><span class="${spinCls}"></span> Cargando pokémon...</div>`;
        }
      }
    }catch(e){console.error(e);}
  }

  const cards=pokemons.map(p=>`
    <div class="type-poke-card" data-poke="${p.name}" data-side="${side}">
      <img src="${p.sprite}" alt="${p.name}" loading="lazy">
      <div class="rec-row-name">${formatName(p.name)}</div>
      <div class="rec-row-types">${p.types.map(t=>`<span class="rec-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>
    </div>`).join('');

  container.innerHTML=`
    <div class="type-search-title">TIPO: ${tn(typeEn).toUpperCase()} <span style="font-family:'Nunito',sans-serif;font-size:.75rem;color:#606070;font-weight:600">(${pokemons.length} pokémon)</span></div>
    ${infoBox}
    <div class="type-poke-grid">${cards}</div>`;
}

// Click en badge de tipo DENTRO de type-info-box → buscar ese tipo en el mismo lado
document.addEventListener('click',e=>{
  const badge=e.target.closest('.type-info-badges .type-badge[data-typeinfo]');
  if(!badge)return;
  const typeEn=badge.dataset.typeinfo;
  const side=badge.dataset.side;
  if(!typeEn||!side)return;
  const input=document.getElementById(side==='def'?'search-def':'search-atk');
  input.value=tn(typeEn);
  searchByType(typeEn,side);
});

// Click en type-badge de la zona de tipos → buscar ese tipo en el otro lado
document.addEventListener('click',e=>{
  const badge=e.target.closest('.types-grid .type-badge, .types-row .type-badge');
  if(!badge)return;
  // Determinar en qué columna estamos
  const colDef=badge.closest('.col-def'),side=colDef?'def':'atk';
  const oppSide=side==='def'?'atk':'def';
  const typeName=badge.textContent.trim().toLowerCase();
  const typeEn=TYPE_ES_EN[typeName]||Object.keys(TIPOS_ES).find(k=>TIPOS_ES[k].toLowerCase()===typeName);
  if(!typeEn)return;
  const input=document.getElementById(oppSide==='def'?'search-def':'search-atk');
  input.value=tn(typeEn);
  searchByType(typeEn,oppSide);
});

setupSearch('search-def','sug-def','def');
setupSearch('search-atk','sug-atk','atk');
document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap'))document.querySelectorAll('.suggestions').forEach(s=>s.style.display='none');});
loadPokedex();
