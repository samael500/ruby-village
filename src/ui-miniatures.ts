/** Decorative chapter illustrations, cropped from the accepted painted map.
 * Coordinates are in map-base.webp's original 1000×400 canvas, not game cells.
 * Keep the text label in the caller: the illustration repeats no accessible name.
 */
const ns = 'http://www.w3.org/2000/svg';
const landmarks: Record<string, readonly [number, number, number, number]> = {
  gate: [18, 6, 220, 165],
  garden: [263, 0, 215, 163],
  well: [509, 17, 194, 146],
  bakery: [747, 3, 218, 164],
  stream: [718, 218, 276, 174],
  mill: [497, 177, 221, 166],
  post: [268, 177, 220, 165],
  forest: [0, 163, 235, 177],
};

function element(tag: string, attrs: Record<string, string>, parent?: Element) {
  const node = document.createElementNS(ns, tag);
  for (const [key, value] of Object.entries(attrs)) node.setAttribute(key, value);
  parent?.append(node);
  return node;
}

function frame(host: HTMLElement, kind: string) {
  const svg = element('svg', {
    viewBox: '0 0 64 52', width: '64', height: '52',
    'aria-hidden': 'true', focusable: 'false', 'data-painted-miniature': kind,
    style: 'display:block;width:100%;height:100%;overflow:visible',
  });
  element('path', {d: 'M5 3 Q30 0 59 3 L61 47 Q33 52 3 48 Z', fill: '#6a4430', opacity: '.25', transform: 'translate(0 1)'}, svg);
  element('path', {d: 'M5 2 Q31 0 59 3 L61 47 Q33 51 3 48 Z', fill: '#f4e4b9', stroke: '#b78c50', 'stroke-width': '.8'}, svg);
  host.replaceChildren(svg);
  return svg;
}

export function renderLevelMiniature(host: HTMLElement, levelId: string): void {
  const crop = landmarks[levelId] ?? landmarks.gate;
  const svg = frame(host, levelId);
  // A nested SVG clips the image to this small window without document-global IDs.
  const viewport = element('svg', {
    x: '5', y: '4', width: '54', height: '43',
    viewBox: crop.join(' '), preserveAspectRatio: 'xMidYMid slice', overflow: 'hidden',
  }, svg);
  element('image', {
    href: `${import.meta.env.BASE_URL}assets/chapter-map-v2/map-base.webp`,
    x: '0', y: '0', width: '1000', height: '400',
  }, viewport);
  element('path', {d: 'M5 4 H59 V47 H5 Z', fill: 'none', stroke: '#8e744b', 'stroke-width': '.65'}, svg);
}

export function renderAdventureMiniature(host: HTMLElement, kind: 'ending' | 'letter'): void {
  if (kind === 'ending') {
    renderLevelMiniature(host, 'forest');
    host.firstElementChild?.setAttribute('data-painted-miniature', 'ending');
    return;
  }
  const svg = frame(host, 'letter');
  element('path', {d: 'M10 13 Q32 8 54 12 L56 40 Q34 45 10 41 Z', fill: '#805b39', opacity: '.22', transform: 'translate(0 2)'}, svg);
  element('path', {d: 'M10 12 Q32 7 54 11 L56 39 Q34 44 10 40 Z', fill: '#edcf92', stroke: '#987443', 'stroke-width': '1'}, svg);
  element('path', {d: 'M11 13 L32 30 L53 12 M11 39 L25 26 M55 39 L39 26', fill: 'none', stroke: '#ad8752', 'stroke-width': '1'}, svg);
  element('path', {d: 'M11 12 Q32 8 53 11 L32 29 Z', fill: '#fae6b5', stroke: '#b6925e', 'stroke-width': '.7'}, svg);
  element('path', {d: 'M28 26 Q31 23 35 25 L38 29 L36 34 L30 35 L26 31 Z', fill: '#9d3344', stroke: '#682738', 'stroke-width': '.7'}, svg);
  element('path', {d: 'M32 27 L35 30 L32 33 L29 30 Z', fill: '#de8790', stroke: '#f3b8a0', 'stroke-width': '.5'}, svg);
  element('path', {d: 'M29 26 L31 25 M27 30 L28 32', fill: 'none', stroke: '#f5b8a4', 'stroke-width': '.6', 'stroke-linecap': 'round'}, svg);
}
