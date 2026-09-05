// DOM-free regression checks for public score rendering. No browser or network.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const root = path.resolve(__dirname, '..');
const html = fs.readFileSync(path.join(root, 'index.html'), 'utf8');
const script = html.match(/<script>([\s\S]*?)<\/script>/)[1];

class Element {
  constructor(id) { this.id = id; this.value = id === 'f-effort' ? 'all' : ''; this.listeners = {}; }
  set innerHTML(value) {
    this.html = value;
    if (['f-cohort'].includes(this.id)) this.value = value.match(/value="([^"]*)"/)?.[1] || '';
  }
  get innerHTML() { return this.html || ''; }
  addEventListener(event, callback) { this.listeners[event] = callback; }
  appendChild() {}
  querySelectorAll() { return []; }
}

(async () => {
  const elements = new Map();
  const context = vm.createContext({
    document: {
      getElementById(id) { if (!elements.has(id)) elements.set(id, new Element(id)); return elements.get(id); },
      createElement() { return new Element(); },
      querySelectorAll() { return []; },
    },
    fetch: async file => ({ ok: true, json: async () => JSON.parse(fs.readFileSync(path.join(root, file), 'utf8')) }),
    Intl, console,
  });
  await vm.runInContext(script, context);
  const evaluate = code => vm.runInContext(code, context);
  assert.ok(html.includes('<title>Deadline</title>'));
  const community = evaluate('RUNS.find(r => r.model === "deepseek-v4-flash-0731")');
  assert.ok(community && !community.official && community.verified);
  assert.equal(community.score, 65.36);
  assert.equal(community.dscore, 31.31);
  assert.equal(community.samples, 1);
  assert.equal(community.seconds, 13362.43);
  assert.ok(elements.get('t-runs').innerHTML.includes('13362s'));
  assert.ok(elements.get('t-runs').innerHTML.includes('deepseek-v4-flash-0731'));
  assert.ok(elements.get('t-runs').innerHTML.includes('class="td-analysis"'));
  assert.ok(elements.get('t-runs').innerHTML.includes('Community<b>&times;1'));
  assert.ok(elements.get('c-frontier').innerHTML.includes('No cost per run measurements'));
  evaluate('metric = "tokens"; render()');
  assert.ok(elements.get('c-frontier').innerHTML.includes('<svg'));
  assert.ok(elements.get('c-frontier').innerHTML.includes('deepseek-v4-flash-0731'));
  assert.ok(!elements.get('c-frontier').innerHTML.includes('NaN'));
  evaluate('source = "community"; render()');
  assert.equal(evaluate('filtered().length'), 1);
  evaluate('source = "all"; metric = "cost"; render()');
  assert.ok(elements.get('t-subs').innerHTML.includes('settings were not independently verified'));
  assert.equal(evaluate('stampOf({official:true})'), '<span class="stamp official">Official</span>');
  assert.ok(elements.get('t-subs').innerHTML.includes('>TIME-DL</th>'));
  assert.ok(!elements.get('t-subs').innerHTML.includes('Time-DL (unverified)'));
  assert.ok(!html.includes('class="measurement-note"'));
  assert.ok(elements.get('t-subs').innerHTML.includes('Full-pass points'));
  const rendered = elements.get('t-subs').innerHTML;
  assert.ok(rendered.indexOf('class="td-analysis"') < rendered.indexOf('class="td-meta"'));
  assert.ok(rendered.includes('class="td-meta"'));
  assert.ok(!rendered.includes('score-summary'));
  assert.ok(!html.includes('Scores by task family'));
  assert.ok(!html.includes('Compare saved answers'));
  assert.ok(!elements.get('t-subs').innerHTML.includes('NaN'));
  assert.match(elements.get('t-subs').innerHTML, /class="score-v"[^>]*>\d+\.\d{2}</);
  assert.ok(elements.get('t-subs').innerHTML.includes('aria-expanded="false"'));
  const initialCount = evaluate('filtered().length');
  assert.ok(initialCount > 1);
  const mediumCount = evaluate('filtered().filter(r => r.effort === "medium").length');
  evaluate('RUNS.push({...RUNS[0], id:"old", suite_hash:"older", score:100})');
  assert.equal(evaluate('filtered().length'), initialCount, 'different suite hashes must not mix');
  elements.get('f-effort').value = 'medium';
  assert.equal(evaluate('filtered().length'), mediumCount);
  elements.get('f-effort').value = 'all';
  assert.equal(evaluate('fmtScore(null)'), '\u2014');
  assert.equal(evaluate('fmtScore(86.2)'), '86.20');
  context.escapeProbe = '<script>"&';
  assert.equal(evaluate('esc(escapeProbe)'), '&lt;script&gt;&quot;&amp;');
  console.log('Leaderboard rendering, precision, cohort isolation, effort filters, compact badges and escaping: PASS');
})().catch(error => { console.error(error); process.exitCode = 1; });
