// Render the editable HTML artwork to the 1200 x 630 social image.
// Usage: node social/render.mjs [path-to-Chrome-or-Chromium]
import { spawn } from 'node:child_process';
import { readFile, writeFile, mkdtemp } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import assert from 'node:assert/strict';

const executable = process.argv[2] || process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const profile = await mkdtemp(join(tmpdir(), 'deadline-social-'));
const chrome = spawn(executable, ['--headless=new', '--disable-gpu', '--no-first-run',
  '--no-default-browser-check', '--remote-debugging-port=0', `--user-data-dir=${profile}`, 'about:blank'],
  {windowsHide: true, stdio: 'ignore'});
let socket;
try {
  let port;
  for (let i = 0; i < 100; i++) {
    try { port = (await readFile(join(profile, 'DevToolsActivePort'), 'utf8')).split('\n')[0]; break; } catch {}
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  assert.ok(port, 'Chrome started');
  const pages = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
  socket = new WebSocket(pages.find(page => page.type === 'page').webSocketDebuggerUrl);
  await new Promise(resolve => socket.addEventListener('open', resolve, {once: true}));
  let id = 0;
  const pending = new Map();
  socket.addEventListener('message', ({data}) => {
    const message = JSON.parse(data), request = pending.get(message.id);
    if (!request) return;
    pending.delete(message.id);
    message.error ? request.reject(message.error) : request.resolve(message.result);
  });
  const send = (method, params = {}) => new Promise((resolve, reject) => {
    pending.set(++id, {resolve, reject});
    socket.send(JSON.stringify({id, method, params}));
  });
  const evaluate = async expression => {
    const result = await send('Runtime.evaluate', {expression, returnByValue: true, awaitPromise: true});
    assert.ok(!result.exceptionDetails, JSON.stringify(result.exceptionDetails));
    return result.result.value;
  };
  await send('Page.enable');
  await send('Emulation.setDeviceMetricsOverride', {width: 1200, height: 630, deviceScaleFactor: 1, mobile: false});
  await send('Page.navigate', {url: new URL('preview.html', import.meta.url).href});
  for (let i = 0; i < 100; i++) {
    if (await evaluate('document.readyState === "complete"')) break;
    await new Promise(resolve => setTimeout(resolve, 50));
  }
  await evaluate('document.fonts.ready.then(() => true)');
  assert.ok(await evaluate('document.fonts.check(\'17px "JetBrains Mono"\')'), 'Local font loaded');
  assert.ok(await evaluate('[...document.querySelectorAll(".card *")].every(e => { const r = e.getBoundingClientRect(); return r.left >= 0 && r.top >= 0 && r.right <= 1200 && r.bottom <= 630; })'), 'Artwork fits the image');
  const png = await send('Page.captureScreenshot', {format: 'png', clip: {x: 0, y: 0, width: 1200, height: 630, scale: 1}});
  const output = fileURLToPath(new URL('../og.png', import.meta.url));
  await writeFile(output, Buffer.from(png.data, 'base64'));
  console.log(`Rendered ${output} (1200 x 630)`);
  await send('Browser.close');
} finally {
  socket?.close();
  chrome.kill();
}
