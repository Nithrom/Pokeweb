const TIPOS_ES={normal:'Normal',fighting:'Lucha',flying:'Volador',poison:'Veneno',ground:'Tierra',rock:'Roca',bug:'Bicho',ghost:'Fantasma',steel:'Acero',fire:'Fuego',water:'Agua',grass:'Planta',electric:'Eléctrico',psychic:'Psíquico',ice:'Hielo',dragon:'Dragón',dark:'Siniestro',fairy:'Hada'};
const TYPE_CLASS={normal:'t-normal',fighting:'t-fighting',flying:'t-flying',poison:'t-poison',ground:'t-ground',rock:'t-rock',bug:'t-bug',ghost:'t-ghost',steel:'t-steel',fire:'t-fire',water:'t-water',grass:'t-grass',electric:'t-electric',psychic:'t-psychic',ice:'t-ice',dragon:'t-dragon',dark:'t-dark',fairy:'t-fairy'};
const CAT_IMG={physical:'img/cat_physical.png',special:'img/cat_special.png',status:'img/cat_status.png'};
const TYPE_ES_EN={normal:'normal',lucha:'fighting',volador:'flying',veneno:'poison',tierra:'ground',roca:'rock',bicho:'bug',fantasma:'ghost',acero:'steel',fuego:'fire',agua:'water',planta:'grass','eléctrico':'electric',electrico:'electric','psíquico':'psychic',psiquico:'psychic',hielo:'ice','dragón':'dragon',dragon:'dragon',siniestro:'dark',hada:'fairy'};

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

// Dado un pokémon (con sus moves y types) y los types del objetivo,
// devuelve hasta 3 nombres de moves ofensivos que le hagan ×2 o más al objetivo
function getStrongMovesAgainst(pokemon, targetTypes){
  if(!DB||!DB.pokemon)return[];
  const dbPoke=DB.pokemon[pokemon.name];
  if(!dbPoke)return[];
  const strong=[];
  for(const m of dbPoke.moves){
    const det=m.detail||(DB.moves&&DB.moves[m.name]);
    if(!det||!det.power||det.category==='status')continue;
    let mult=1;
    for(const dt of targetTypes)mult*=(EFF[det.type]?.[dt]??1);
    if(mult>=2)strong.push({name:m.name,type:det.type,mult:Math.round(mult*100)/100});
  }
  strong.sort((a,b)=>b.mult-a.mult||b.name.localeCompare(a.name));
  // Deduplicar por tipo para mostrar variedad
  const seen=new Set();const result=[];
  for(const s of strong){if(!seen.has(s.type)){seen.add(s.type);result.push(s);}if(result.length>=3)break;}
  return result;
}

const MULT_DEF=[{key:4,label:'×4 Le destroza',cls:'mx4'},{key:2,label:'×2 Supereficaz',cls:'mx2'},{key:1,label:'×1 Normal',cls:'mx1'},{key:0.5,label:'×0,5 Poco eficaz',cls:'mx05'},{key:0.25,label:'×0,25 Muy poco eficaz',cls:'mx025'},{key:0,label:'×0 Inmune',cls:'mx0'}];
const MULT_ATK=[{key:4,label:'×4 Destroza a',cls:'mx4'},{key:2,label:'×2 Supereficaz contra',cls:'mx2'},{key:1,label:'×1 Normal contra',cls:'mx1'},{key:0.5,label:'×0,5 Flojo contra',cls:'mx05'},{key:0.25,label:'×0,25 Muy flojo contra',cls:'mx025'},{key:0,label:'×0 No afecta a',cls:'mx0'}];
const TYPE_POOL={normal:[143,113,241,234,289,446],fighting:[68,107,297,448,534,619],flying:[18,142,277,334,468,561],poison:[34,89,211,454,452,545],ground:[31,75,232,330,443,530],rock:[76,185,219,248,369,411],bug:[123,127,212,214,291,542],ghost:[94,200,302,354,429,477],steel:[81,208,227,376,385,448],fire:[6,38,59,136,157,250],water:[9,54,90,121,131,134],grass:[3,45,103,154,182,254],electric:[26,125,135,181,243,310],psychic:[65,122,196,199,280,376],ice:[87,91,131,144,215,461],dragon:[130,147,230,334,373,445],dark:[197,248,262,359,430,461],fairy:[35,39,176,183,282,468]};

let allPokemon=[],typeCache={},moveDetailCache={};
let DB=null;

function applyPokedexDb(db){
  DB=db;
  allPokemon=Object.entries(DB.pokemon).map(([name,p])=>({name,id:p.id})).sort((a,b)=>a.id-b.id);
  for(const[name,p]of Object.entries(DB.pokemon)){
    typeCache[name]={types:p.types,sprite:p.sprite,id:p.id,allMoves:p.moves};
  }
  if(DB.moves)for(const[mn,detail]of Object.entries(DB.moves))moveDetailCache['__'+mn]=detail;
}

async function loadPokedex(){
  if(typeof checkApiAvailable==='function'&&await checkApiAvailable()){
    try{
      const db=await loadPokemonDbFromApi();
      applyPokedexDb(db);
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon</span>`;
      document.getElementById('search-def').disabled=false;
      document.getElementById('search-atk').disabled=false;
      return;
    }catch(e){console.warn('API pokedex',e);}
  }
  try{
    const res=await fetch('data/pokemon_db.json');
    if(res.ok){
      applyPokedexDb(await res.json());
      document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon</span>`;
      document.getElementById('search-def').disabled=false;
      document.getElementById('search-atk').disabled=false;
      return;
    }
  }catch(e){}
  try{
    const res=await fetch('https://pokeapi.co/api/v2/pokemon?limit=1025');
    const data=await res.json();
    allPokemon=data.results.map((p,i)=>({name:p.name,id:i+1}));
    document.getElementById('status-bar').innerHTML=`<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px"> <span>${allPokemon.length} Pokémon</span>`;
    document.getElementById('search-def').disabled=false;
    document.getElementById('search-atk').disabled=false;
  }catch(e){
    document.getElementById('status-bar').innerHTML='Error cargando la Pokédex.';
  }
}

function formatName(n){return n.split('-').map(w=>w.charAt(0).toUpperCase()+w.slice(1)).join(' ');}
function tc(t){return TYPE_CLASS[t]||'t-normal';}
function tn(t){return TIPOS_ES[t]||t;}
function powerClass(p){if(!p)return 'pow-none';if(p>=100)return 'pow-high';if(p>=60)return 'pow-mid';return 'pow-low';}

// ── Búsqueda: pokemon + tipo simple + doble tipo ──
function setupSearch(inputId,sugId,side){
  const input=document.getElementById(inputId),sug=document.getElementById(sugId);
  input.addEventListener('input',()=>{
    const q=input.value.toLowerCase().trim();
    if(!q){sug.style.display='none';return;}
    const isNum=/^\d+$/.test(q);let matches;
    if(isNum){const n=parseInt(q);matches=allPokemon.filter(p=>p.id===n||String(p.id).startsWith(q)).slice(0,8);}
    else{if(q.length<2){sug.style.display='none';return;}matches=allPokemon.filter(p=>p.name.includes(q)).slice(0,8);}
    if(!matches.length){sug.style.display='none';return;}
    sug.innerHTML=matches.map(p=>`<div class="sug-item" data-name="${p.name}"><img src="https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/${p.id}.png" loading="lazy"><span>${formatName(p.name)}</span><span class="sug-num">${p.id>9999?"???":"N.º "+p.id}</span></div>`).join('');
    sug.style.display='block';
    sug.querySelectorAll('.sug-item').forEach(el=>el.addEventListener('click',()=>{sug.style.display='none';input.value=formatName(el.dataset.name);selectPokemon(el.dataset.name,side);}));
  });
  input.addEventListener('keydown',e=>{
    if(e.key!=='Enter')return;
    sug.style.display='none';
    const q=input.value.toLowerCase().trim();
    // Comprobar doble tipo: "lucha bicho", "hielo dragón", etc.
    const parts=q.split(/\s+/);
    if(parts.length===2){
      const t1=TYPE_ES_EN[parts[0]]||Object.keys(TIPOS_ES).find(k=>TIPOS_ES[k].toLowerCase()===parts[0]);
      const t2=TYPE_ES_EN[parts[1]]||Object.keys(TIPOS_ES).find(k=>TIPOS_ES[k].toLowerCase()===parts[1]);
      if(t1&&t2){searchByDualType(t1,t2,side);return;}
    }
    // Tipo simple
    const typeEn=TYPE_ES_EN[q]||Object.keys(TIPOS_ES).find(k=>TIPOS_ES[k].toLowerCase()===q);
    if(typeEn){searchByType(typeEn,side);}
  });
}

function buildValidatedUrl(baseUrl, moveId) {
  try {
    if (baseUrl.includes('/../') || /\/%2e%2e\//i.test(baseUrl)) {
      throw new Error('Invalid path');
    }
    const url = new URL(baseUrl);
    const allowedDomains = ['pokeapi.co'];
    if (!allowedDomains.includes(url.hostname)) {
      throw new Error('Invalid host');
    }
    if (!['http:', 'https:'].includes(url.protocol)) {
      throw new Error('Invalid protocol');
    }
    if (moveId && !/^[A-Za-z0-9_-]+$/.test(moveId)) {
      throw new Error('Invalid parameter');
    }
    if (moveId) {
      url.pathname = `/api/v2/move/${moveId}`;
    }
    return url.href;
  } catch {
    throw new Error('Invalid URL');
  }
}

async function getMoveDetail(url){
  const moveName=url.split('/').slice(-2,-1)[0];
  const dbKey='__'+moveName;
  if(moveDetailCache[dbKey])return moveDetailCache[dbKey];
  if(moveDetailCache[url])return moveDetailCache[url];
  const lsKey='mv_'+moveName;
  try{const cached=localStorage.getItem(lsKey);if(cached){const r=JSON.parse(cached);moveDetailCache[url]=r;return r;}}catch(e){}
  try{
    const validatedUrl = buildValidatedUrl('https://pokeapi.co', moveName);
    const res=await fetch(validatedUrl);const d=await res.json();
    const r={type:d.type?.name||'normal',category:d.damage_class?.name||'status',power:d.power||null,pp:d.pp||null,accuracy:d.accuracy||null};
    moveDetailCache[url]=r;
    try{localStorage.setItem(lsKey,JSON.stringify(r));}catch(e){}
    return r;
  }catch(e){return{type:'normal',category:'status',power:null,pp:null,accuracy:null};}
}

async function getPokemonData(name){
  if(typeCache[name]){
    const cached=typeCache[name];
    if(cached.allMoves&&cached.allMoves.length>0&&cached.allMoves[0].detail)return cached;
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

// Mapa de familias evolutivas: representante de cada línea
// Solo guardamos los IDs "base" o "más conocidos" de cada familia
// Si un pokémon tiene ID en esta lista, es el representante de su familia
const EVO_FAMILIES = new Set([
  1,4,7,10,13,16,19,21,23,25,27,29,32,35,37,39,41,43,46,48,50,52,54,56,58,60,
  63,66,69,72,74,77,79,81,83,84,86,88,90,92,95,96,98,100,102,104,106,107,108,
  109,111,113,114,115,116,118,120,122,123,124,125,126,127,128,129,131,132,133,
  137,138,140,142,143,144,145,146,147,150,151,152,155,158,161,163,165,167,169,
  170,172,173,174,175,177,179,183,185,187,190,191,193,194,196,197,198,200,201,
  202,203,204,206,207,209,211,213,214,215,216,218,220,222,223,225,226,227,228,
  231,233,234,235,236,238,239,240,241,242,243,244,245,246,249,250,251,252,255,
  258,261,263,265,270,273,276,278,280,283,285,287,290,293,296,298,299,300,302,
  303,304,306,307,309,311,312,313,314,315,316,318,320,322,324,325,327,328,331,
  333,335,336,337,338,339,341,343,345,347,349,351,352,353,355,357,358,359,360,
  361,363,366,369,370,371,374,377,378,379,380,381,382,383,384,385,386,387,390,
  393,396,399,401,403,406,408,410,412,415,417,418,420,422,424,425,427,429,430,
  431,433,434,436,438,439,440,441,442,443,446,447,449,451,453,455,456,458,459,
  460,461,462,463,464,465,466,467,468,469,470,471,472,473,474,475,476,477,478,
  479,480,481,482,483,484,485,486,487,488,489,491,492,493,494,495,498,501,504,
  506,509,511,513,515,517,519,522,524,527,529,531,532,535,538,539,540,543,546,
  548,550,551,554,556,557,559,561,562,564,566,568,570,572,574,577,580,582,585,
  587,588,590,592,594,595,597,599,602,605,607,610,613,615,616,618,619,621,622,
  624,626,627,629,631,632,633,636,638,639,640,641,642,643,644,645,646,647,648,
  649,650,653,656,659,662,665,668,671,672,674,676,677,679,682,684,686,688,690,
  692,694,696,698,700,701,702,703,704,707,708,710,712,714,716,717,718,719,720,
  721,722,725,728,731,734,736,739,741,742,744,746,747,749,751,753,755,757,759,
  761,764,765,766,767,769,771,772,774,775,776,777,778,779,780,781,782,785,786,
  787,788,789,791,792,793,800,801,802,803,806,807,808,810,813,816,819,821,824,
  826,827,829,831,833,835,837,840,842,843,845,846,847,848,850,852,854,856,858,
  859,862,863,864,865,866,867,868,870,871,872,874,875,876,877,878,880,881,882,
  883,884,885,888,889,890,891,892,893,894,895,896,897,898,899,900,901,902,903,
  904,905,906,909,912,915,918,921,922,923,924,925,926,927,928,929,930,931,932,
  933,934,935,936,937,938,939,940,941,942,943,944,945,946,947,948,949,950,951,
  952,953,954,955,956,957,958,959,960,961,962,963,964,965,966,967,968,969,970,
  971,972,973,974,975,976,977,978,979,980,981,982,983,984,985,986,987,988,989,
  990,991,992,993,994,995,996,997,998,999,1000,1001,1002,1003,1004,1005,1006,
  1007,1008,1009,1010,1017,1020,1021,1022,1023,1024,1025
]);

async function getRecsForTypes(goodTypes,count=8){
  if(DB&&DB.pokemon){
    const results=[];
    const seenFamilies=new Set();
    // Iterar por orden de ID para priorizar pokémon base
    const sorted=Object.entries(DB.pokemon).sort((a,b)=>a[1].id-b[1].id);
    for(const t of goodTypes){
      for(const[name,p]of sorted){
        if(!p.types.includes(t))continue;
        // Solo mostrar si es representante de su línea evolutiva
        if(!EVO_FAMILIES.has(p.id))continue;
        const famKey=p.id;
        if(seenFamilies.has(famKey))continue;
        seenFamilies.add(famKey);
        results.push({name,id:p.id,types:p.types,sprite:p.sprite});
        if(results.length>=count)return results;
      }
    }
    return results;
  }
  const ids=new Set();
  for(const t of goodTypes){for(const id of(TYPE_POOL[t]||[])){ids.add(id);if(ids.size>=count)break;}if(ids.size>=count)break;}
  const results=[];
  for(const id of[...ids].slice(0,count)){
    try{const d=await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);const p=await d.json();results.push({name:p.name,id:p.id,types:p.types.map(t=>t.type.name),sprite:p.sprites.other['official-artwork'].front_default||p.sprites.front_default});}
    catch(e){}
  }
  return results;
}

// recRow: muestra moves fuertes del recomendado contra el pokemon seleccionado (en lugar del multiplicador)
function recRow(p,moveTypes,side){
  const isLeft=side==='def';
  const targetName=window._currentPokemon?.[side];
  const targetTypes=targetName&&typeCache[targetName]?typeCache[targetName].types:null;
  let rightHtml='';

  if(targetTypes){
    // Moves del pokémon recomendado fuertes contra el pokemon objetivo
    const strongMoves=getStrongMovesAgainst(p,targetTypes);
    if(strongMoves.length>0){
      const pills=strongMoves.map(m=>{
        const{txt,cls}=multLabel(m.mult);
        return`<span class="rec-strong-move"><span class="rec-badge ${tc(m.type)}">${formatName(m.name)}</span><span class="rec-mult-pill ${cls}">${txt}</span></span>`;
      }).join('');
      rightHtml=`<div class="rec-strong-label">⚠ Puede usar:</div><div class="rec-moves-detail">${pills}</div>`;
    } else {
      rightHtml=`<div class="rec-no-threat">Sin moves fuertes contra ti</div>`;
    }
  } else if(moveTypes&&moveTypes.length>0){
    // Fallback: sin DB, mostrar multiplicador como antes
    const effects=moveTypes.map(a=>{let m=1;for(const d of p.types)m*=(EFF[a]?.[d]??1);return{type:a,mult:Math.round(m*100)/100};}).sort((a,b)=>b.mult-a.mult);
    const{txt,cls}=multLabel(effects[0].mult);
    const detail=effects.map(e=>{const{txt:mt,cls:mc}=multLabel(e.mult);return`<span class="rec-move-eff"><span class="rec-badge ${tc(e.type)}">${tn(e.type)}</span><span class="rec-mult-pill ${mc}">${mt}</span></span>`;}).join('');
    rightHtml=`<div class="rec-best-mult ${cls}">${txt}</div><div class="rec-moves-detail">${detail}</div>`;
  } else {
    const def=calcDefense(p.types);
    const w4=def[4]||[],w2=def[2]||[],imm=def[0]||[],res=(def[0.25]||[]).concat(def[0.5]||[]);
    if(w4.length||w2.length){rightHtml+=`<div class="rec-why-row"><span class="rec-why-label">Débil a:</span>${w4.map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×4</span>`).join('')}${w2.slice(0,3-w4.length).map(t=>`<span class="rec-weak-tag rwt-good">${tn(t)} ×2</span>`).join('')}</div>`;}
    if(imm.length||res.length){rightHtml+=`<div class="rec-why-row"><span class="rec-why-label">Aguanta:</span>${imm.slice(0,2).map(t=>`<span class="rec-weak-tag rwt-immune">${tn(t)} ×0</span>`).join('')}${res.slice(0,3-imm.length).map(t=>`<span class="rec-weak-tag rwt-resist">${tn(t)}</span>`).join('')}</div>`;}
  }
  return`<div class="rec-row" data-poke="${p.name}" data-side="${side}" style="cursor:pointer"><div class="rec-img-wrap"><img class="rec-row-img" src="${p.sprite}" alt="${p.name}" loading="lazy"></div><div class="rec-row-info"><div class="rec-row-name">${formatName(p.name)}</div><div class="rec-row-types">${p.types.map(t=>`<span class="rec-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div>${rightHtml}</div></div>`;
}

// ── Filtro + ordenación de moves ──
function renderMovesTable(side){
  const data=window._movesData?.[side];if(!data)return;
  const isLeft=side==='def';
  const movesList=document.getElementById(isLeft?'moves-list-def':'moves-list-atk');
  const movesCount=document.getElementById(isLeft?'moves-count-def':'moves-count-atk');
  const selInfo=document.getElementById(isLeft?'moves-sel-info-def':'moves-sel-info-atk');

  const q=(data.filter||'').toLowerCase().trim();
  let source=data.all;

  if(q){
    const catMap={'físico':'physical','fisico':'physical','especial':'special','estado':'status'};
    const catQ=catMap[q];
    const typeQ=Object.keys(TYPE_ES_EN).find(k=>k===q)?TYPE_ES_EN[q]:Object.values(TYPE_ES_EN).find(v=>v===q)||null;
    const powerQ=q.replace('%','').replace('potencia','').trim();
    const isNum=!isNaN(parseInt(powerQ))&&powerQ!=='';

    source=data.all.filter(m=>{
      const d=m.detail;
      if(catQ)return d.category===catQ;
      if(typeQ)return d.type===typeQ;
      if(isNum){
        const num=parseInt(powerQ);
        return d.power===num||(d.accuracy!=null&&d.accuracy===num);
      }
      return m.name.includes(q)||formatName(m.name).toLowerCase().includes(q)||tn(d.type).toLowerCase().includes(q);
    });
  }

  // Ordenación
  const sort=data.sort||'default';
  const sorted=[...source];
  if(sort==='name-az')sorted.sort((a,b)=>a.name.localeCompare(b.name));
  else if(sort==='name-za')sorted.sort((a,b)=>b.name.localeCompare(a.name));
  else if(sort==='type-az')sorted.sort((a,b)=>a.detail.type.localeCompare(b.detail.type));
  else if(sort==='type-za')sorted.sort((a,b)=>b.detail.type.localeCompare(a.detail.type));
  else if(sort==='cat')sorted.sort((a,b)=>{const o={physical:0,special:1,status:2};return o[a.detail.category]-o[b.detail.category];});
  else if(sort==='cat-desc')sorted.sort((a,b)=>{const o={physical:0,special:1,status:2};return o[b.detail.category]-o[a.detail.category];});
  else if(sort==='pow-desc')sorted.sort((a,b)=>(b.detail.power||0)-(a.detail.power||0));
  else if(sort==='pow-asc')sorted.sort((a,b)=>(a.detail.power||0)-(b.detail.power||0));
  else if(sort==='acc-desc')sorted.sort((a,b)=>(b.detail.accuracy||0)-(a.detail.accuracy||0));
  else if(sort==='acc-asc')sorted.sort((a,b)=>(a.detail.accuracy||0)-(b.detail.accuracy||0));

  movesCount.textContent=`${sorted.length}${q?` de ${data.all.length}`:''} movs.`;
  movesList.innerHTML=sorted.length?sorted.map(m=>moveRow(m,data.selected.has(m.name),side)).join(''):`<tr><td colspan="6" class="moves-empty">Sin resultados</td></tr>`;
  const nSel=data.selected.size;
  selInfo.style.display=nSel>0?'block':'none';
  if(nSel>0)selInfo.textContent=`${nSel} movimiento${nSel>1?'s':''} seleccionado${nSel>1?'s':''} — click para limpiar`;
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

// Sort por click en th
document.addEventListener('click',e=>{
  const th=e.target.closest('th[data-sort]');if(!th)return;
  const side=th.dataset.side,sortKey=th.dataset.sort;
  const data=window._movesData?.[side];if(!data)return;
  // Ciclo: default → asc → desc → asc ...
  const cur=data.sort||'default';
  const ascKey=sortKey==='name'?'name-az':sortKey==='type'?'type-az':sortKey==='cat'?'cat':sortKey==='pow'?'pow-asc':'acc-asc';
  const descKey=sortKey==='name'?'name-za':sortKey==='type'?'type-za':sortKey==='cat'?'cat-desc':sortKey==='pow'?'pow-desc':'acc-desc';
  data.sort=(cur===ascKey)?descKey:ascKey;
  // Actualizar flechas en todos los th de esa tabla
  const table=th.closest('table');
  table.querySelectorAll('th[data-sort] .sort-arrow').forEach(a=>a.textContent='↕');
  th.querySelector('.sort-arrow').textContent=data.sort.endsWith('-za')||data.sort.endsWith('-desc')||data.sort==='cat-desc'?'↓':'↑';
  renderMovesTable(side);
});

document.addEventListener('click',e=>{
  const info=e.target.closest('.moves-selected-info');if(!info)return;
  const side=info.id.includes('def')?'def':'atk',data=window._movesData?.[side];if(!data)return;
  data.selected.clear();renderMovesTable(side);restoreDefaultRecs(side);
});

function getSelectedMoveTypes(side){
  const data=window._movesData?.[side];if(!data||data.selected.size===0)return[];
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

  // Defensor (isLeft): recomienda pokémon que resistan los tipos de los moves seleccionados
  // Atacante (!isLeft): recomienda pokémon débiles a los tipos de los moves seleccionados
  function scoreTypes(fn){
    return Object.keys(EFF).map(defType=>{
      let score=0;
      for(const atkType of moveTypes) score+=fn(EFF[atkType]?.[defType]??1);
      return{type:defType,score};
    }).filter(x=>x.score>0).sort((a,b)=>b.score-a.score).slice(0,5).map(x=>x.type);
  }

  let goodTypes;
  if(isLeft){
    // Queremos pokémon que resistan estos moves (defensores del atacante)
    // = tipos con multiplicador BAJO contra los move types
    goodTypes=scoreTypes(m=>m===0?3:m<=0.25?2:m<=0.5?1:0);
  } else {
    // Queremos pokémon débiles a estos moves (víctimas del atacante)
    goodTypes=scoreTypes(m=>m>=4?4:m>=2?2:0);
  }

  if(!goodTypes.length) goodTypes=moveTypes;
  const recs=await getRecsForTypes(goodTypes,8);
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

// Shiny toggle
document.addEventListener('click',e=>{
  const btn=e.target.closest('.shiny-btn');if(!btn)return;
  const side=btn.dataset.side;
  const img=document.getElementById(side==='def'?'img-def':'img-atk');
  const isShiny=btn.dataset.shiny==='1';
  const pokeName=window._currentPokemon?.[side];if(!pokeName)return;
  if(isShiny){
    // Volver al normal
    btn.dataset.shiny='0';btn.title='Ver Shiny ✨';btn.style.opacity='0.6';
    const p=typeCache[pokeName];if(p)img.src=p.sprite;
  } else {
    // Intentar shiny
    const id=typeCache[pokeName]?.id;
    if(!id)return;
    btn.dataset.shiny='1';btn.title='Ver normal';btn.style.opacity='1';
    img.src=`https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/shiny/${id}.png`;
    img.onerror=()=>{img.onerror=null;img.src=typeCache[pokeName]?.sprite||'';btn.dataset.shiny='0';};
  }
});

async function selectPokemon(name,side){
  const isLeft=side==='def';
  const cardEl=document.getElementById(isLeft?'card-def':'card-atk');
  const recList=document.getElementById(isLeft?'rec-def':'rec-atk');
  const recLabel=document.getElementById(isLeft?'rec-label-def':'rec-label-atk');
  const typesTitle=document.getElementById(isLeft?'types-title-def':'types-title-atk');
  const typeResults=document.getElementById(isLeft?'type-results-def':'type-results-atk');
  const spinCls=isLeft?'spinner':'spinner spinner-atk';

  // Ocultar resultados de búsqueda por tipo y limpiar
  typeResults.style.display='none';typeResults.innerHTML='';
  cardEl.style.display='none';recLabel.style.display='none';recList.innerHTML='';
  typesTitle.style.display='none';
  document.getElementById(isLeft?'output-left-def':'output-left-atk').innerHTML='';
  document.getElementById(isLeft?'output-right-def':'output-right-atk').innerHTML='';
  document.getElementById(isLeft?'moves-section-def':'moves-section-atk').style.display='none';

  try{
    const{types,sprite,id,allMoves}=await getPokemonData(name);
    document.getElementById(isLeft?'img-def':'img-atk').src=sprite;
    document.getElementById(isLeft?'name-def':'name-atk').textContent=formatName(name);
    document.getElementById(isLeft?'id-def':'id-atk').textContent=id>9999?'???':''+id;
    document.getElementById(isLeft?'types-def':'types-atk').innerHTML=types.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join('');
    // Reset shiny button
    const shinyBtn=document.getElementById(isLeft?'shiny-btn-def':'shiny-btn-atk');
    if(shinyBtn){shinyBtn.dataset.shiny='0';shinyBtn.style.opacity='0.6';shinyBtn.title='Ver Shiny ✨';}
    cardEl.style.display='block';
    // Siempre empezar en modo sprite al cargar un nuevo pokémon
    showSpritePanel(isLeft?'def':'atk');

    const cacheKey=isLeft?'def':'atk';
    window._movesData=window._movesData||{};window._currentPokemon=window._currentPokemon||{};
    window._currentPokemon[cacheKey]=name;
    window._movesData[cacheKey]={all:[],filter:'',sort:'default',selected:new Set()};
    const movesSec=document.getElementById(isLeft?'moves-section-def':'moves-section-atk');
    movesSec.style.display='flex';
    const movesList=document.getElementById(isLeft?'moves-list-def':'moves-list-atk');
    const movesFilter=document.getElementById(isLeft?'moves-filter-def':'moves-filter-atk');
    const sortSel=document.getElementById(isLeft?'moves-sort-def':'moves-sort-atk');
    movesFilter.value='';if(sortSel)sortSel.value='default';
    movesList.innerHTML=`<tr><td colspan="6" class="moves-empty"><span class="${spinCls}"></span> Cargando...</td></tr>`;
    const movesWithDetail=[];
    if(allMoves.length>0&&allMoves[0].detail){movesWithDetail.push(...allMoves);}
    else{for(let i=0;i<allMoves.length;i+=20){const batch=allMoves.slice(i,i+20);const details=await Promise.all(batch.map(m=>getMoveDetail(m.url)));batch.forEach((m,j)=>movesWithDetail.push({...m,detail:details[j]}));}}
    window._movesData[cacheKey].all=movesWithDetail;
    movesFilter.oninput=()=>{window._movesData[cacheKey].filter=movesFilter.value.trim().toLowerCase();renderMovesTable(cacheKey);};
    renderMovesTable(cacheKey);

    typesTitle.style.display='block';
    const eff=isLeft?calcDefense(types):calcAttack(types);
    const config=isLeft?MULT_DEF:MULT_ATK;
    const left=config.slice(0,3),right=config.slice(3);
    const buildCol=cfgs=>cfgs.map(cfg=>{const list=eff[cfg.key]||[];return`<div class="mult-group"><div class="mult-label ${cfg.cls}">${cfg.label} (${list.length})</div><div class="types-grid">${list.length?list.map(t=>`<span class="type-badge ${tc(t)}">${tn(t)}</span>`).join(''):'<span class="none-text">Ninguno</span>'}</div></div>`;}).join('');
    document.getElementById(isLeft?'output-left-def':'output-left-atk').innerHTML=buildCol(left);
    document.getElementById(isLeft?'output-right-def':'output-right-atk').innerHTML=buildCol(right);

    const goodTypes=eff[4].concat(eff[2]);
    if(goodTypes.length>0){
      recLabel.style.display='block';recLabel.textContent=isLeft?'COUNTERS RECOMENDADOS':'POKÉMON DÉBILES';
      recList.innerHTML=`<div class="loading"><span class="${spinCls}"></span></div>`;
      const recs=await getRecsForTypes(goodTypes,8);
      recList.innerHTML=recs.map(p=>recRow(p,[],side)).join('');
    }
  }catch(e){console.error(e);}
}

// Tooltip
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

// Click recomendado → lado contrario
document.addEventListener('click',e=>{
  const row=e.target.closest('.rec-row[data-poke]');if(!row)return;
  const poke=row.dataset.poke,side=row.dataset.side,oppSide=side==='def'?'atk':'def';
  document.getElementById(oppSide==='def'?'search-def':'search-atk').value=formatName(poke);
  selectPokemon(poke,oppSide);
});

// ── Búsqueda por tipo ──
function showTypeResults(side,html){
  const isLeft=side==='def';
  const typeResults=document.getElementById(isLeft?'type-results-def':'type-results-atk');
  // Ocultar zona de pokemon si estaba visible
  document.getElementById(isLeft?'card-def':'card-atk').style.display='none';
  document.getElementById(isLeft?'moves-section-def':'moves-section-atk').style.display='none';
  document.getElementById(isLeft?'types-title-def':'types-title-atk').style.display='none';
  document.getElementById(isLeft?'output-left-def':'output-left-atk').innerHTML='';
  document.getElementById(isLeft?'output-right-def':'output-right-atk').innerHTML='';
  document.getElementById(isLeft?'rec-label-def':'rec-label-atk').style.display='none';
  document.getElementById(isLeft?'rec-def':'rec-atk').innerHTML='';
  typeResults.style.display='block';
  typeResults.innerHTML=html;
}

async function searchByType(typeEn,side){
  const isLeft=side==='def';
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  showTypeResults(side,`<div class="loading"><span class="${spinCls}"></span> Buscando tipo ${tn(typeEn)}...</div>`);
  const container=document.getElementById(isLeft?'type-results-def':'type-results-atk');

  const atkEff=EFF[typeEn]||{};
  const atk4=Object.entries(atkEff).filter(([,v])=>v>=4).map(([k])=>k);
  const atk2=Object.entries(atkEff).filter(([,v])=>v>=2&&v<4).map(([k])=>k);
  const atk1=Object.entries(atkEff).filter(([,v])=>v===1).map(([k])=>k);
  const atk05=Object.entries(atkEff).filter(([,v])=>v>0&&v<1).map(([k])=>k);
  const atk0=Object.entries(atkEff).filter(([,v])=>v===0).map(([k])=>k);
  const defEff=calcDefense([typeEn]);
  const def4=defEff[4]||[],def2=defEff[2]||[],def1=defEff[1]||[],def05=(defEff[0.5]||[]).concat(defEff[0.25]||[]),def0=defEff[0]||[];

  const badgeRow=arr=>arr.length?arr.map(t=>`<span class="type-badge ${tc(t)}" data-typeinfo="${t}" data-side="${side}">${tn(t)}</span>`).join(''):'<span class="none-text">—</span>';
  const multRow=(label,cls,arr)=>arr.length?`<div class="type-info-row"><div class="type-info-label ${cls}">${label}</div><div class="type-info-badges">${badgeRow(arr)}</div></div>`:'';

  const infoBox=`<div class="type-info-box">
    <div class="type-info-name"><span class="type-badge ${tc(typeEn)}">${tn(typeEn)}</span></div>
    <div class="type-info-cols">
      <div><div class="type-info-section-label">⚔ Ataque</div>${multRow('×4 Destroza a:','mx4',atk4)}${multRow('×2 Fuerte contra:','mx2',atk2)}${multRow('×1 Normal contra:','mx1',atk1)}${multRow('×½ Flojo contra:','mx05',atk05)}${multRow('×0 No afecta a:','mx0',atk0)}</div>
      <div><div class="type-info-section-label">🛡 Defensa</div>${multRow('×4 Le destroza:','mx4',def4)}${multRow('×2 Débil a:','mx2',def2)}${multRow('×1 Normal:','mx1',def1)}${multRow('×½ Resiste:','mx05',def05)}${multRow('×0 Inmune a:','mx0',def0)}</div>
    </div>
  </div>`;

  let pokemons=[];
  if(DB&&DB.pokemon){
    pokemons=Object.entries(DB.pokemon).filter(([,p])=>p.types.includes(typeEn)).map(([name,p])=>({name,id:p.id,types:p.types,sprite:p.sprite})).sort((a,b)=>a.id-b.id);
  } else {
    try{
      const r=await fetch('data/pokemon_db.json')
      const d=await r.json();
      const ids=d.pokemon.map(p=>{const parts=p.pokemon.url.split('/');return{name:p.pokemon.name,id:parseInt(parts[parts.length-2])};}).filter(p=>p.id<=1025).sort((a,b)=>a.id-b.id);
      for(let i=0;i<ids.length;i+=20){
        const batch=ids.slice(i,i+20);
        const results=await Promise.all(batch.map(async({name,id})=>{
          if(typeCache[name])return{name,id:typeCache[name].id,types:typeCache[name].types,sprite:typeCache[name].sprite};
          try{const res=await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);const p=await res.json();return{name:p.name,id:p.id,types:p.types.map(t=>t.type.name),sprite:p.sprites.other['official-artwork'].front_default||p.sprites.front_default};}
          catch(e){return null;}
        }));
        pokemons.push(...results.filter(Boolean));
      }
    }catch(e){console.error(e);}
  }

  const cards=pokemons.map(p=>`<div class="type-poke-card" data-poke="${p.name}" data-side="${side}"><img src="${p.sprite}" alt="${p.name}" loading="lazy"><div class="rec-row-name">${formatName(p.name)}</div><div class="rec-row-types">${p.types.map(t=>`<span class="rec-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div></div>`).join('');
  container.innerHTML=`<div class="type-search-title">TIPO: ${tn(typeEn).toUpperCase()} <span style="font-family:'Nunito',sans-serif;font-size:.75rem;color:#606070;font-weight:600">(${pokemons.length} pokémon)</span></div>${infoBox}<div class="type-poke-grid">${cards}</div>`;
}

async function searchByDualType(t1,t2,side){
  const isLeft=side==='def';
  const spinCls=isLeft?'spinner':'spinner spinner-atk';
  showTypeResults(side,`<div class="loading"><span class="${spinCls}"></span> Buscando ${tn(t1)}+${tn(t2)}...</div>`);
  const container=document.getElementById(isLeft?'type-results-def':'type-results-atk');

  let pokemons=[];
  if(DB&&DB.pokemon){
    pokemons=Object.entries(DB.pokemon).filter(([,p])=>p.types.includes(t1)&&p.types.includes(t2)).map(([name,p])=>({name,id:p.id,types:p.types,sprite:p.sprite})).sort((a,b)=>a.id-b.id);
  } else {
    // Sin DB: intersección de dos llamadas de tipo
    try{
      const [r1,r2]=await Promise.all([fetch(`https://pokeapi.co/api/v2/type/${t1}`),fetch(`https://pokeapi.co/api/v2/type/${t2}`)]);
      const [d1,d2]=await Promise.all([r1.json(),r2.json()]);
      const set1=new Set(d1.pokemon.map(p=>p.pokemon.name));
      const both=d2.pokemon.filter(p=>set1.has(p.pokemon.name)).map(p=>{const parts=p.pokemon.url.split('/');return{name:p.pokemon.name,id:parseInt(parts[parts.length-2])};}).filter(p=>p.id<=1025).sort((a,b)=>a.id-b.id);
      for(let i=0;i<both.length;i+=10){
        const batch=both.slice(i,i+10);
        const results=await Promise.all(batch.map(async({name,id})=>{
          if(typeCache[name])return{name,id:typeCache[name].id,types:typeCache[name].types,sprite:typeCache[name].sprite};
          try{const res=await fetch(`https://pokeapi.co/api/v2/pokemon/${id}`);const p=await res.json();return{name:p.name,id:p.id,types:p.types.map(t=>t.type.name),sprite:p.sprites.other['official-artwork'].front_default||p.sprites.front_default};}
          catch(e){return null;}
        }));
        pokemons.push(...results.filter(Boolean));
      }
    }catch(e){console.error(e);}
  }

  const cards=pokemons.length
    ?pokemons.map(p=>`<div class="type-poke-card" data-poke="${p.name}" data-side="${side}"><img src="${p.sprite}" alt="${p.name}" loading="lazy"><div class="rec-row-name">${formatName(p.name)}</div><div class="rec-row-types">${p.types.map(t=>`<span class="rec-badge ${tc(t)}">${tn(t)}</span>`).join('')}</div></div>`).join('')
    :`<div class="loading">No hay pokémon de tipo ${tn(t1)}+${tn(t2)}</div>`;
  container.innerHTML=`<div class="type-search-title">TIPO: ${tn(t1).toUpperCase()} + ${tn(t2).toUpperCase()} <span style="font-family:'Nunito',sans-serif;font-size:.75rem;color:#606070;font-weight:600">(${pokemons.length} pokémon)</span></div><div class="type-poke-grid">${cards}</div>`;
}

// Click en type-info-badge → buscar ese tipo en el mismo lado
document.addEventListener('click',e=>{
  const badge=e.target.closest('.type-info-badges .type-badge[data-typeinfo]');if(!badge)return;
  const typeEn=badge.dataset.typeinfo,side=badge.dataset.side;if(!typeEn||!side)return;
  document.getElementById(side==='def'?'search-def':'search-atk').value=tn(typeEn);
  searchByType(typeEn,side);
});

// Click en type-poke-card → cargar pokémon en lado contrario
document.addEventListener('click',e=>{
  const card=e.target.closest('.type-poke-card');if(!card)return;
  const poke=card.dataset.poke,side=card.dataset.side,oppSide=side==='def'?'atk':'def';
  document.getElementById(oppSide==='def'?'search-def':'search-atk').value=formatName(poke);
  selectPokemon(poke,oppSide);
});

// Click en type-badge de types-grid o types-row → buscar tipo en lado contrario
document.addEventListener('click',e=>{
  const badge=e.target.closest('.types-grid .type-badge, .types-row .type-badge');if(!badge)return;
  const colDef=badge.closest('.col-def'),side=colDef?'def':'atk',oppSide=side==='def'?'atk':'def';
  const typeName=badge.textContent.trim().toLowerCase();
  const typeEn=TYPE_ES_EN[typeName]||Object.keys(TIPOS_ES).find(k=>TIPOS_ES[k].toLowerCase()===typeName);
  if(!typeEn)return;
  document.getElementById(oppSide==='def'?'search-def':'search-atk').value=tn(typeEn);
  searchByType(typeEn,oppSide);
});

setupSearch('search-def','sug-def','def');
setupSearch('search-atk','sug-atk','atk');
document.addEventListener('click',e=>{if(!e.target.closest('.search-wrap'))document.querySelectorAll('.suggestions').forEach(s=>s.style.display='none');});
loadPokedex();

// ══════════════════════════════════════
// STATS RADAR
// ══════════════════════════════════════

const STAT_KEYS = [
  { key: 'hp',         label: 'PS',   cls: 'sb-hp'  },
  { key: 'attack',     label: 'ATQ',  cls: 'sb-atk' },
  { key: 'defense',    label: 'DEF',  cls: 'sb-def' },
  { key: 'sp_attack',  label: 'ATQE', cls: 'sb-spa' },
  { key: 'sp_defense', label: 'DEFE', cls: 'sb-spd' },
  { key: 'speed',      label: 'VEL',  cls: 'sb-spe' },
];
const STAT_MAX = 255; // máximo teórico de PokeAPI

// Colores de relleno del radar por lado
const RADAR_FILL = { def: 'rgba(74,158,255,0.20)', atk: 'rgba(255,170,51,0.20)' };
const RADAR_STROKE = { def: '#4a9eff', atk: '#ffaa33' };

function drawRadar(canvasId, stats, side) {
  const canvas = document.getElementById(canvasId);
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const W = canvas.width, H = canvas.height;
  ctx.clearRect(0, 0, W, H);

  const cx = W / 2, cy = H / 2;
  const R = Math.min(W, H) / 2 - 36; // radio máximo dejando margen para labels
  const N = 6;
  const angleOffset = -Math.PI / 2; // empezar arriba

  function angleOf(i) { return angleOffset + (2 * Math.PI * i) / N; }
  function pointAt(i, r) {
    const a = angleOf(i);
    return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
  }

  // — Fondo: telarañas —
  const levels = [0.25, 0.5, 0.75, 1.0];
  for (const lvl of levels) {
    ctx.beginPath();
    for (let i = 0; i < N; i++) {
      const [x, y] = pointAt(i, R * lvl);
      i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
    }
    ctx.closePath();
    ctx.strokeStyle = 'rgba(255,255,255,0.07)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // — Ejes —
  for (let i = 0; i < N; i++) {
    const [x, y] = pointAt(i, R);
    ctx.beginPath();
    ctx.moveTo(cx, cy);
    ctx.lineTo(x, y);
    ctx.strokeStyle = 'rgba(255,255,255,0.10)';
    ctx.lineWidth = 1;
    ctx.stroke();
  }

  // — Polígono de stats —
  const values = STAT_KEYS.map(s => (stats[s.key] || 0) / STAT_MAX);
  ctx.beginPath();
  for (let i = 0; i < N; i++) {
    const [x, y] = pointAt(i, R * values[i]);
    i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
  }
  ctx.closePath();
  ctx.fillStyle = RADAR_FILL[side] || RADAR_FILL.def;
  ctx.fill();
  ctx.strokeStyle = RADAR_STROKE[side] || RADAR_STROKE.def;
  ctx.lineWidth = 2;
  ctx.stroke();

  // — Puntos en cada vértice —
  for (let i = 0; i < N; i++) {
    const [x, y] = pointAt(i, R * values[i]);
    ctx.beginPath();
    ctx.arc(x, y, 3, 0, 2 * Math.PI);
    ctx.fillStyle = RADAR_STROKE[side] || RADAR_STROKE.def;
    ctx.fill();
  }

  // — Labels de stats —
  ctx.font = 'bold 9px Nunito, sans-serif';
  ctx.fillStyle = '#a0a0b0';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  const labelR = R + 22;
  for (let i = 0; i < N; i++) {
    const [x, y] = pointAt(i, labelR);
    ctx.fillText(STAT_KEYS[i].label, x, y);
  }
}

function renderStatBars(containerId, stats, side) {
  const el = document.getElementById(containerId);
  if (!el) return;
  el.innerHTML = STAT_KEYS.map(s => {
    const val = stats[s.key] || 0;
    const pct = Math.round((val / STAT_MAX) * 100);
    return `<div class="stat-bar-row ${s.cls}">
      <span class="stat-bar-label">${s.label}</span>
      <span class="stat-bar-val">${val}</span>
      <div class="stat-bar-track"><div class="stat-bar-fill" style="width:${pct}%"></div></div>
    </div>`;
  }).join('');
}

function showStatsPanel(side) {
  const name = window._currentPokemon?.[side];
  if (!name) return;

  const spriteWrap = document.getElementById(`sprite-wrap-${side}`);
  const statsWrap  = document.getElementById(`stats-wrap-${side}`);
  const btn        = document.getElementById(`stats-btn-${side}`);
  const shinyBtn   = document.getElementById(`shiny-btn-${side}`);
  const card       = document.getElementById(`card-${side}`);

  const pdata = DB?.pokemon?.[name];
  const hasStats = pdata && (pdata.hp || pdata.attack || pdata.speed);

  spriteWrap.style.display = 'none';
  statsWrap.style.display  = 'flex';
  btn.classList.add('active');
  btn.textContent = 'SPRITE';
  if (shinyBtn) shinyBtn.style.display = 'none';
  // Ocultar nombre, número y tipos
  card.querySelector('.poke-name').style.display   = 'none';
  card.querySelector('.poke-num').style.display    = 'none';
  card.querySelector('.types-row').style.display   = 'none';

  if (!hasStats) {
    statsWrap.innerHTML = '<div class="stats-no-data">Stats no disponibles aún.<br>Ejecuta enrich_stats.py</div>';
    return;
  }

  // Restaurar estructura por si se reusó
  statsWrap.innerHTML = `<canvas id="stats-radar-${side}" width="200" height="200"></canvas><div class="stats-bars" id="stats-bars-${side}"></div>`;
  drawRadar(`stats-radar-${side}`, pdata, side);
  renderStatBars(`stats-bars-${side}`, pdata, side);
}

function showSpritePanel(side) {
  const spriteWrap = document.getElementById(`sprite-wrap-${side}`);
  const statsWrap  = document.getElementById(`stats-wrap-${side}`);
  const btn        = document.getElementById(`stats-btn-${side}`);
  const shinyBtn   = document.getElementById(`shiny-btn-${side}`);
  const card       = document.getElementById(`card-${side}`);

  spriteWrap.style.display = 'flex';
  statsWrap.style.display  = 'none';
  btn.classList.remove('active');
  btn.textContent = 'STATS';
  if (shinyBtn) shinyBtn.style.display = '';
  // Restaurar nombre, número y tipos
  card.querySelector('.poke-name').style.display   = '';
  card.querySelector('.poke-num').style.display    = '';
  card.querySelector('.types-row').style.display   = '';
}

// Toggle al hacer click en el botón STATS / SPRITE
document.addEventListener('click', e => {
  const btn = e.target.closest('.stats-btn');
  if (!btn) return;
  const side = btn.dataset.side;
  const mode = btn.textContent.trim();
  if (mode === 'STATS') {
    showStatsPanel(side);
  } else {
    showSpritePanel(side);
  }
});
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
