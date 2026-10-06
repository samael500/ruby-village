export type Hex = { q: number; r: number };
export const key = (h: Hex) => `${h.q},${h.r}`;
export const add = (a: Hex, b: Hex): Hex => ({ q: a.q + b.q, r: a.r + b.r });
export const directions: readonly Hex[] = [{q:1,r:0},{q:1,r:-1},{q:0,r:-1},{q:-1,r:0},{q:-1,r:1},{q:0,r:1}];
export const neighbors = (h: Hex) => directions.map(d => add(h, d));
export function rotate(h: Hex, turns: number): Hex {
  let {q, r} = h;
  for (let i = 0; i < ((turns % 6) + 6) % 6; i++) [q, r] = [-r, q + r];
  return {q: q || 0, r: r || 0};
}
export const offsetHex = (col: number, row: number): Hex => ({q: col - Math.floor(row / 2), r: row});
export function boardCells(cols: number, rows: number): Hex[] {
  return Array.from({length: cols * rows}, (_, i) => offsetHex(i % cols, Math.floor(i / cols)));
}
export const footprint = (shape: readonly Hex[], anchor: Hex, turns: number) => shape.map(h => add(anchor, rotate(h, turns)));
export function canPlace(cells: readonly Hex[], board: ReadonlySet<string>, occupied: ReadonlySet<string>): boolean {
  return cells.length > 0 && new Set(cells.map(key)).size === cells.length && cells.every(h => board.has(key(h)) && !occupied.has(key(h)));
}
export function findPath(start: Hex, end: Hex, paved: ReadonlySet<string>): Hex[] | null {
  const allowed = new Set([...paved, key(start), key(end)]);
  const queue = [start];
  const previous = new Map<string, Hex | null>([[key(start), null]]);
  for (let i = 0; i < queue.length; i++) {
    const h = queue[i];
    if (key(h) === key(end)) {
      const path: Hex[] = [];
      let cursor: Hex | null = h;
      while (cursor) { path.push(cursor); cursor = previous.get(key(cursor)) ?? null; }
      return path.reverse();
    }
    for (const n of neighbors(h)) if (allowed.has(key(n)) && !previous.has(key(n))) {
      previous.set(key(n), h); queue.push(n);
    }
  }
  return null;
}
export const hexCenter = (h: Hex, radius: number) => ({x: Math.sqrt(3) * radius * (h.q + h.r / 2), y: 1.5 * radius * h.r});
export function pixelHex(x: number, y: number, radius: number): Hex {
  const q = (Math.sqrt(3) / 3 * x - y / 3) / radius, r = 2 / 3 * y / radius;
  let rx = Math.round(q), rz = Math.round(r);
  const ry = Math.round(-q-r), dx = Math.abs(rx-q), dy = Math.abs(ry+q+r), dz = Math.abs(rz-r);
  if (dx > dy && dx > dz) rx = -ry-rz;
  else if (dz > dy) rz = -rx-ry;
  return {q:rx || 0,r:rz || 0};
}
