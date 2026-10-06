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
const gardenTerrain:Record<string,Terrain>={};
for(let row=0;row<4;row++) gardenTerrain[key(offsetHex(4,row))]=row%2?'rock':'tree';
for(const [col,row] of [[0,0],[1,0],[7,5],[8,5]]) gardenTerrain[key(offsetHex(col,row))]='tree';
const riverTerrain:Record<string,Terrain>={};
for(let row=0;row<7;row++) for(let col=4;col<=6;col++) {
  if((row===1||row===6)&&col!==5) continue;
  riverTerrain[key(offsetHex(col,row))]='water';
}
for(const [col,row] of [[0,0],[1,6],[9,5],[10,6]]) riverTerrain[key(offsetHex(col,row))]='tree';
export const levels:readonly Level[]=[
  {id:'gate',name:'До калитки',cols:7,rows:5,terrain:{[key(offsetHex(0,0))]:'tree',[key(offsetHex(6,4))]:'rock'},
    start:offsetHex(1,2),goal:offsetHex(5,2),startName:'Дом Руты',goalName:'Калитка',
    pieces:[stone('pair','Два камня',pair),stone('single','Камешек',one,'#b080c6')],
    intro:'Вчера здесь была дорожка. Давай вернём её!',outro:'Получилось! Теперь можно выйти к саду.',
    solution:{pair:{anchor:{q:1,r:2},turns:0},single:{anchor:{q:3,r:2},turns:0}}},
  {id:'garden',name:'В обход сада',cols:9,rows:6,terrain:gardenTerrain,
    start:offsetHex(1,2),goal:offsetHex(7,2),startName:'Калитка',goalName:'Сад',
    pieces:[stone('garden-a','Длинная 1',line,'#8465b2'),stone('garden-b','Длинная 2',line,'#ac79ad'),stone('garden-c','Четвёрка',cluster,'#7965a3'),stone('garden-extra','Треугольник',[{q:0,r:0},{q:1,r:0},{q:0,r:1}])],
    intro:'Между деревьями тесно. Попробуем обойти сад?',outro:'Дорога готова! А возле реки тоже не хватает камней…',
    solution:{'garden-a':{anchor:{q:1,r:2},turns:1},'garden-b':{anchor:{q:2,r:4},turns:0},'garden-c':{anchor:{q:5,r:3},turns:0}}},
  {id:'mill',name:'Переправа к мельнице',cols:11,rows:7,terrain:riverTerrain,
    start:offsetHex(1,1),goal:offsetHex(9,1),startName:'Берег',goalName:'Мельница',
    pieces:[{id:'bridge',name:'Мост',kind:'bridge',shape:[{q:0,r:0},{q:-1,r:0},{q:1,r:0}],color:'#bc905e'},stone('mill-a','Уголок 1',bend,'#8465b2'),stone('mill-b','Уголок 2',bend,'#ac79ad'),stone('mill-extra','Камешек',one)],
    intro:'На том берегу мельница. Нам понадобится мост!',outro:'Мельница снова работает! Только куда делись старые камни?',
    solution:{bridge:{anchor:offsetHex(5,1),turns:0},'mill-a':{anchor:{q:2,r:0},turns:0},'mill-b':{anchor:{q:8,r:2},turns:3}}},
];
