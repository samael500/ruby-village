import {levels} from '../src/levels.ts';
import {boardCells,key,neighbors} from '../src/hex.ts';
import {validPlacement,placedCells,winningPath,type Layout} from '../src/game.ts';
const result:any={};
for(const l of levels){
 const candidates=l.pieces.map(p=>boardCells(l.cols,l.rows).flatMap(anchor=>Array.from({length:6},(_,turns)=>({anchor,turns}))).filter(x=>validPlacement(l,p.id,x,{})));
 let visits=0;const seen=new Set<string>();
 const distance=(h:any)=>Math.max(Math.abs(h.q-l.goal.q),Math.abs(h.r-l.goal.r),Math.abs(h.q+h.r-l.goal.q-l.goal.r));
 function dfs(layout:Layout,used:Set<number>):Layout|null{
  if(winningPath(l,layout))return layout;
  if(++visits>500000)return null;
  const paved=new Set([key(l.start),...Object.entries(layout).flatMap(([id,p])=>placedCells(id,p,l.pieces).map(key))]);
  const hash=[...paved].sort().join('|')+';'+[...used].sort().join(',');if(seen.has(hash))return null;seen.add(hash);
  const next:any[]=[];
  for(let i=0;i<l.pieces.length;i++)if(!used.has(i))for(const p of candidates[i]){
   if(!validPlacement(l,l.pieces[i].id,p,layout))continue;
   const cells=placedCells(l.pieces[i].id,p,l.pieces);
   if(cells.some(h=>neighbors(h).some(n=>paved.has(key(n)))))next.push({i,p,rank:Math.min(...cells.map(distance))});
  }
  next.sort((a,b)=>a.rank-b.rank);
  for(const {i,p} of next){const x=dfs({...layout,[l.pieces[i].id]:p},new Set([...used,i]));if(x)return x;}
  return null;
 }
 const solution=dfs({},new Set());console.error(l.id,visits,!!solution);if(!solution)throw Error(l.id);result[l.id]=solution;
}
console.log(JSON.stringify(result,null,2));
