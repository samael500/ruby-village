import {storyFor} from './story.ts';
import {key,offsetHex} from './hex.ts';
import type {Level,Piece,Terrain} from './model.ts';
const one=[{q:0,r:0}];
const pair=[{q:0,r:0},{q:1,r:0}];
const line=[{q:0,r:0},{q:1,r:0},{q:2,r:0}];
const bend=[{q:0,r:0},{q:1,r:0},{q:1,r:1}];
const cluster=[{q:0,r:0},{q:1,r:0},{q:0,r:1},{q:-1,r:2}];
const stone=(id:string,name:string,shape:Piece['shape'],color='#9873bf'):Piece=>({id,name,shape,color});
export const sandboxPieces:readonly Piece[]=[
  stone('one-a','Камешек 1',one),stone('one-b','Камешек 2',one,'#b080c6'),
  stone('line','Три в ряд',line,'#8465b2'),stone('bend','Уголок',bend,'#ac79ad'),stone('cluster','Четвёрка',cluster,'#7965a3'),
];
export function sandbox(cols=9,rows=6):Level {
  return {id:'sandbox',name:'Песочница',cols,rows,terrain:{},start:offsetHex(0,Math.floor(rows/2)),goal:offsetHex(cols-1,Math.floor(rows/2)),startName:'Деревня',goalName:'Мельница',pieces:sandboxPieces,intro:'Выбери плиту, затем клетку.',outro:'Дорога готова!',solution:{}};
}
const river=():Record<string,Terrain>=>Object.fromEntries(Array.from({length:7},(_,r)=>[key(offsetHex(5,r)),'water']));
const wall=(col:number,rows:number[],kind:Terrain):Record<string,Terrain>=>Object.fromEntries(rows.map(r=>[key(offsetHex(col,r)),kind]));
const bridge:Piece={id:'bridge',name:'Мост',kind:'bridge',shape:[{q:0,r:0},{q:-1,r:0},{q:1,r:0}],color:'#bc905e'};
const at=(q:number,r:number,turns=0)=>({anchor:{q,r},turns});
const define=(data:Omit<Level,'name'|'intro'|'outro'>):Level=>{
 const story=storyFor(data.id)!;
 return {...data,name:story.title,intro:story.before.map(d=>`${d.speaker}: ${d.text}`).join('\n'),outro:story.after.map(d=>`${d.speaker}: ${d.text}`).join('\n')};
};
export const levels:readonly Level[]=[
 define({id:'gate',cols:7,rows:5,terrain:{'0,0':'house','1,0':'house'},start:offsetHex(0,1),goal:offsetHex(6,4),startName:'Дом Руты',goalName:'Калитка',
 pieces:Array.from({length:6},(_,i)=>stone(`gate-${i+1}`,`Камень ${i+1}`,one)),
 solution:{'gate-1':at(1,1),'gate-2':at(2,1),'gate-3':at(2,2),'gate-4':at(2,3),'gate-5':at(3,3),'gate-6':at(3,4)}}),
 define({id:'garden',cols:11,rows:7,terrain:wall(4,[0,1,2,3],'tree'),start:{q:0,r:3},goal:{q:6,r:3},startName:'Калитка',goalName:'Стол',
 pieces:[stone('garden-a','Три камня',[{q:0,r:0},{q:0,r:1},{q:0,r:2}]),stone('garden-b','Два камня',pair),stone('garden-c','Камешек',one)],
 solution:{'garden-a':at(0,4,5),'garden-b':at(3,4),'garden-c':at(5,3)}}),
 define({id:'well',cols:11,rows:7,terrain:wall(5,[2,3,4],'flower'),start:{q:1,r:3},goal:{q:7,r:3},startName:'Площадь',goalName:'Колодец',
 pieces:[stone('well-a','Уголок',bend),stone('well-b','Два камня 1',pair),stone('well-c','Два камня 2',pair)],
 solution:{'well-a':at(2,2,5),'well-b':at(5,1),'well-c':at(6,2)}}),
 define({id:'bakery',cols:11,rows:7,terrain:{'3,2':'rock','3,1':'flower','7,5':'tree'},start:{q:0,r:2},goal:{q:7,r:2},startName:'Двор',goalName:'Пекарня',
 pieces:[stone('bakery-a','Уголок',bend),stone('bakery-b','Три в ряд',line),stone('bakery-c','Камешек',one)],
 solution:{'bakery-a':at(1,2),'bakery-b':at(3,3),'bakery-c':at(6,2)}}),
 define({id:'stream',cols:11,rows:7,terrain:river(),start:{q:0,r:3},goal:{q:8,r:3},startName:'Берег',goalName:'За ручьём',
 pieces:[stone('stream-a','Два камня 1',pair),bridge,stone('stream-b','Два камня 2',pair)],
 solution:{'stream-a':at(1,3),bridge:at(4,3),'stream-b':at(6,3)}}),
 define({id:'mill',cols:11,rows:7,terrain:river(),start:{q:0,r:1},goal:{q:8,r:3},startName:'Ручей',goalName:'Мельница',
 pieces:[stone('mill-a','Уголок',bend),stone('mill-b','Камешек',one),bridge,stone('mill-c','Два камня',pair)],
 solution:{'mill-a':at(1,1),'mill-b':at(3,2),bridge:at(4,3),'mill-c':at(6,3)}}),
 define({id:'post',cols:11,rows:7,terrain:{'3,2':'flower','4,1':'tree','5,1':'tree','2,5':'rock'},start:{q:0,r:2},goal:{q:7,r:2},startName:'Двор',goalName:'Почта',
 pieces:[stone('post-a','Уголок',bend),stone('post-b','Три в ряд',line),stone('post-c','Камешек',one),stone('post-extra','Два камня',pair)],
 solution:{'post-a':at(1,2),'post-b':at(3,3),'post-c':at(6,2)}}),
 define({id:'forest',cols:11,rows:7,terrain:{...river(),'0,1':'tree','1,1':'tree','7,0':'tree','8,0':'tree'},start:{q:0,r:4},goal:{q:8,r:2},startName:'Деревня',goalName:'Указатель',
 pieces:[stone('forest-a','Четвёрка',cluster),bridge,stone('forest-b','Три в ряд',line)],
 solution:{'forest-a':at(1,3),bridge:at(4,3),'forest-b':at(6,3)}}),
];
// A second independently checked route around the flowerbed. No unique-solution claim.
export const wellAlternative={'well-a':at(2,5,3),'well-b':at(3,5),'well-c':at(5,4)};
