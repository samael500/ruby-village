import {test} from 'node:test';
import assert from 'node:assert/strict';
import spec from '../src/chapter-1.story.json' with {type:'json'};
import {stories,storyFor,ending,invitation} from '../src/story.ts';
import {levels} from '../src/levels.ts';
test('Сюжетный адаптер сопоставляет восемь сцен, порядок карты и engine IDs',()=>{
 assert.equal(stories.length,8);assert.equal(new Set(stories.map(s=>s.id)).size,8);
 assert.deepEqual(stories.map(s=>s.engineId),levels.map(l=>l.id));
 assert.deepEqual(spec.map.nodes.map(n=>n.levelId),stories.map(s=>s.id));
 stories.forEach((s,i)=>{
  assert.equal(storyFor(levels[i].id)?.id,s.id);assert.equal(s.title,levels[i].name);
  assert.ok(s.before.length&&s.after.length&&s.victoryScene&&s.clue);
  assert.equal(s.nextLevelId,stories[i+1]?.id??null);
  if(i<7)assert.deepEqual(spec.map.edges[i],{fromLevel:s.id,toLevel:stories[i+1].id});
 });
 assert.equal(invitation.revealedAt,stories[6].id);assert.equal(ending.title,'Письма через лес');
 assert.equal(levels.length,8); // The next chapter is an announcement, not playable data.
});
