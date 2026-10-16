/** Screen-space directions: derive these from the projected route, never hex indices. */
export type Direction = 'e' | 'se' | 'sw' | 'w' | 'nw' | 'ne';
export type Surface = 'earth' | 'stone' | 'wood';
export type Point = { x: number; y: number };
export interface CharacterFrame {
  sourceRect: [number, number, number, number];
  frameSize: [number, number];
  footAnchor: [number, number];
  durationMs: number;
  contact?: 'left' | 'right';
}
export interface CharacterClip { frames: CharacterFrame[]; loop: boolean }
const directions: Direction[] = ['e', 'se', 'sw', 'w', 'nw', 'ne'];
export function projectedDirection(from: Point, to: Point, previous: Direction = 'e'): Direction {
  const dx = to.x - from.x, dy = to.y - from.y;
  if (Math.hypot(dx, dy) < 0.001) return previous;
  const angle = Math.atan2(dy, dx);
  // Eight degrees of hysteresis at sector boundaries prevents direction chatter.
  const old = directions.indexOf(previous) * Math.PI / 3;
  const delta = Math.atan2(Math.sin(angle - old), Math.cos(angle - old));
  if (Math.abs(delta) <= Math.PI / 6 + 8 * Math.PI / 180) return previous;
  return directions[(Math.round(angle / (Math.PI / 3)) + 6) % 6];
}
export interface FootContact { type: 'foot-contact'; foot: 'left' | 'right'; surface: Surface }
/** Controlled delta clock. Call with paused=true for dialogue, hidden tab or portrait.
 * The first resumed tick is discarded, so background time never advances the actor. */
export class CharacterPlayer {
  private elapsed = 0;
  private suspended = false;
  private frameIndex = 0;
  readonly clip: CharacterClip;
  constructor(clip: CharacterClip) {
    this.clip = clip;
    if (!clip.frames.length || clip.frames.some(f => !Number.isFinite(f.durationMs) || f.durationMs <= 0)) {
      throw new Error('A clip requires positive finite frame durations');
    }
  }
  get frame(): CharacterFrame { return this.clip.frames[this.frameIndex]; }
  advance(deltaMs: number, options: { paused?: boolean; reducedMotion?: boolean; surface?: Surface } = {}): FootContact[] {
    if (options.paused) { this.suspended = true; return []; }
    if (this.suspended) { this.suspended = false; return []; }
    if (options.reducedMotion || !Number.isFinite(deltaMs) || deltaMs <= 0) return [];
    this.elapsed += deltaMs;
    const events: FootContact[] = [];
    while (this.elapsed >= this.frame.durationMs) {
      this.elapsed -= this.frame.durationMs;
      if (this.frameIndex === this.clip.frames.length - 1 && !this.clip.loop) { this.elapsed = 0; break; }
      this.frameIndex = (this.frameIndex + 1) % this.clip.frames.length;
      const foot = this.frame.contact;
      if (foot) events.push({ type: 'foot-contact', foot, surface: options.surface ?? 'earth' });
    }
    return events;
  }
}
/** Arc-length movement, independent of render frame rate. */
export function positionAlongPath(path: readonly Point[], distance: number): Point {
  if (!path.length) throw new Error('A route requires a point');
  let remaining = Math.max(0, distance);
  for (let i = 1; i < path.length; i++) {
    const a = path[i - 1], b = path[i], length = Math.hypot(b.x - a.x, b.y - a.y);
    if (!length) continue;
    if (remaining <= length) return { x: a.x + (b.x - a.x) * remaining / length, y: a.y + (b.y - a.y) * remaining / length };
    remaining -= length;
  }
  return { ...path[path.length - 1] };
}

/** Route state is independent of sprites. Completion is emitted once, including reduced motion. */
export class CharacterRoute {
  private distance = 0;
  private suspended = false;
  private completed = false;
  private heading: Direction = 'e';
  private readonly total: number;
  private readonly path: readonly Point[];
  private readonly speed: number;
  private readonly onComplete?: () => void;
  constructor(path: readonly Point[], pixelsPerSecond: number, onComplete?: () => void) {
    if (!path.length || !Number.isFinite(pixelsPerSecond) || pixelsPerSecond <= 0 || path.some(p => !Number.isFinite(p.x) || !Number.isFinite(p.y))) throw new Error('A route requires finite points and positive speed');
    this.path = path.map(p => ({ ...p })); this.speed = pixelsPerSecond; this.onComplete = onComplete;
    this.total = path.reduce((length, p, i) => i ? length + Math.hypot(p.x - path[i-1].x, p.y - path[i-1].y) : length, 0);
  }
  get position(): Point { return positionAlongPath(this.path, this.distance); }
  get direction(): Direction { return this.heading; }
  get done(): boolean { return this.completed; }
  advance(deltaMs: number, options: { paused?: boolean; reducedMotion?: boolean } = {}): Point {
    if (options.paused) { this.suspended = true; return this.position; }
    if (this.suspended) { this.suspended = false; return this.position; }
    if (this.completed || !Number.isFinite(deltaMs) || deltaMs < 0) return this.position;
    const from = this.position;
    this.distance = options.reducedMotion ? this.total : Math.min(this.total, this.distance + deltaMs * this.speed / 1000);
    const to = this.position; this.heading = projectedDirection(from, to, this.heading);
    if (this.distance >= this.total) { this.completed = true; this.onComplete?.(); }
    return to;
  }
}
