def ready_images(page):
 page.evaluate('''async () => {
  await Promise.all([...document.querySelectorAll('img')].map(img=>img.decode()));
  await Promise.all([...document.querySelectorAll('svg image')].map(el=>{const img=new Image();img.src=el.getAttribute('href');return img.decode()}));
  await Promise.all([...document.querySelectorAll('*')].flatMap(el=>[...getComputedStyle(el).backgroundImage.matchAll(/url\\("?([^"\\)]+)"?\\)/g)].map(m=>{const img=new Image();img.src=m[1];return img.decode()})));
  await new Promise(resolve=>requestAnimationFrame(()=>requestAnimationFrame(resolve)));
 }''')
def screenshot(page,path):
 ready_images(page)
 page.screenshot(path=str(path))
