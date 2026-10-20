const activated=new Set<number>();
let installed=false;
let lastPointer:{id:number;type:string}|null=null;
/** A deliberate touch release activates once, even if Chromium omits its
 * compatibility click after dragging. Mouse and keyboard keep native clicks. */
export function activateTouchRelease(button:HTMLButtonElement){
 if(!installed){
  installed=true;
  document.addEventListener('pointerdown',event=>{lastPointer={id:event.pointerId,type:event.pointerType};activated.delete(event.pointerId);},true);
  // A control may hide or move after activation. Suppress the matching native
  // click before it can be retargeted to another control in the changed dock.
  document.addEventListener('click',event=>{
   const pointer=event instanceof PointerEvent&&event.pointerType?{id:event.pointerId,type:event.pointerType}:lastPointer;
   if(event.isTrusted&&event.detail>0&&pointer?.type==='touch'&&activated.has(pointer.id)){
    activated.delete(pointer.id);event.preventDefault();event.stopImmediatePropagation();
   }
  },true);
 }
 let press:{id:number;x:number;y:number}|null=null;
 button.addEventListener('pointerdown',event=>{
  if(event.pointerType==='touch'&&event.isPrimary&&!button.disabled)press={id:event.pointerId,x:event.clientX,y:event.clientY};
 });
 button.addEventListener('pointercancel',()=>{press=null;});
 button.addEventListener('pointermove',event=>{if(press&&event.pointerId===press.id&&Math.hypot(event.clientX-press.x,event.clientY-press.y)>8)press=null;});
 button.addEventListener('pointerup',event=>{
  const start=press;press=null;
  if(!start||start.id!==event.pointerId||event.pointerType!=='touch'||button.disabled||Math.hypot(event.clientX-start.x,event.clientY-start.y)>8)return;
  const bounds=button.getBoundingClientRect();
  if(event.clientX<bounds.left||event.clientX>bounds.right||event.clientY<bounds.top||event.clientY>bounds.bottom)return;
  activated.add(event.pointerId);
  if(activated.size>64)activated.delete(activated.values().next().value!);
  button.click();
 });
}
