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
  return TRAINERS_DB?.games?.find(g=>g.slug===slug)?.gen||0;
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
  return!!getEmbeddedRematchBlocks(trainer.team||[]);
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

function setRematchSelectorVisible(show){
  const group=document.getElementById('sel-rematch-group');
  const arrow=document.getElementById('arrow-before-rematch');
  const sel=document.getElementById('sel-rematch');
  if(group)group.hidden=!show;
  if(arrow)arrow.hidden=!show;
  if(sel)sel.disabled=!show;
}

function setDifficultySelectorVisible(show){
  const group=document.getElementById('sel-difficulty-group');
  const arrow=document.getElementById('arrow-before-difficulty');
  const sel=document.getElementById('sel-difficulty');
  if(group)group.hidden=!show;
  if(arrow)arrow.hidden=!show;
  if(sel)sel.disabled=!show;
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

/** Revancha y dificultad por separado: solo los que apliquen al entrenador. */
function buildTrainerOptionSelectors(slug,trainer){
  resetRematchSelector();
  resetDifficultySelector();
  if(!trainer||!slug)return;
  if(trainerHasRematchVariants(trainer,slug))buildRematchSelector(slug,trainer);
  if(trainerHasDifficultyVariants(trainer,slug))buildDifficultySelector(slug,trainer);
}

function updateLoadTrainerButton(){
  const slug=document.getElementById('sel-game').value;
  const trainerVal=document.getElementById('sel-trainer').value;
  const starterEl=document.getElementById('sel-starter');
  const gen=getGameGen(slug);
  const needsStarter=!!slug&&!!GEN_STARTERS[gen];
  const starterOk=!needsStarter||!!starterEl.value;
  const trainerOk=!!trainerVal&&(useApi()||!isNaN(parseInt(trainerVal)));
  document.getElementById('btn-load-trainer').disabled=!(slug&&trainerOk&&starterOk);
}

function normalizeTrainerFromApi(t){
  return{
    id:t.id,
    slug:t.slug,
    name:t.name,
    type:t.type,
    order:t.order,
    location:t.location||'',
    badge:t.badge||'',
    specialty:t.specialty||'',
    sprite:t.sprite,
    team:(t.team||[]).map(m=>({
      name:m.name,
      name_display:m.name_es||formatName(m.name),
      level:m.level,
      types:m.types_en||m.types||[],
      moves:(m.moves||[]).map(mv=>({
        name:mv.name,
        name_display:mv.name_es||mv.name_display||formatName(mv.name),
      })),
    })),
  };
}

async function loadTrainersForGame(slug){
  if(!slug)return[];
  if(useApi()){
    const list=await fetchApi(`/trainers?game_slug=${encodeURIComponent(slug)}&include_team=1`);
    const normalized=list.map(normalizeTrainerFromApi);
    if(!TRAINERS_DB.trainers)TRAINERS_DB.trainers={};
    TRAINERS_DB.trainers[slug]=normalized;
    return normalized;
  }
  return TRAINERS_DB.trainers[slug]||[];
}

// ── Carga de datos ────────────────────────────────────
async function initTrainers(){
  IS_TRAINER_PAGE=true;
  let tries=0;
  while((!DB||!allPokemon.length)&&tries<50){
    await new Promise(r=>setTimeout(r,200));
    tries++;
  }

  try{
    const apiOk=typeof checkApiAvailable==='function'&&await checkApiAvailable();
    if(apiOk){
      const [games,stats]=await Promise.all([
        fetchApi('/games'),
        fetchApi('/stats').catch(()=>({})),
      ]);
      TRAINERS_DB={
        games:games.map(g=>({slug:g.slug,name:g.name,gen:g.gen,region:g.region})),
        trainers:{},
        meta:{total_trainers:stats.trainers||287},
      };
      setTrainersDataSource('api', getApiBase() + '/trainers'); // POKEWEB-TEMP-DATA-SOURCE-INDICATOR
    }else{
      const res=await fetch('data/trainers_db.json');
      if(!res.ok)throw new Error('No trainers DB');
      TRAINERS_DB=await res.json();
      setTrainersDataSource('json','data/trainers_db.json'); // POKEWEB-TEMP-DATA-SOURCE-INDICATOR
    }
    buildGameSelector();
    resetStarterSelector();
    resetRematchSelector();
    resetDifficultySelector();
    document.getElementById('status-bar').innerHTML=
      `<img src="img/favicon.png" style="height:1.2em;vertical-align:middle;margin-right:5px">
       <span>${allPokemon.length} Pokémon · ${TRAINERS_DB.meta?.total_trainers||'?'} entrenadores</span>`;
    if(typeof updateDataSourceUI==='function')updateDataSourceUI(['pokemon','trainers']); // POKEWEB-TEMP-DATA-SOURCE-INDICATOR
  }catch(e){
    setTrainersDataSource('none','Error al cargar entrenadores'); // POKEWEB-TEMP-DATA-SOURCE-INDICATOR
    document.getElementById('status-bar').textContent='Sin DB de entrenadores (Flask + import_db.py).';
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

function populateTrainerSelect(trainers,sorted){
  const selTrainer=document.getElementById('sel-trainer');
  const slug=document.getElementById('sel-game').value;
  selTrainer.innerHTML='<option value="">— Entrenador —</option>';
  let lastType='';
  sorted.forEach((t,i)=>{
    const typeLabel={gym:'🏟 Líder',kahuna:'🌺 Kahuna',captain:'🏝 Capitán',elite4:'🏆 Alto Mando',champion:'👑 Campeón',other:'⚔ Otro'}[t.type]||'';
    if(t.type!==lastType){
      const og=document.createElement('optgroup');
      og.label={gym:'── Líderes de Gimnasio ──',kahuna:'── Kahunas ──',captain:'── Capitanes ──',elite4:'── Alto Mando ──',champion:'── Campeón ──',other:'── Otros ──'}[t.type]||t.type;
      selTrainer.appendChild(og);
      lastType=t.type;
    }
    const opt=document.createElement('option');
    opt.value=useApi()&&t.slug?t.slug:String(i);
    opt.textContent=`${typeLabel} ${t.name}${t.location?' — '+t.location:''}`;
    selTrainer.appendChild(opt);
  });
  selTrainer.disabled=false;
  selTrainer.value='';
  selTrainer._sorted=sorted;
  selTrainer.onchange=()=>{
    const val=selTrainer.value;
    let tr=null;
    if(useApi()&&val)tr=sorted.find(x=>x.slug===val);
    else{
      const idx=parseInt(val);
      tr=!isNaN(idx)?sorted[idx]:null;
    }
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
    return;
  }

  buildStarterSelector(slug);
  resetRematchSelector();
  resetDifficultySelector();

  selTrainer.disabled=true;
  selTrainer.innerHTML='<option value="">Cargando entrenadores…</option>';

  let trainers=[];
  try{
    trainers=await loadTrainersForGame(slug);
  }catch(e){
    selTrainer.innerHTML='<option value="">Error al cargar</option>';
    return;
  }

  const sorted=[...trainers].sort((a,b)=>{
    const typeOrder={gym:0,kahuna:0,elite4:1,champion:2,captain:3,other:4};
    const ta=typeOrder[a.type]??4,tb=typeOrder[b.type]??4;
    if(ta!==tb)return ta-tb;
    return(a.order||0)-(b.order||0);
  });

  populateTrainerSelect(trainers,sorted);
  updateLoadTrainerButton();
}

function applyStarterFilters(team,trainer,slug,starterId){
  const gen=getGameGen(slug);
  const finals=STARTER_FINALS_BY_GEN[gen]||[];
  const keepFinal=RIVAL_COUNTER_BY_GEN[gen]?.[starterId];
  const finalsInTeam=finals.filter(f=>team.some(p=>p.name===f));

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
  return team;
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
function resolveTrainerTeam(trainer, slug, starterId, difficulty, rematchSel){
  const peer=getRematchPeer(trainer,slug);
  let team;

  if(rematchSel==='rematch'&&peer){
    team=[...(peer.team||[])];
  }else if(rematchSel==='rematch'){
    const embedded=getEmbeddedRematchBlocks(trainer.team||[]);
    team=embedded?embedded[embedded.length-1]:[...(trainer.team||[])];
  }else if(peer&&!isRematchEntry(trainer)){
    team=[...(trainer.team||[])];
  }else{
    const embedded=getEmbeddedRematchBlocks(trainer.team||[]);
    team=embedded?embedded[0]:[...(trainer.team||[])];
  }

  team=collapseDuplicatedRoster(team);
  team=applyStarterFilters(team,trainer,slug,starterId);

  if(trainerHasDifficultyVariants({team},slug)){
    const diffBlocks=splitDifficultyBlocks(team);
    const wantChallenge=difficulty==='challenge';
    team=wantChallenge?diffBlocks[diffBlocks.length-1]:diffBlocks[0];
  }else if(team.length>MAX_TEAM){
    team=trimTeamByLevelCluster(team,trainer.type,false);
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
function loadTrainer(){
  const slug=document.getElementById('sel-game').value;
  const selTrainer=document.getElementById('sel-trainer');
  const val=selTrainer.value;
  if(!slug||!val)return;

  const sorted=selTrainer._sorted;
  let trainer=null;
  if(useApi())trainer=sorted?.find(t=>t.slug===val);
  else{
    const idx=parseInt(val);
    if(!isNaN(idx))trainer=sorted[idx];
  }
  if(!trainer)return;

  const gameName = document.getElementById('sel-game').options[document.getElementById('sel-game').selectedIndex].text;
  const starterId=document.getElementById('sel-starter').value;
  const rematchEl=document.getElementById('sel-rematch');
  const difficultyEl=document.getElementById('sel-difficulty');
  const rematchSel=(!rematchEl.disabled&&rematchEl.value)||'first';
  const difficulty=(!difficultyEl.disabled&&difficultyEl.value)||'normal';
  const resolvedTeam=resolveTrainerTeam(trainer,slug,starterId,difficulty,rematchSel);
  const starterLabel=document.getElementById('sel-starter').selectedOptions[0]?.textContent||'';
  const rematchLabel=rematchEl.disabled?'':rematchEl.selectedOptions[0]?.textContent||'';
  const diffLabel=difficultyEl.disabled?'':difficultyEl.selectedOptions[0]?.textContent||'';

  document.getElementById('trainer-b-name').textContent = trainer.name || 'Rival';
  const meta=[gameName];
  if(starterLabel)meta.push(`Inicial: ${starterLabel}`);
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
    const moves = resolveTrainerMoves(pData, tp);
    if(!moves.length)noMoves++;

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
  let msg=skipped
    ? `Equipo de ${trainer.name}: ${loaded}/${resolvedTeam.length} Pokémon (${skipped} sin datos en la DB).`
    : `Equipo de ${trainer.name} cargado (${loaded} Pokémon).`;
  if(noMoves)msg+=` ${noMoves} sin movimientos en datos (ejecuta enrich_moves.py).`;
  showToast(msg, (skipped||noMoves)?'warn':'ok');
}

/** Solo movimientos del JSON (Bulbapedia); sin inventar por nivel. */
function resolveTrainerMoves(pData, tp){
  const raw = tp.moves || [];
  if(!raw.length) return [];

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
  return out;
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
