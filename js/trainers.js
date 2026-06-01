// ══════════════════════════════════════════════════════
//  trainers.js — Batalla contra entrenadores
//  Depende de teams.js (ya cargado antes)
// ══════════════════════════════════════════════════════

let TRAINERS_DB = null;
/** Caché de equipos canónicos (evita mezclar Rojo/Azul con Amarillo vía API/SQL desactualizado). */
let _trainersJsonCache = null;

function countTrainersInDb(db){
  if(!db)return 0;
  if(db.trainers){
    const n=Object.values(db.trainers).reduce((s,list)=>s+(list?.length||0),0);
    if(n>0)return n;
  }
  if(db.games?.length){
    const fromGames=db.games.reduce((s,g)=>s+(Number(g.trainer_count)||0),0);
    if(fromGames>0)return fromGames;
  }
  const apiTotal=Number(db._trainerTotal);
  if(Number.isFinite(apiTotal)&&apiTotal>0)return apiTotal;
  return 0;
}

function formatTrainersStatusBar(pokemonCount,trainerCount){
  return `<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px">`+
    `<span>${pokemonCount} Pokémon · ${trainerCount} entrenadores</span>`;
}

function refreshTrainersStatusBar(){
  const bar=document.getElementById('status-bar');
  if(!bar||!TRAINERS_DB)return;
  bar.innerHTML=formatTrainersStatusBar(
    allPokemon?.length||0,
    countTrainersInDb(TRAINERS_DB),
  );
}

/** Gen 2 / HGSS: gimnasios Johto (orden 1–8) y revancha Kanto (9–16). */
const DUAL_REGION_GYM_GAMES=new Set(['gold-silver','crystal','heartgold-soulsilver']);
const KANTO_GYM_ORDER_MIN=9;

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
  /** RSE: Treecko→Blaziken, Torchic→Swampert, Mudkip→Sceptile */
  3:{treecko:'blaziken',torchic:'swampert',mudkip:'sceptile'},
  4:{turtwig:'infernape',chimchar:'empoleon',piplup:'torterra'},
  5:{snivy:'emboar',tepig:'samurott',oshawott:'serperior'},
  6:{chespin:'delphox',fennekin:'greninja',froakie:'chesnaught'},
  7:{rowlet:'incineroar',litten:'primarina',popplio:'decidueye'},
  8:{grookey:'cinderace',scorbunny:'inteleon',sobble:'rillaboom'},
  9:{sprigatito:'skeledirge',fuecoco:'quaquaval',quaxly:'meowscarada'},
};

/** Gen de iniciales si difiere del campo gen del juego en BD. */
const STARTER_GEN_BY_GAME={
  'firered-leafgreen':1,
};

/** Campeones cuyo slot de inicial depende de tu elección (triángulo rival). */
const RIVAL_STARTER_CHAMPIONS={
  'red-blue':new Set(['Blue']),
  'yellow':new Set(['Blue']),
  'ruby-sapphire':new Set(['Steven']),
  'firered-leafgreen':new Set(['Blue']),
  'diamond-pearl':new Set(['Cynthia']),
  'platinum':new Set(['Cynthia']),
};

const STARTER_LINE_BY_GEN={
  1:['bulbasaur','ivysaur','venusaur','charmander','charmeleon','charizard','squirtle','wartortle','blastoise'],
  3:['treecko','grovyle','sceptile','torchic','combusken','blaziken','mudkip','marshtomp','swampert'],
  4:['turtwig','grotle','torterra','chimchar','monferno','infernape','piplup','prinplup','empoleon'],
};

const GEN3_CHAMPION_STARTER_SLOT=new Set(['aggron','cradily','armaldo']);

/** Hau (USUM): Eevee evoluciona a la ventaja sobre tu inicial. */
const HAU_EEVEELUTION={rowlet:'flareon',litten:'vaporeon',popplio:'leafeon'};
const EEVEELUTIONS=new Set(['vaporeon','jolteon','flareon','espeon','umbreon','leafeon','glaceon','sylveon']);

/** Slugs sin guión (scrape) → slug en pokemon_db / moves */
const MOVE_SLUG_ALIASES={
  thundershock:'thunder-shock',
  thunderpunch:'thunder-punch',
  poisonpowder:'poison-powder',
  sonicboom:'sonic-boom',
  doubleslap:'double-slap',
  doublekick:'double-kick',
  selfdestruct:'self-destruct',
  smokescreen:'smoke-screen',
  bubblebeam:'bubble-beam',
  hijumpkick:'high-jump-kick',
  'hi-jump-kick':'high-jump-kick',
  pinmissile:'pin-missile',
  sonicboom:'sonic-boom',
  thundershock:'thunder-shock',
  dynamicpunch:'dynamic-punch',
  dragonbreath:'dragon-breath',
  smokescreen:'smoke-screen',
  sandattack:'sand-attack',
  faintattack:'feint-attack',
  featherdance:'feather-dance',
  spiderweb:'spider-web',
  rockwrecker:'rock-wrecker',
  mudshot:'mud-shot',
  whirlwind:'whirlwind',
  roost:'roost',
  icefang:'ice-fang',
  ancientpower:'ancient-power',
  stringshot:'string-shot',
  solarbeam:'solar-beam',
  extremespeed:'extreme-speed',
  lightscreen:'light-screen',
  psychup:'psych-up',
  perishsong:'perish-song',
  zapcannon:'zap-cannon',
  lockon:'lock-on',
  mirrormove:'mirror-move',
  cottonspore:'cotton-spore',
  scaryface:'scary-face',
  spikecannon:'spike-cannon',
  defensecurl:'defense-curl',
  horndrill:'horn-drill',
  firespin:'fire-spin',
  fireblast:'fire-blast',
  hydropump:'hydro-pump',
  gigadrain:'giga-drain',
  megadrain:'mega-drain',
  leechseed:'leech-seed',
  sleeppowder:'sleep-powder',
  razorleaf:'razor-leaf',
  vinewhip:'vine-whip',
  petaldance:'petal-dance',
  sunnyday:'sunny-day',
  raindance:'rain-dance',
  batonpass:'baton-pass',
  futuresight:'future-sight',
  shockwave:'shock-wave',
  rocktomb:'rock-tomb',
  armthrust:'arm-thrust',
  bulkup:'bulk-up',
  focusenergy:'focus-energy',
  overheat:'overheat',
  facade:'facade',
  teeterdance:'teeter-dance',
  bellydrum:'belly-drum',
  slackoff:'slack-off',
  aerialace:'aerial-ace',
  endeavor:'endeavor',
  steelwing:'steel-wing',
  dragondance:'dragon-dance',
  calmind:'calm-mind',
  waterpulse:'water-pulse',
  sweetkiss:'sweet-kiss',
  needlearm:'needle-arm',
  shadowpunch:'shadow-punch',
  skillswap:'skill-swap',
  willowisp:'will-o-wisp',
  iceball:'ice-ball',
  sheercold:'sheer-cold',
  meteormash:'meteor-mash',
  dragonclaw:'dragon-claw',
  doubleedge:'double-edge',
  extrasensory:'extrasensory',
  fakeout:'fake-out',
  swordsdance:'swords-dance',
  focuspunch:'focus-punch',
  hiddenpower:'hidden-power',
  waterspout:'water-spout',
  crabhammer:'crabhammer',
  magnitude:'magnitude',
  dragondance:'dragon-dance',
  rapidspin:'rapid-spin',
  sweetscent:'sweet-scent',
  megahorn:'megahorn',
  spikecannon:'spike-cannon',
  slackoff:'slack-off',
  megakick:'mega-kick',
  crosschop:'cross-chop',
  poisonfang:'poison-fang',
  leechlife:'leech-life',
  solarbeam:'solar-beam',
  shadowsneak:'shadow-sneak',
  magicalleaf:'magical-leaf',
  grassknot:'grass-knot',
  aurasphere:'aura-sphere',
  forcepalm:'force-palm',
  metalclaw:'metal-claw',
  dragonrage:'dragon-rage',
  mudshot:'mud-shot',
  aquajet:'aqua-jet',
  shadowclaw:'shadow-claw',
  gyroball:'gyro-ball',
  irondefense:'iron-defense',
  iceshard:'ice-shard',
  woodhammer:'wood-hammer',
  doublehit:'double-hit',
  thunderfang:'thunder-fang',
  icefang:'ice-fang',
  firefang:'fire-fang',
  bulletseed:'bullet-seed',
  bugbuzz:'bug-buzz',
  airslash:'air-slash',
  nightslash:'night-slash',
  attackorder:'attack-order',
  defendorder:'defend-order',
  healorder:'heal-order',
  closecombat:'close-combat',
  poisonfang:'poison-fang',
  aquatail:'aqua-tail',
  hammerarm:'hammer-arm',
  suckerpunch:'sucker-punch',
  rockpolish:'rock-polish',
  stoneedge:'stone-edge',
  flareblitz:'flare-blitz',
  poisonjab:'poison-jab',
  ominouswind:'ominous-wind',
  darkpulse:'dark-pulse',
  silverwind:'silver-wind',
  toxicspikes:'toxic-spikes',
  dragonpulse:'dragon-pulse',
  mirrorcoat:'mirror-coat',
  aircutter:'air-cutter',
};

const YELLOW_BLUE_EEVEELUTIONS=[
  {id:'vaporeon',label:'Vaporeon'},
  {id:'jolteon',label:'Jolteon'},
  {id:'flareon',label:'Flareon'},
];

function needsYellowBlueEeveelution(trainer,slug){
  return slug==='yellow'&&trainer?.name==='Blue'&&trainer?.type==='champion'
    &&!!(trainer.teamByEeveelution&&Object.keys(trainer.teamByEeveelution).length);
}

const MAX_TEAM=6;

function normalizeMoveSlug(name){
  if(!name)return name;
  const k=name.toLowerCase().replace(/\s+/g,'');
  return MOVE_SLUG_ALIASES[k]||MOVE_SLUG_ALIASES[name]||name;
}

function getTrainerBaseTeam(trainer,starterId,slug,eeveelutionId){
  if(needsYellowBlueEeveelution(trainer,slug)&&eeveelutionId&&trainer.teamByEeveelution[eeveelutionId]){
    return JSON.parse(JSON.stringify(trainer.teamByEeveelution[eeveelutionId]));
  }
  if(trainer?.teamByStarter&&starterId&&trainer.teamByStarter[starterId]){
    return JSON.parse(JSON.stringify(trainer.teamByStarter[starterId]));
  }
  return JSON.parse(JSON.stringify(trainer?.team||[]));
}

const DIFFICULTY_LEVEL_GAP=3;
/** Challenge Mode con equipos distintos (Gen 5). */
const CHALLENGE_MODE_GAMES=new Set(['black-white-2']);

function getDifficultyLabels(slug){
  if(slug==='black-white-2'){
    return{normal:'Normal / Fácil',challenge:'Challenge Mode'};
  }
  return{normal:'Normal / Fácil',challenge:'Difícil'};
}

function getGameGen(slug){
  const g=TRAINERS_DB?.games?.find(x=>x.slug===slug);
  const n=Number(g?.gen);
  return Number.isFinite(n)&&n>0?n:0;
}

function getStarterGen(slug){
  if(STARTER_GEN_BY_GAME[slug]!=null)return STARTER_GEN_BY_GAME[slug];
  return getGameGen(slug);
}

function gameHasStarters(slug){
  if(!slug)return false;
  const gen=getStarterGen(slug);
  return!!(GEN_STARTERS[gen]?.length);
}

function trainerUsesRivalStarterSwap(trainer,slug){
  if(!trainer||!slug)return false;
  if(trainer.type!=='champion')return false;
  if(trainer.teamByStarter&&Object.keys(trainer.teamByStarter).length)return true;
  const names=RIVAL_STARTER_CHAMPIONS[slug];
  return!!names&&names.has(trainer.name);
}

function swapRivalStarterSlot(team,keepFinal,gen,trainer,slug){
  const rivalGen=getStarterGen(slug)||gen;
  const finals=STARTER_FINALS_BY_GEN[rivalGen]||[];
  const lines=STARTER_LINE_BY_GEN[rivalGen]||[];
  const swapNames=new Set([...finals,...lines]);
  if(rivalGen===3){
    GEN3_CHAMPION_STARTER_SLOT.forEach(n=>swapNames.add(n));
  }
  if(slug==='firered-leafgreen'&&trainer.name==='Blue'){
    ['arcanine','charizard','charmeleon','charmander'].forEach(n=>swapNames.add(n));
  }
  const idx=team.findIndex(p=>swapNames.has(p.name));
  if(idx<0)return team;
  const template=team[idx];
  const dbMon=typeof allPokemon!=='undefined'?allPokemon.find(x=>x.name===keepFinal):null;
  const out=team.map((p,i)=>{
    if(i!==idx)return p;
    return{
      ...template,
      name:keepFinal,
      name_display:dbMon?.name_es||formatName(keepFinal),
      types:dbMon?.types?.length?[...dbMon.types]:(template.types||[]),
    };
  });
  return out;
}

function blockSpecies(block){
  return block.map(p=>p.name);
}

function blockAvgLevel(block){
  if(!block.length)return 0;
  return block.reduce((s,p)=>s+(p.level||0),0)/block.length;
}

/** Punto de corte: misma especie reaparece con varios niveles más (p. ej. BW2). */
function splitDifficultyBlocks(team,levelGap=DIFFICULTY_LEVEL_GAP){
  if(!team?.length)return[team||[]];
  const firstLevel={};
  for(let i=0;i<team.length;i++){
    const n=team[i].name;
    const lv=team[i].level||0;
    if(firstLevel[n]!==undefined&&lv>firstLevel[n]+levelGap){
      return[team.slice(0,i),team.slice(i)];
    }
    if(firstLevel[n]===undefined)firstLevel[n]=lv;
  }
  return[team];
}

/** Revancha: mismos Pokémon, mismo tamaño de equipo, niveles claramente mayores. */
function isRematchBlockPattern(blocks){
  if(!blocks||blocks.length<2)return false;
  const[b0,b1]=blocks;
  if(b0.length<3||b1.length<3||b0.length!==b1.length)return false;
  const n0=new Set(blockSpecies(b0));
  const n1=new Set(blockSpecies(b1));
  if(n0.size!==n1.size)return false;
  for(const n of n0)if(!n1.has(n))return false;
  return blockAvgLevel(b1)>=blockAvgLevel(b0)+6;
}

function isRematchEntry(trainer){
  return(trainer?.specialty||'').startsWith('rematch');
}

/** Otro registro en el mismo juego (p. ej. líder vs revancha en la liga). */
function getRematchPeer(trainer,slug){
  if(!trainer||!slug||!TRAINERS_DB)return null;
  const all=TRAINERS_DB.trainers[slug]||[];
  if(isRematchEntry(trainer)){
    return all.find(t=>t.name===trainer.name&&t.type===trainer.type&&!isRematchEntry(t))||null;
  }
  return all.find(t=>t.name===trainer.name&&t.type===trainer.type&&isRematchEntry(t))||null;
}

function getEmbeddedRematchBlocks(team){
  const blocks=splitDifficultyBlocks(team);
  return isRematchBlockPattern(blocks)?blocks:null;
}

function trainerHasRematchVariants(trainer,slug){
  if(!trainer)return false;
  if(getRematchPeer(trainer,slug))return true;
  const embedded=getEmbeddedRematchBlocks(trainer.team||[]);
  if(!embedded)return false;
  // Equipo embebido en un solo JSON: liga/campeón/rival, no gimnasios (evita falsos positivos scrape)
  if(['gym','kahuna','captain'].includes(trainer.type))return false;
  return true;
}

/** Challenge real: solo BW2; primer bloque sin especies repetidas; no es patrón de revancha. */
function trainerHasDifficultyVariants(trainer,slug){
  if(!CHALLENGE_MODE_GAMES.has(slug))return false;
  const team=trainer?.team||[];
  const blocks=splitDifficultyBlocks(team);
  if(blocks.length<2||blocks[0].length<2||blocks[1].length<2)return false;
  if(isRematchBlockPattern(blocks))return false;
  const b0=blocks[0];
  if(blockSpecies(b0).length!==b0.length)return false;
  const n0=new Set(blockSpecies(b0));
  const n1=new Set(blockSpecies(blocks[1]));
  if(n0.size===n1.size&&[...n0].every(n=>n1.has(n)))return false;
  return blocks[1].length>b0.length||[...n0].some(n=>n1.has(n));
}

function isOptionalSelectorActive(idPrefix){
  const group=document.getElementById(`sel-${idPrefix}-group`);
  return !!(group&&!group.hasAttribute('hidden'));
}

function setOptionalSelectorVisible(idPrefix,show){
  const group=document.getElementById(`sel-${idPrefix}-group`);
  const arrow=document.getElementById(`arrow-before-${idPrefix}`);
  const sel=document.getElementById(`sel-${idPrefix}`);
  for(const el of [group,arrow]){
    if(!el)continue;
    if(show){
      el.removeAttribute('hidden');
      el.removeAttribute('aria-hidden');
    }else{
      el.setAttribute('hidden','');
      el.setAttribute('aria-hidden','true');
    }
  }
  if(sel){
    sel.disabled=!show;
    if(!show)sel.value=idPrefix==='rematch'?'first':'normal';
  }
}

function setRematchSelectorVisible(show){
  setOptionalSelectorVisible('rematch',show);
}

function setDifficultySelectorVisible(show){
  setOptionalSelectorVisible('difficulty',show);
}

function resetRematchSelector(){
  const sel=document.getElementById('sel-rematch');
  if(sel){
    sel.value='first';
    sel.onchange=updateLoadTrainerButton;
  }
  setRematchSelectorVisible(false);
}

function resetDifficultySelector(){
  const sel=document.getElementById('sel-difficulty');
  if(sel){
    sel.value='normal';
    sel.onchange=updateLoadTrainerButton;
  }
  setDifficultySelectorVisible(false);
}

function buildRematchSelector(slug,trainer){
  const sel=document.getElementById('sel-rematch');
  const show=!!(trainer&&trainerHasRematchVariants(trainer,slug));
  if(!show){
    resetRematchSelector();
    return;
  }
  setRematchSelectorVisible(true);
  if(isRematchEntry(trainer))sel.value='rematch';
  else if(sel.value!=='rematch')sel.value='first';
  sel.onchange=updateLoadTrainerButton;
}

function buildDifficultySelector(slug,trainer){
  const sel=document.getElementById('sel-difficulty');
  const show=!!(trainer&&trainerHasDifficultyVariants(trainer,slug));
  if(!show){
    resetDifficultySelector();
    return;
  }
  setDifficultySelectorVisible(true);
  const labels=getDifficultyLabels(slug);
  sel.options[0].textContent=labels.normal;
  sel.options[1].textContent=labels.challenge;
  sel.value=sel.value==='challenge'?'challenge':'normal';
  sel.onchange=updateLoadTrainerButton;
}

function resetEeveelutionSelector(){
  const sel=document.getElementById('sel-eeveelution');
  if(sel){
    sel.value='vaporeon';
    sel.onchange=onEeveelutionChange;
  }
  setOptionalSelectorVisible('eeveelution',false);
}

function buildEeveelutionSelector(slug,trainer){
  if(!needsYellowBlueEeveelution(trainer,slug)){
    resetEeveelutionSelector();
    return;
  }
  const sel=document.getElementById('sel-eeveelution');
  setOptionalSelectorVisible('eeveelution',true);
  sel.innerHTML=YELLOW_BLUE_EEVEELUTIONS.map(e=>
    `<option value="${e.id}">${e.label}</option>`).join('');
  if(!sel.value||!trainer.teamByEeveelution[sel.value])sel.value='vaporeon';
  sel.onchange=onEeveelutionChange;
}

function onEeveelutionChange(){
  updateLoadTrainerButton();
  const selTrainer=document.getElementById('sel-trainer');
  if(selTrainer?.value)loadTrainer();
}

/** Revancha, dificultad y Eeveelución (Blue/Yellow): solo si aplican. */
function buildTrainerOptionSelectors(slug,trainer){
  resetRematchSelector();
  resetDifficultySelector();
  resetEeveelutionSelector();
  if(!trainer||!slug)return;
  if(trainerHasRematchVariants(trainer,slug))buildRematchSelector(slug,trainer);
  if(trainerHasDifficultyVariants(trainer,slug))buildDifficultySelector(slug,trainer);
  buildEeveelutionSelector(slug,trainer);
}

function updateLoadTrainerButton(){
  const slug=document.getElementById('sel-game').value;
  const trainerVal=document.getElementById('sel-trainer').value;
  const starterEl=document.getElementById('sel-starter');
  const gen=getGameGen(slug);
  const needsStarter=gameHasStarters(slug);
  const starterOk=!needsStarter||!!starterEl.value;
  const trainerOk=!!trainerVal&&(useApi()||!isNaN(parseInt(trainerVal)));
  const eeveeOk=!isOptionalSelectorActive('eeveelution')
    ||!!document.getElementById('sel-eeveelution')?.value;
  document.getElementById('btn-load-trainer').disabled=!(slug&&trainerOk&&starterOk&&eeveeOk);
}

async function ensureTrainersJson(){
  if(_trainersJsonCache)return _trainersJsonCache;
  const res=await fetch('data/trainers_db.json');
  if(!res.ok)throw new Error('No trainers_db.json');
  _trainersJsonCache=await res.json();
  return _trainersJsonCache;
}

function findJsonTrainer(json,gameSlug,trainer){
  const list=json?.trainers?.[gameSlug]||[];
  return list.find(t=>
    t.name===trainer.name&&
    t.type===trainer.type&&
    (t.order||0)===(trainer.order||0)
  )||list.find(t=>t.name===trainer.name&&t.type===trainer.type);
}

function applyJsonTeam(trainer,gameSlug,json){
  if(!json||!trainer)return trainer;
  const jt=findJsonTrainer(json,gameSlug,trainer);
  if(!jt)return trainer;
  return{
    ...trainer,
    location:jt.location||trainer.location,
    sprite:jt.sprite||trainer.sprite,
    team:JSON.parse(JSON.stringify(jt.team||[])),
    teamByStarter:jt.teamByStarter
      ?JSON.parse(JSON.stringify(jt.teamByStarter))
      :trainer.teamByStarter,
    teamByEeveelution:jt.teamByEeveelution
      ?JSON.parse(JSON.stringify(jt.teamByEeveelution))
      :trainer.teamByEeveelution,
  };
}

function trainerOptionValue(gameSlug,trainer){
  return useApi()&&trainer.slug?`${gameSlug}/${trainer.slug}`:null;
}

function gymLeaderRegion(trainer,gameSlug){
  if(trainer?.region==='johto'||trainer?.region==='kanto')return trainer.region;
  if(!DUAL_REGION_GYM_GAMES.has(gameSlug)||trainer?.type!=='gym')return null;
  const o=trainer.order||0;
  if(o>=KANTO_GYM_ORDER_MIN)return 'kanto';
  if(o>=1)return 'johto';
  return null;
}

const TRAINER_TYPE_SORT={gym:0,kahuna:0,elite4:1,champion:2,captain:3,other:4};

function compareTrainers(a,b,gameSlug){
  const ta=TRAINER_TYPE_SORT[a.type]??4;
  const tb=TRAINER_TYPE_SORT[b.type]??4;
  if(ta!==tb)return ta-tb;
  const ra=gymLeaderRegion(a,gameSlug);
  const rb=gymLeaderRegion(b,gameSlug);
  if(ra&&rb&&ra!==rb)return ra==='johto'?-1:1;
  return(a.order||0)-(b.order||0);
}

function trainerSelectGroupKey(trainer,gameSlug){
  if(trainer.type==='gym'){
    const region=gymLeaderRegion(trainer,gameSlug);
    if(region)return `gym-${region}`;
  }
  return trainer.type||'other';
}

function trainerSelectGroupLabel(groupKey){
  const labels={
    'gym-johto':'── Líderes de Gimnasio (Johto) ──',
    'gym-kanto':'── Líderes de Gimnasio (Kanto) ──',
    gym:'── Líderes de Gimnasio ──',
    kahuna:'── Kahunas ──',
    captain:'── Capitanes ──',
    elite4:'── Alto Mando ──',
    champion:'── Campeón ──',
    other:'── Otros ──',
  };
  return labels[groupKey]||groupKey;
}

function findTrainerInSorted(sorted,gameSlug,val){
  if(!val||!sorted?.length)return null;
  const idx=parseInt(val,10);
  if(!isNaN(idx)&&idx>=0&&idx<sorted.length)return sorted[idx];
  if(useApi()){
    const key=val.includes('/')?val:`${gameSlug}/${val}`;
    const bySlug=sorted.find(t=>trainerOptionValue(gameSlug,t)===key);
    if(bySlug)return bySlug;
  }
  return sorted.find(t=>t.name===val||String(t.slug)===val)||null;
}

function parseTeamByEeveelution(t,slug){
  if(t.teamByEeveelution)return t.teamByEeveelution;
  const s=t.team_by_starter;
  if(slug==='yellow'&&t.name==='Blue'&&s?.vaporeon){
    return{vaporeon:s.vaporeon,jolteon:s.jolteon,flareon:s.flareon};
  }
  return null;
}

function normalizeTrainerFromApi(t,gameSlug){
  return{
    id:t.id,
    slug:t.slug,
    gameSlug:gameSlug||t.game_slug||'',
    name:t.name,
    type:t.type,
    order:t.order,
    region:t.region||null,
    location:t.location||'',
    badge:t.badge||'',
    specialty:t.specialty||'',
    sprite:t.sprite,
    teamByStarter:t.teamByStarter||t.team_by_starter||null,
    teamByEeveelution:parseTeamByEeveelution(t,gameSlug),
    team:(t.team||[]).map(m=>({
      name:m.name,
      name_display:m.name_es||formatName(m.name),
      level:m.level,
      types:m.types_en||m.types||[],
      moves:(m.moves||[]).map(mv=>{
        const slug=normalizeMoveSlug(mv.name);
        return{
          name:slug,
          name_display:mv.name_es||mv.name_display||formatName(slug),
        };
      }),
    })),
  };
}

async function loadTrainersForGame(slug){
  if(!slug)return[];
  if(TRAINERS_DB?.trainers?.[slug]?.length){
    return TRAINERS_DB.trainers[slug];
  }
  if(!useApi()){
    console.warn('loadTrainersForGame requiere API o trainers_db.json');
    return [];
  }
  let json=null;
  try{
    json=await ensureTrainersJson();
  }catch(e){
    console.warn('trainers_db.json:',e);
  }
  const list=await fetchApi(`/trainers?game_slug=${encodeURIComponent(slug)}`);
  const normalized=list.map(t=>{
    const n=normalizeTrainerFromApi(t,slug);
    return json?applyJsonTeam(n,slug,json):n;
  });
  if(!TRAINERS_DB.trainers)TRAINERS_DB.trainers={};
  TRAINERS_DB.trainers[slug]=normalized;
  return normalized;
}

// ── Carga de datos ────────────────────────────────────
async function initTrainers(){
  const bar=document.getElementById('status-bar');
  try{
    if(typeof setStatusLoading==='function'){
      setStatusLoading('Cargando entrenadores y Pokédex…');
    }

    const json=await ensureTrainersJson();
    TRAINERS_DB={
      games:(json.games||[]).map(g=>({
        slug:g.slug,
        name:g.name,
        gen:Number(g.gen)||STARTER_GEN_BY_GAME[g.slug]||0,
        region:g.region||'',
        trainer_count:Number(g.trainer_count)||0,
      })),
      trainers:json.trainers||{},
    };

    if(typeof loadPokemonDb==='function'){
      const dexOk=await loadPokemonDb({quiet:true});
      if(!dexOk||!allPokemon.length)throw new Error('Pokédex no cargada');
    }else{
      let tries=0;
      while((!DB||!allPokemon.length)&&tries<50){
        await new Promise(r=>setTimeout(r,200));
        tries++;
      }
    }

    if(typeof checkApiAvailable==='function'&&await checkApiAvailable(true)){
      try{
        const apiGames=await fetchApi('/games');
        if(apiGames?.length){
          TRAINERS_DB.games=apiGames.map(g=>{
            const meta=json.games?.find(x=>x.slug===g.slug);
            return{
              slug:g.slug,
              name:g.name||meta?.name,
              gen:Number(g.gen)||Number(meta?.gen)||STARTER_GEN_BY_GAME[g.slug]||0,
              region:g.region||meta?.region||'',
              trainer_count:Number(g.trainer_count)||Number(meta?.trainer_count)||0,
            };
          });
        }
      }catch(e){console.warn('/games',e);}
    }

    buildGameSelector();
    resetStarterSelector();
    resetRematchSelector();
    resetDifficultySelector();
    resetEeveelutionSelector();
    refreshTrainersStatusBar();
    if(typeof bootstrapTeamsUI==='function')bootstrapTeamsUI();
  }catch(e){
    console.error('initTrainers',e);
    if(bar){
      bar.textContent='Error: sube data/trainers_db.json y data/pokemon_db.json al hosting, o conecta la API.';
    }
  }
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

function resetStarterSelector(msg='— Elige juego —'){
  const sel=document.getElementById('sel-starter');
  if(!sel)return;
  sel.innerHTML=`<option value="">${msg}</option>`;
  sel.disabled=true;
  sel.value='';
  sel.onchange=onStarterChange;
}

function onStarterChange(){
  updateLoadTrainerButton();
  const selTrainer=document.getElementById('sel-trainer');
  if(selTrainer?.value)loadTrainer();
}

function buildStarterSelector(slug){
  const sel=document.getElementById('sel-starter');
  if(!sel)return;

  if(!slug){
    resetStarterSelector();
    return;
  }

  const gen=getStarterGen(slug);
  const starters=GEN_STARTERS[gen];
  if(!starters?.length){
    console.warn('Sin iniciales para',slug,'gen',gen);
    resetStarterSelector('— Sin iniciales —');
    return;
  }

  sel.innerHTML=starters.map(s=>`<option value="${s.id}">${s.label}</option>`).join('');
  sel.disabled=false;
  sel.value=starters[0].id;
  sel.onchange=onStarterChange;
}

function populateTrainerSelect(trainers,sorted){
  const selTrainer=document.getElementById('sel-trainer');
  const slug=document.getElementById('sel-game').value;
  selTrainer.innerHTML='<option value="">— Entrenador —</option>';
  let lastGroup='';
  let currentOg=null;
  sorted.forEach((t,i)=>{
    const typeLabel={gym:'🏟 Líder',kahuna:'🌺 Kahuna',captain:'🏝 Capitán',elite4:'🏆 Alto Mando',champion:'👑 Campeón',other:'⚔ Otro'}[t.type]||'';
    const groupKey=trainerSelectGroupKey(t,slug);
    if(groupKey!==lastGroup){
      currentOg=document.createElement('optgroup');
      currentOg.label=trainerSelectGroupLabel(groupKey);
      selTrainer.appendChild(currentOg);
      lastGroup=groupKey;
    }
    const opt=document.createElement('option');
    opt.value=trainerOptionValue(slug,t)??String(i);
    const roleHint=t.type==='champion'?' (Campeón)':t.type==='gym'&&t.order?` (Gimnasio ${t.order})`:'';
    opt.textContent=`${typeLabel} ${t.name}${roleHint}${t.location?' — '+t.location:''}`;
    (currentOg||selTrainer).appendChild(opt);
  });
  selTrainer.disabled=false;
  selTrainer.value='';
  selTrainer._sorted=sorted;
  buildTrainerOptionSelectors(slug,null);
  selTrainer.onchange=()=>{
    const val=selTrainer.value;
    const tr=findTrainerInSorted(sorted,slug,val);
    buildTrainerOptionSelectors(slug,tr);
    updateLoadTrainerButton();
  };
}

async function onGameChange(){
  const slug=document.getElementById('sel-game').value;
  const selTrainer=document.getElementById('sel-trainer');
  updateLoadTrainerButton();

  if(!slug){
    selTrainer.innerHTML='<option value="">— Entrenador —</option>';
    selTrainer.disabled=true;
    buildStarterSelector('');
    resetRematchSelector();
    resetDifficultySelector();
    resetEeveelutionSelector();
    return;
  }

  buildStarterSelector(slug);
  resetRematchSelector();
  resetDifficultySelector();
  resetEeveelutionSelector();

  selTrainer.disabled=true;
  selTrainer.innerHTML='<option value="">Cargando entrenadores…</option>';

  let trainers=[];
  try{
    trainers=await loadTrainersForGame(slug);
  }catch(e){
    console.error('onGameChange',slug,e);
    selTrainer.innerHTML='<option value="">Error al cargar</option>';
    return;
  }
  if(!trainers.length){
    selTrainer.innerHTML='<option value="">Sin entrenadores</option>';
    selTrainer.disabled=true;
    return;
  }

  const sorted=[...trainers].sort((a,b)=>compareTrainers(a,b,slug));

  populateTrainerSelect(trainers,sorted);
  updateLoadTrainerButton();
}

function applyStarterFilters(team,trainer,slug,starterId){
  if(trainer?.teamByStarter&&starterId&&trainer.teamByStarter[starterId]){
    return JSON.parse(JSON.stringify(trainer.teamByStarter[starterId]));
  }

  const gen=getGameGen(slug);
  const finals=STARTER_FINALS_BY_GEN[gen]||[];
  const rivalGen=getStarterGen(slug)||gen;
  const keepFinal=RIVAL_COUNTER_BY_GEN[rivalGen]?.[starterId];
  team=JSON.parse(JSON.stringify(team));

  if(trainer.name==='Hau'&&slug.includes('ultra')){
    const keepEevee=HAU_EEVEELUTION[starterId];
    team=team.filter(p=>!EEVEELUTIONS.has(p.name)||p.name===keepEevee);
  }

  if(!keepFinal||!trainerUsesRivalStarterSwap(trainer,slug))return team;

  const finalsInTeam=finals.filter(f=>team.some(p=>p.name===f));
  if(finalsInTeam.length>=2){
    const nonFinal=team.filter(p=>!finals.includes(p.name));
    const kept=team.find(p=>p.name===keepFinal);
    if(kept)return [...nonFinal.slice(0,MAX_TEAM-1),kept];
    return nonFinal.slice(0,MAX_TEAM);
  }
  if(finalsInTeam.length===1&&finalsInTeam[0]===keepFinal)return team;
  return swapRivalStarterSlot(team,keepFinal,rivalGen,trainer,slug);
}

/** Dos bloques idénticos en JSON (error enrich); no confundir con revancha real. */
function collapseDuplicatedRoster(team){
  if(!team||team.length<4||team.length%2!==0)return team;
  const half=team.length/2;
  const first=team.slice(0,half);
  const second=team.slice(half);
  const n0=first.map(p=>p.name);
  const n1=second.map(p=>p.name);
  if(n0.length!==n1.length||!n0.every((n,i)=>n===n1[i]))return team;
  if(isRematchBlockPattern([first,second]))return team;
  return first;
}

/** Iniciales rivales, revancha, Challenge Mode (BW2). */
function resolveTrainerTeam(trainer, slug, starterId, difficulty, rematchSel, eeveelutionId){
  const peer=getRematchPeer(trainer,slug);
  let team;
  const base=getTrainerBaseTeam(trainer,starterId,slug,eeveelutionId);

  if(rematchSel==='rematch'&&peer){
    team=getTrainerBaseTeam(peer,starterId,slug,eeveelutionId);
  }else if(rematchSel==='rematch'){
    const embedded=getEmbeddedRematchBlocks(base);
    team=embedded?embedded[embedded.length-1]:[...base];
  }else if(peer&&!isRematchEntry(trainer)){
    team=[...base];
  }else{
    const embedded=getEmbeddedRematchBlocks(base);
    team=embedded?embedded[0]:[...base];
  }

  team=collapseDuplicatedRoster(team);
  team=applyStarterFilters(team,trainer,slug,starterId);

  if(trainerHasDifficultyVariants({team},slug)){
    const diffBlocks=splitDifficultyBlocks(team);
    const wantChallenge=difficulty==='challenge';
    team=wantChallenge?diffBlocks[diffBlocks.length-1]:diffBlocks[0];
  }else if(team.length>MAX_TEAM){
    const preferHigh=['elite4','champion','kahuna'].includes(trainer.type)
      ||trainer.type==='gym';
    team=trimTeamByLevelCluster(team,trainer.type,preferHigh);
  }
  if(team.length>MAX_TEAM)team=team.slice(0,MAX_TEAM);
  return team;
}

function trimTeamByLevelCluster(team,trainerType,preferHighOverride){
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
  const preferHigh=preferHighOverride!=null
    ?preferHighOverride
    :['elite4','champion','kahuna'].includes(trainerType);
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
  if(tp.name==='jellicent'||tp.name.startsWith('jellicent')){
    if(display.includes('female')){
      p=allPokemon.find(x=>x.name==='jellicent-female');
      if(p)return p;
    }
    p=allPokemon.find(x=>x.name==='jellicent-male');
    if(p)return p;
  }
  return null;
}

// ── Cargar entrenador al lado B ───────────────────────
async function loadTrainer(){
  const slug=document.getElementById('sel-game').value;
  const selTrainer=document.getElementById('sel-trainer');
  const val=selTrainer.value;
  if(!slug||!val)return;

  if(!allPokemon.length||!DB){
    showToast('Espera a que cargue la Pokédex (barra superior).','warn');
    return;
  }

  const sorted=selTrainer._sorted;
  let trainer=findTrainerInSorted(sorted,slug,val);
  if(!trainer){
    showToast('No se encontró el entrenador. Vuelve a elegir juego y rival.','warn');
    return;
  }

  const gameName = document.getElementById('sel-game').options[document.getElementById('sel-game').selectedIndex].text;
  const starterId=document.getElementById('sel-starter').value;
  const rematchEl=document.getElementById('sel-rematch');
  const difficultyEl=document.getElementById('sel-difficulty');
  const rematchSel=isOptionalSelectorActive('rematch')?rematchEl.value:'first';
  const difficulty=isOptionalSelectorActive('difficulty')?difficultyEl.value:'normal';
  const eeveelutionId=isOptionalSelectorActive('eeveelution')
    ?document.getElementById('sel-eeveelution').value:null;
  let resolvedTeam=resolveTrainerTeam(trainer,slug,starterId,difficulty,rematchSel,eeveelutionId);
  if(!resolvedTeam?.length){
    resolvedTeam=(trainer.team||[]).slice();
  }
  if(!resolvedTeam?.length){
    showToast(`El entrenador ${trainer.name} no tiene equipo en los datos.`,'warn');
    return;
  }
  const starterLabel=document.getElementById('sel-starter').selectedOptions[0]?.textContent||'';
  const rematchLabel=isOptionalSelectorActive('rematch')?rematchEl.selectedOptions[0]?.textContent||'':'';
  const diffLabel=isOptionalSelectorActive('difficulty')?difficultyEl.selectedOptions[0]?.textContent||'':'';
  const eeveeLabel=isOptionalSelectorActive('eeveelution')
    ?document.getElementById('sel-eeveelution').selectedOptions[0]?.textContent||'':'';

  document.getElementById('trainer-b-name').textContent = trainer.name || 'Rival';
  const meta=[gameName];
  if(starterLabel)meta.push(`Inicial: ${starterLabel}`);
  if(eeveeLabel)meta.push(`Eevee: ${eeveeLabel}`);
  if(rematchLabel)meta.push(rematchLabel);
  if(diffLabel)meta.push(diffLabel);
  document.getElementById('trainer-b-game').textContent = meta.join(' · ');
  const tnb=document.getElementById('team-name-b'); if(tnb) tnb.value!==undefined ? tnb.value=trainer.name||'Rival' : tnb.textContent=trainer.name||'Rival';

  for(let i=0;i<MAX_TEAM;i++){
    teams.b[i]=null;
    const st=slotSt('b',i);
    st.shiny=false; st.stats=false;
  }

  renderTrainerSprite(trainer, 'b');

  let skipped=0;
  let noMoves=0;
  resolvedTeam.forEach((tp,i)=>{
    if(i>=MAX_TEAM)return;
    const pData=resolveTrainerPokemon(tp);
    if(!pData){ skipped++; return; }

    const level = tp.level || 100;
    const moves = resolveTrainerMoves(pData, tp, slug);
    if(!moves.length)noMoves++;

    const slotTypes=(pData.types&&pData.types.length)?pData.types:(tp.types||[]);
    teams.b[i] = {
      ...pData,
      types:slotTypes,
      moves,
      trainerLevel: level,
    };
    slotSt('b',i).shiny=false;
    slotSt('b',i).stats=false;
  });

  try{
    renderAllSlots('b');
  }catch(e){
    console.error('renderAllSlots b',e);
    showToast('Error al dibujar el equipo rival.','warn');
    return;
  }
  setTimeout(()=>addLevelBadges(), 60);

  const filled=teams.b.filter(Boolean).length;
  const loaded=filled;
  let msg=filled===0
    ? `No se pudo mostrar el equipo de ${trainer.name} (revisa que la Pokédex haya cargado).`
    :skipped
      ? `Equipo de ${trainer.name}: ${filled}/${resolvedTeam.length} en pantalla (${skipped} sin datos en la Pokédex).`
      : `Equipo de ${trainer.name} cargado (${filled} Pokémon).`;
  if(noMoves)msg+=` ${noMoves} sin movimientos en datos.`;
  showToast(msg, (filled===0||skipped||noMoves)?'warn':'ok');
}

window.loadTrainer=loadTrainer;

/** Solo movimientos del JSON (Bulbapedia); sin inventar por nivel. */
function resolveTrainerMoves(pData, tp, gameSlug){
  const raw = tp.moves || [];
  if(!raw.length) return [];

  const gameGen=getGameGen(gameSlug);
  const out = [];
  for(const m of raw.slice(0, 4)){
    const rawName = typeof m === 'string' ? m : m.name;
    if(!rawName) continue;
    const name=normalizeMoveSlug(rawName);
    const fromSlot = pData.allMoves?.find(x => x.name === name);
    const global = DB?.moves?.[name];
    let detail = fromSlot?.detail || global || {
      type: 'normal', category: 'status', power: null, accuracy: null, pp: null,
    };
    if(typeof PokeMoveGenTypes!=='undefined'&&gameGen>0){
      detail=PokeMoveGenTypes.detailForGen(detail,name,gameGen);
    }
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
  return out;
}

function renderTrainerSprite(trainer, team){
  const container = document.getElementById(`slots-${team}`);
  if(!container)return;
  let wrap = document.getElementById('trainer-sprite-block');
  if(wrap) wrap.remove();
  if(!trainer.sprite) return;
  const parent=container.parentElement;
  if(!parent)return;
  wrap = document.createElement('div');
  wrap.id = 'trainer-sprite-block';
  wrap.className = 'trainer-sprite-wrap';
  wrap.innerHTML = `
    <img class="trainer-sprite" src="${trainer.sprite}" alt="${trainer.name}" onerror="this.style.display='none'">
    <div class="trainer-sprite-name">${trainer.name}</div>

    ${trainer.badge?`<div class="trainer-sprite-badge">${trainer.badge}</div>`:''}
  `;
  parent.insertBefore(wrap, container);
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
