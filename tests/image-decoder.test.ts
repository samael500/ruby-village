import {test} from 'node:test';
import assert from 'node:assert/strict';
import {createImageDecoder} from '../src/image-decoder.ts';

test('transient atlas failure can retry; concurrent and successful loads are shared',async()=>{
 let attempts=0,resolve!:()=>void,reject!:(e:Error)=>void;
 const made:{src:string;decode:()=>Promise<void>}[]=[];
 const decoded=createImageDecoder('/ruby-village/',()=>{
  attempts++;const promise=new Promise<void>((yes,no)=>{resolve=yes;reject=no;});
  const image={src:'',decode:()=>promise};made.push(image);return image as HTMLImageElement;
 });
 const a=decoded('atlas.webp'),b=decoded('atlas.webp');
 assert.equal(a,b);assert.equal(attempts,1);
 const failed=assert.rejects(a,/temporary network failure/);
 reject(new Error('temporary network failure'));await failed;
 const retry=decoded('atlas.webp');assert.notEqual(retry,a);assert.equal(attempts,2);
 assert.equal(decoded('atlas.webp'),retry);resolve();
 assert.equal(await retry,made[1]);assert.equal(made[1].src,'/ruby-village/atlas.webp');
 assert.equal(await decoded('atlas.webp'),made[1]);assert.equal(attempts,2);
});
