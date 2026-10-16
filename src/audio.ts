import manifest from './sound-manifest.json' with {type:'json'};
export type SoundEvent=keyof typeof manifest.events;
export type AudioPreferences={muted:boolean;music:number;sfx:number};
export const AUDIO_PREFERENCES_KEY='ruby-village:audio:v1';
type StorageLike={getItem(key:string):string|null;setItem(key:string,value:string):void};
type Cue={file:string;gain:number;loop:boolean};
type Voice={source:AudioBufferSourceNode;gain:GainNode;kind:'sfx'|'ambience'|'music'};
/** Creates no audio device until unlock is called by a user gesture. No queued one-shots. */
export function createGameAudio(baseUrl:string,storage?:StorageLike) {
 const clamp=(n:unknown,fallback:number)=>typeof n==='number'&&Number.isFinite(n)?Math.min(1,Math.max(0,n)):fallback;
 let preferences:AudioPreferences={muted:false,music:.35,sfx:.65};
 try{const saved=JSON.parse(storage?.getItem(AUDIO_PREFERENCES_KEY)??'null');if(saved)preferences={muted:saved.muted===true,music:clamp(saved.music,.35),sfx:clamp(saved.sfx,.65)};}catch{/* Optional storage. */}
 let context:AudioContext|undefined,buses:Record<'master'|'sfx'|'ambience'|'music',GainNode>|undefined;
 let disposed=false,unlocked=false,paused=false,ducked=false,scene:string|null=null,music:string|null=null;
 let sceneGeneration=0,musicGeneration=0,epoch=0,manualPaused=false,hidden=typeof document!=='undefined'&&document.hidden;
 const voices=new Set<Voice>(),buffers=new Map<string,Promise<AudioBuffer|null>>(),last=new Map<string,number>(),variants=new Map<string,number>();
 const counters={played:0,dropped:0,loadErrors:0};
 const url=(file:string)=>`${baseUrl.replace(/\/?$/,'/')}assets/audio/${file}`;
 function ramp(node:GainNode,value:number,seconds=.15){if(!context)return;node.gain.cancelScheduledValues(context.currentTime);node.gain.setTargetAtTime(value,context.currentTime,seconds);}
 function mix(){if(!buses)return;ramp(buses.master,preferences.muted?0:.7);ramp(buses.sfx,preferences.sfx);ramp(buses.ambience,preferences.sfx*(ducked?.3:1));ramp(buses.music,preferences.music*(ducked?.35:1));}
 function stop(voice:Voice,fade=0){if(!context)return;if(fade)ramp(voice.gain,0,fade/3);try{voice.source.stop(context.currentTime+fade);}catch{}if(!fade){voice.source.disconnect();voice.gain.disconnect();voices.delete(voice);}}
 function stopKind(kind:Voice['kind'],fade=0){const matching=[...voices].filter(v=>v.kind===kind);matching.forEach((voice,index)=>stop(voice,index===matching.length-1?fade:0));}
 async function buffer(file:string){
  if(!context)return null;
  if(!buffers.has(file))buffers.set(file,(async()=>{try{const response=await fetch(url(file));if(!response.ok)throw Error('audio fetch');return await context!.decodeAudioData(await response.arrayBuffer());}catch{counters.loadErrors++;return null;}})());
  return buffers.get(file)!;
 }
 function start(data:AudioBuffer,kind:Voice['kind'],gain:number,loop=false,fade=false){
  if(!context||!buses||disposed||paused||!unlocked)return;
  const source=context.createBufferSource(),node=context.createGain();source.buffer=data;source.loop=loop;source.connect(node);node.connect(buses[kind]);node.gain.value=fade?0:gain;
  const voice={source,gain:node,kind};voices.add(voice);
  source.onended=()=>{source.disconnect();node.disconnect();voices.delete(voice);};
  if(fade)ramp(node,gain,.25);source.start();counters.played++;
 }
 async function ambience(){const generation=++sceneGeneration;if(!unlocked||paused||!scene||disposed)return;
  const item=(manifest.ambiences as Record<string,Cue>)[scene];if(!item){stopKind('ambience',.3);return;}
  const data=await buffer(`sfx/${item.file}`);if(generation!==sceneGeneration||paused||disposed)return;
  stopKind('ambience',.6);if(data)start(data,'ambience',item.gain,true,true);
 }
 let musicManifest:Promise<Record<string,Cue>>|undefined;
 async function musicLoop(){const generation=++musicGeneration;if(!unlocked||paused||!music||disposed)return;
  const cueName=music;
  musicManifest??=(async()=>{try{const response=await fetch(url('music/manifest.json'));if(!response.ok)throw Error('music manifest');const data=await response.json();return data.cues??{};}catch{counters.loadErrors++;return {};}})();
  const item=(await musicManifest)[cueName];if(generation!==musicGeneration||paused||disposed)return;
  if(!item){stopKind('music',.4);return;}
  const data=await buffer(`music/${item.file}`);if(generation!==musicGeneration||paused||disposed)return;
  stopKind('music',.7);if(data)start(data,'music',clamp(item.gain,.6),item.loop!==false,true);
 }
 async function unlock(){
  if(disposed)return false;
  try{
   if(!context){context=new AudioContext();const master=context.createGain(),sfx=context.createGain(),ambience=context.createGain(),music=context.createGain();buses={master,sfx,ambience,music};master.gain.value=0;master.connect(context.destination);sfx.connect(master);ambience.connect(master);music.connect(master);mix();}
   await context.resume();if(disposed)return false;const first=!unlocked;unlocked=context.state==='running';
   if(unlocked&&first){void ambience();void musicLoop();}return unlocked;
  }catch{counters.loadErrors++;return false;}
 }
 async function play(event:SoundEvent){
  if(!unlocked||disposed||paused||preferences.muted||!context||context.state!=='running'){counters.dropped++;return;}
  const item=manifest.events[event];if(!item)return;
  const now=context.currentTime*1000,previous=last.get(event)??-Infinity;
  if(now-previous<item.minIntervalMs||[...voices].filter(v=>v.kind==='sfx').length>=8){counters.dropped++;return;}
  last.set(event,now);const turn=variants.get(event)??0;variants.set(event,turn+1);const generation=epoch;
  const data=await buffer(`sfx/${item.variants[turn%item.variants.length]}`);
  // Loading is not a sound queue: never release stale footsteps after a scene/pause change.
  if(!data||generation!==epoch||paused||disposed||preferences.muted||!context||context.currentTime*1000-now>400){counters.dropped++;return;}
  if([...voices].filter(v=>v.kind==='sfx').length>=8){counters.dropped++;return;}
  start(data,'sfx',item.gain);
 }
 function applyPause(){const value=manualPaused||hidden;if(paused===value)return;paused=value;epoch++;sceneGeneration++;musicGeneration++;if(value){for(const voice of voices)stop(voice);}else{void ambience();void musicLoop();}}
 function setScene(value:string|null){if(scene===value)return;scene=value;epoch++;stopKind('sfx');if(!value){sceneGeneration++;stopKind('ambience',.4);}else void ambience();}
 function setMusic(value:string|null){if(music===value)return;music=value;if(!value){musicGeneration++;stopKind('music',.4);}else void musicLoop();}
 function setPreferences(patch:Partial<AudioPreferences>){preferences={muted:typeof patch.muted==='boolean'?patch.muted:preferences.muted,music:clamp(patch.music,preferences.music),sfx:clamp(patch.sfx,preferences.sfx)};try{storage?.setItem(AUDIO_PREFERENCES_KEY,JSON.stringify(preferences));}catch{}mix();}
 function setPaused(value:boolean){manualPaused=value;applyPause();}
 function visibility(){hidden=document.hidden;applyPause();}
 if(typeof document!=='undefined')document.addEventListener('visibilitychange',visibility);
 applyPause();
 return {unlock,play,setScene,setMusic,setPaused,setDucked(value:boolean){ducked=value;mix();},setPreferences,
  get preferences(){return {...preferences};},get metrics(){return {...counters,activeVoices:voices.size,cachedFiles:buffers.size,unlocked,paused,contextState:context?.state??'not-created'};},
  dispose(){if(disposed)return;disposed=true;epoch++;sceneGeneration++;musicGeneration++;for(const voice of voices)stop(voice);if(typeof document!=='undefined')document.removeEventListener('visibilitychange',visibility);void context?.close().catch(()=>{});buffers.clear();}
 };
}
