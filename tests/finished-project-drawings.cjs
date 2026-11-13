const fs = require('node:fs');
const http = require('node:http');
const assert = require('node:assert/strict');
const {chromium} = require('playwright');

const source = fs.readFileSync('index.html', 'utf8');
const hook = `window.finishedDrawingsTest={fresh,activateProject,changed,saveNow,projectWrite,projectRead,renderProjects,projectDrawingsReady,cbPlanToBoard,openProjectDrawings,snapshot:()=>({projectId:currentProject,project:clone(),surveyMode,screen:cbScreen,circuitId:cbCircuit?.id||null})};`;
const marker = "document.querySelector('.app').inert=true;\nensureUiState();";
const html = source.replace(marker, hook + marker);
assert.notEqual(html, source, 'test hook must be installed');
const server = http.createServer((req, res) => {
  const file = (req.url || '/').split('?')[0].slice(1) || 'index.html';
  try {
    res.setHeader('Content-Type', file.endsWith('.js') ? 'text/javascript' : file.endsWith('.png') ? 'image/png' : file.endsWith('.webp') ? 'image/webp' : 'text/html');
    res.end(file === 'index.html' ? html : fs.readFileSync(file));
  } catch {
    res.statusCode = 404;
    res.end();
  }
}).listen(0, '127.0.0.1');

(async () => {
  await new Promise(resolve => server.once('listening', resolve));
  const browser = await chromium.launch({headless: true});
  try {
    const page = await browser.newPage({viewport: {width: 390, height: 844}, hasTouch: true});
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto('http://127.0.0.1:' + server.address().port);
    await page.waitForFunction(() => !document.querySelector('#homeNew').disabled);
    const gates = await page.evaluate(async () => {
      const t = finishedDrawingsTest;
      const image = document.createElement('canvas');
      image.width = 800;
      image.height = 500;
      const imageUrl = image.toDataURL();
      const floor = (id, name, y) => {
        const d = t.fresh();
        d.image = imageUrl;
        d.isBlank = true;
        d.zones = [{id: 'zone', number: '1', name: 'Sales area', color: '#d44848'}];
        d.shapes = [{id: 'area', zone: 'zone', points: [{x: .1, y: .1}, {x: .9, y: .1}, {x: .9, y: .9}, {x: .1, y: .9}]}];
        d.walls = [{id: 'wall', kind: 'wall', points: [{x: .1, y: .1}, {x: .9, y: .1}, {x: .9, y: .9}]}];
        d.labels = [{id: 'label', x: .5, y: .65, text: name}];
        d.symbols = [{id: 'panel', type: 'panel', scope: 'survey', x: .2, y}, {id: 'detector', type: 'smoke', scope: 'survey', x: .7, y}];
        const bounds = {x1: 0, y1: 0, x2: 1, y2: 1};
        const layout = Object.fromEntries(d.symbols.map(s => [s.id, t.cbPlanToBoard(s, bounds)]));
        d.circuits = [{id: 'route-' + id, name: 'Zone 1', type: 'conventional', zoneId: 'zone', panelId: 'panel', deviceIds: ['detector'], bounds, layout, sequence: ['panel', 'detector'], legs: [{from: 'panel', to: 'detector', points: [layout.panel, layout.detector]}], bridges: [], complete: true}];
        d.asFit = {generatedAt: Date.now(), circuitIds: [d.circuits[0].id]};
        return {id, name, data: d};
      };
      const finished = {...t.fresh(), site: 'Finished shop', floors: [floor('ground', 'Ground floor', .3), floor('upper', 'Upper floor', .5)], activeFloor: 'ground'};
      const copy = value => JSON.parse(JSON.stringify(value));
      const check = mutate => {const p = copy(finished); mutate(p); return t.projectDrawingsReady(p)};
      const results = {
        complete: t.projectDrawingsReady(finished),
        acceptedUnassigned: check(p => p.floors[0].data.symbols.push({id: 'unassigned', type: 'heat', scope: 'survey', x: .6, y: .6})),
        unfinishedUpper: check(p => p.floors[1].data.circuits[0].complete = false),
        missingUpperAsFit: check(p => p.floors[1].data.asFit = null),
        missingZone: check(p => p.floors[0].data.zones = []),
        missingZoneArea: check(p => p.floors[0].data.shapes = []),
        unusedZone: check(p => p.floors[0].data.zones.push({id: 'empty', number: '2'})),
        missingSurvey: check(p => p.floors[0].data.symbols = []),
        movedSurvey: check(p => p.floors[0].data.symbols[1].x = .8),
        openEdit: check(p => p.floors[0].data.circuits[0].editDraft = {gaps: []}),
        staleCircuitIds: check(p => p.floors[0].data.asFit.circuitIds = ['old-route']),
        extraCircuit: check(p => p.floors[0].data.circuits.push({...copy(p.floors[0].data.circuits[0]), id: 'new-route'})),
        emptyProject: t.projectDrawingsReady(t.fresh())
      };
      const active = {...t.fresh(), site: 'Separate active project', image: imageUrl, isBlank: true};
      await t.activateProject('active-project', active);
      t.changed();
      await t.saveNow();
      const record = {id: 'finished-project', site: finished.site, systemType: 'fire', floorCount: 2, updatedAt: Date.now(), project: finished};
      await t.projectWrite('project:finished-project', record);
      const incomplete = copy(record);
      incomplete.id = 'incomplete-project';
      incomplete.site = incomplete.project.site = 'Unfinished shop';
      incomplete.project.floors[1].data.asFit = null;
      await t.projectWrite('project:incomplete-project', incomplete);
      document.querySelector('#projectsHome').hidden = false;
      document.querySelector('.app').inert = true;
      await t.renderProjects();
      window.finishedDrawingRecord = copy(record);
      return results;
    });
    assert.equal(gates.complete, true);
    assert.equal(gates.acceptedUnassigned, true, 'saved As fits may include explicitly accepted unassigned devices');
    for (const [name, ready] of Object.entries(gates)) {
      if (!['complete', 'acceptedUnassigned'].includes(name)) assert.equal(ready, false, name + ' must hide finished drawings');
    }
    const card = name => page.locator('.projectCard').filter({has: page.getByRole('heading', {name, exact: true})});
    const view = card('Finished shop').getByRole('button', {name: 'View finished drawings', exact: true});
    assert.equal(await view.count(), 1);
    assert.equal(await card('Unfinished shop').getByRole('button', {name: 'View finished drawings', exact: true}).count(), 0);
    const before = await page.evaluate(() => finishedDrawingsTest.snapshot());
    await view.click();
    await page.waitForFunction(() => document.querySelectorAll('#projectDrawingsGrid canvas').length === 3 && !document.querySelector('#projectDrawingsStatus').textContent);
    assert.deepEqual(await page.locator('#projectDrawingsGrid h3').allTextContents(), ['Zones - for customer', 'Survey - for engineer', 'As fit - for record']);
    assert.equal(await page.locator('#projectDrawingsFloor option').count(), 2);
    assert.equal(await page.locator('#projectDrawingsClose').evaluate(el => el === document.activeElement), true);
    const ground = await page.locator('#projectDrawingsGrid canvas').evaluateAll(canvases => canvases.map(c => c.toDataURL()));
    assert.equal(new Set(ground).size, 3, 'the three modes must render distinct drawings');
    await page.locator('#projectDrawingsFloor').selectOption('upper');
    await page.waitForFunction(() => document.querySelectorAll('#projectDrawingsGrid canvas').length === 3 && [...document.querySelectorAll('#projectDrawingsGrid canvas')].every(c => c.getAttribute('aria-label').endsWith('Upper floor')));
    const upper = await page.locator('#projectDrawingsGrid canvas').evaluateAll(canvases => canvases.map(c => c.toDataURL()));
    upper.forEach((drawing, i) => assert.notEqual(drawing, ground[i], 'floor switch must update drawing ' + i));
    assert.deepEqual(await page.evaluate(() => finishedDrawingsTest.snapshot()), before, 'previewing another project must preserve active project, floor and circuit state');
    assert.equal(await page.evaluate(async () => JSON.stringify(await finishedDrawingsTest.projectRead('project:finished-project')) === JSON.stringify(window.finishedDrawingRecord)), true, 'preview must preserve saved source project');
    await page.getByRole('button', {name: 'Enlarge As fit - for record', exact: true}).click();
    assert.equal(await page.getByRole('button', {name: 'Reduce As fit - for record', exact: true}).getAttribute('aria-expanded'), 'true');
    assert.equal(await page.locator('#projectDrawingsGrid figure.expanded .projectDrawingCanvas').evaluate(el => el.scrollWidth > el.clientWidth && el.querySelector('canvas').getBoundingClientRect().width > innerWidth), true, 'enlarged phone drawing must provide real magnification within a scrollable region');
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth && document.querySelector('#projectDrawings').scrollWidth <= document.querySelector('#projectDrawings').clientWidth), true, 'phone preview must not overflow horizontally');
    await page.getByRole('button', {name: 'Reduce As fit - for record', exact: true}).click();
    assert.equal(await page.getByRole('button', {name: 'Enlarge As fit - for record', exact: true}).getAttribute('aria-expanded'), 'false');
    assert.equal(await page.getByRole('region', {name: 'As fit - for record drawing; scroll to inspect when enlarged', exact: true}).evaluate(el => el.scrollWidth === el.clientWidth && el.querySelector('canvas').getBoundingClientRect().width <= el.clientWidth), true, 'Reduce drawing must restore the fitted preview');
    fs.mkdirSync('test-results', {recursive: true});
    await page.locator('#projectDrawings').evaluate(el => el.scrollTop = 0);
    await page.screenshot({path: 'test-results/finished-project-drawings-phone.png'});
    await page.screenshot({path: '/tmp/finished-drawings-phone.png'});
    await page.keyboard.press('Escape');
    await page.locator('#projectDrawings').waitFor({state: 'hidden'});
    await page.waitForFunction(() => document.activeElement?.textContent === 'View finished drawings');
    assert.equal(await page.locator('#projectDrawingsGrid canvas').count(), 0, 'closing releases rendered canvases');
    await view.click();
    await page.locator('#projectDrawings').waitFor({state: 'visible'});
    await page.locator('#projectDrawingsClose').click();
    await page.locator('#projectDrawings').waitFor({state: 'hidden'});
    await page.waitForFunction(() => document.activeElement?.textContent === 'View finished drawings');
    await page.reload();
    await page.waitForFunction(() => !document.querySelector('#homeNew').disabled);
    await view.click();
    await page.waitForFunction(() => document.querySelectorAll('#projectDrawingsGrid canvas').length === 3);
    assert.deepEqual(await page.locator('#projectDrawingsGrid h3').allTextContents(), ['Zones - for customer', 'Survey - for engineer', 'As fit - for record']);
    assert.equal((await page.evaluate(() => finishedDrawingsTest.snapshot())).projectId, 'active-project');
    await page.setViewportSize({width: 1440, height: 1000});
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    await page.locator('#projectDrawings').evaluate(el => el.scrollTop = 0);
    await page.screenshot({path: 'test-results/finished-project-drawings-desktop.png'});
    await page.screenshot({path: '/tmp/finished-drawings-desktop.png'});
    assert.deepEqual(errors, []);
    console.log('PASS: finished project gates, three labelled drawings, floor switching, read-only project isolation, close/focus, reload and responsive preview');
  } finally {
    await browser.close();
    server.close();
  }
})().catch(error => {console.error(error); server.close(); process.exitCode = 1;});
