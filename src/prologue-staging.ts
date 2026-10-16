import {prologueFrames} from './prologue.ts';
/** Semantic anchors resolve through the scene manifest, never independent screen coordinates. */
export const prologueStaging=[
 {scene:'gate',camera:'wide',actors:[{id:'ruta',pose:'basket-hold',anchor:'start'}],props:['basket-apples'],road:'intact',next:'Дальше'},
 {scene:'gate',camera:'wide',actors:[{id:'ruta',pose:'basket-hold',anchor:'start'}],props:['basket-apples'],road:'intact',next:'Дальше'},
 {scene:'garden',camera:'wide',actors:[{id:'rabbit',pose:'baking',anchor:'goal'}],props:['table','bowl','spoon'],road:'hidden',next:'Дальше'},
 {scene:'gate',camera:'wide',actors:[{id:'ruta',pose:'surprised',anchor:'start'}],props:['basket-apples','loose-stones'],road:'missing',next:'Дальше'},
 {scene:'gate',camera:'wide',actors:[{id:'ruta',pose:'crouch',anchor:'loose-stone'}],props:['basket-ground','loose-stones'],road:'missing',next:'Дальше'},
 {scene:'gate',camera:'gameplay',actors:[{id:'ruta',pose:'idle',anchor:'start'}],props:['basket-ground','loose-stones'],road:'missing',next:'К калитке'}
] as const;
export function stagedPrologueFrame(index:number) {
 if(!Number.isInteger(index)||index<0||index>=prologueFrames.length)throw new RangeError('Invalid prologue frame');
 return {...prologueFrames[index],staging:prologueStaging[index],showPuzzleUI:false,backDisabled:index===0};
}
