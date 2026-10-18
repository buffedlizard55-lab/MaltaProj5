/* Optional real-browser QA. Runtime remains dependency-free.
 * npm install --prefix .cache/browser --no-audit --no-fund playwright-core@1.64.1 @sparticuz/chromium@153.0.0 axe-core@4.14.0
 * Start a static server, then:
 * NODE_PATH=.cache/browser/node_modules node tests/browser_smoke.cjs
 */
'use strict';
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright-core');
const chromiumPackage = require('@sparticuz/chromium');
const binary = chromiumPackage.default || chromiumPackage;

const base = (process.env.BASE_URL || 'http://127.0.0.1:8080').replace(/\/$/, '');
const pages = ['index.html', 'upcoming.html', 'weekly.html', 'monthly.html', 'annual.html', 'special.html', 'gaming.html', 'music.html', 'ai.html', 'free.html', 'markets.html', 'museums.html', 'culture.html', 'community.html', 'analysis.html', 'review.html', 'sources.html'];
// The directory table on a page carries class 'events' and a unique id, because the
// Upcoming page renders several grouped tables. The landing table is always #1.
const TABLE = 'table.events';
const ID = '-1';
const root = path.resolve(__dirname, '..');
const stats = JSON.parse(fs.readFileSync(path.join(root, 'data/audit_summary.json'), 'utf8'));
const output = path.resolve('.cache/qa');
let server;
const accessibility = [];
fs.mkdirSync(output, { recursive: true });

(async () => {
  if (process.argv.includes('--serve')) {
    const { spawn } = require('node:child_process');
    server = spawn('python3', ['-u', '-m', 'http.server', new URL(base).port || '8080', '--bind', '0.0.0.0'], { stdio: ['ignore', 'pipe', 'pipe'] });
    await new Promise((resolve, reject) => {
      const timeout = setTimeout(() => reject(new Error('Static test server did not start')), 10000);
      server.stdout.on('data', data => { if (String(data).includes('Serving HTTP')) { clearTimeout(timeout); resolve(); } });
      server.on('error', reject);
      server.on('exit', code => { clearTimeout(timeout); if (code) reject(new Error(`Static test server exited ${code}`)); });
    });
  }
  // The npm package bundles the shared NSS libraries needed in this minimal Linux sandbox.
  if (process.platform === 'linux' && chromiumPackage.inflate) {
    const bin = path.resolve(path.dirname(require.resolve('@sparticuz/chromium')), '../bin');
    const libraries = await chromiumPackage.inflate(path.join(bin, 'al2023.tar.br'));
    chromiumPackage.setupLambdaEnvironment(path.join(libraries, 'lib'));
  }
  const browser = await chromium.launch({ args: binary.args.filter(arg => arg !== '--single-process'), executablePath: await binary.executablePath(), headless: true });
  try {
    const errors = [];
    const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
    const page = await context.newPage();
    page.on('pageerror', error => errors.push(String(error)));
    page.on('console', message => { if (message.type() === 'error') errors.push(message.text()); });
    page.on('response', response => { if (response.url().startsWith(base) && response.status() >= 400) errors.push(`${response.status()} ${response.url()}`); });
    for (const filename of pages) {
      const response = await page.goto(`${base}/${filename}`);
      assert.equal(response.status(), 200, filename);
      assert.equal(await page.locator('h1').count(), 1, filename);
      assert.equal(await page.locator('nav[aria-label="Main navigation"] a').count(), 17);
      if (['analysis.html', 'sources.html'].includes(filename)) {
        assert.equal(await page.locator(TABLE).count(), 0, filename);
      } else {
        assert((await page.locator(TABLE).count()) >= 1, filename);
      }
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `Desktop document overflow: ${filename}`);
      if (['index.html', 'upcoming.html', 'free.html', 'review.html', 'sources.html', 'analysis.html'].includes(filename)) {
        await page.addScriptTag({ path: require.resolve('axe-core/axe.min.js') });
        const result = await page.evaluate(async () => await axe.run(document, { runOnly: { type: 'tag', values: ['wcag2a', 'wcag2aa', 'wcag21aa'] } }));
        const violations = result.violations.map(v => ({ id: v.id, impact: v.impact, nodes: v.nodes.map(n => n.target) }));
        accessibility.push({ page: filename, viewport: 'desktop', violations });
        assert.deepEqual(violations, [], `WCAG A/AA automated findings: ${filename}`);
      }
    }
    await page.goto(`${base}/index.html`);
    await page.screenshot({ path: path.join(output, 'index-desktop.png') });
    assert.equal(await page.locator(`${TABLE} tbody tr`).count(), stats.listed);
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.listed);
    assert.equal(await page.locator('#b-sf-pride-celebration').count(), 0);
    assert.equal(await page.locator('#b-nihonmachi-street-fair').count(), 0);
    assert.equal(await page.locator('#b-ferry-plaza-farmers-market td').nth(4).textContent(), '', 'blank admission stays blank');
    assert.match(await page.locator('#b-ferry-plaza-farmers-market td').nth(0).textContent(), /Not stated/, 'cost badge');
    assert.match(await page.locator('#b-opera-ball-2026').textContent(), /November 12, 2026/);
    assert.match(await page.locator('#b-opera-ball-2026').textContent(), /Future dated/);
    assert.match(await page.locator('#x-bill-graham-menorah').textContent(), /Date\/year unconfirmed/);
    assert(await page.locator('#table-tools' + ID).isVisible());
    await page.selectOption('#kind' + ID, 'Weekly');
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.kinds.Weekly);
    await page.fill('#search' + ID, 'no-such-event-xyz');
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), 0);
    assert(await page.locator('#empty' + ID).isVisible());
    await page.click('#reset' + ID);
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.listed);
    assert.equal(await page.inputValue('#search' + ID), '');
    await page.selectOption('#temporal' + ID, 'Future dated');
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.temporal['Future dated']);
    await page.click('#reset' + ID);
    await page.locator(TABLE).evaluate(element => element.scrollIntoView({ block: 'start' }));
    await page.screenshot({ path: path.join(output, 'index-table-desktop.png') });
    assert(await page.locator(`${TABLE} tbody tr`).evaluateAll(rows => rows.every(row => [...row.querySelectorAll('a.official')].some(a => a.href.startsWith('https://')))));
    await page.locator('#b-ferry-plaza-farmers-market a.evidence').click();
    await page.waitForURL('**/sources.html#e-b-ferry-plaza-farmers-market');
    await page.locator('#e-b-ferry-plaza-farmers-market details').first().locator('summary').click();
    assert(await page.locator('#e-b-ferry-plaza-farmers-market blockquote').first().isVisible());
    await page.screenshot({ path: path.join(output, 'field-evidence-desktop.png') });
    await page.goto(`${base}/review.html`);
    assert.equal(await page.locator(`${TABLE} tbody tr`).count(), stats.candidates);
    // Each table carries its own filter bar, so use the suffix of the table on this page.
    const reviewId = (await page.locator(TABLE).getAttribute('id')).replace('events-', '');
    await page.selectOption('#publication-' + reviewId, 'review_only');
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.review_only);
    assert.equal(await page.locator('#b-sf-pride-celebration td').nth(3).textContent(), '');
    assert.equal(await page.locator('#b-sf-pride-celebration td').nth(4).textContent(), '');
    assert.equal(await page.locator('#b-nihonmachi-street-fair td').nth(3).textContent(), '');

    await page.setViewportSize({ width: 390, height: 844 });
    for (const filename of pages) {
      const response = await page.goto(`${base}/${filename}`);
      assert.equal(response.status(), 200);
      assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), `Mobile document overflow: ${filename}`);
    }
    await page.goto(`${base}/index.html`);
    await page.screenshot({ path: path.join(output, 'index-mobile.png') });
    await page.getByRole('navigation', { name: 'Main navigation' }).getByRole('link', { name: 'Flagged for Review', exact: true }).click();
    await page.waitForURL('**/review.html');
    await page.locator('#table-tools-' + reviewId).scrollIntoViewIfNeeded();
    await page.selectOption('#publication-' + reviewId, 'review_only');
    assert.equal(await page.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.review_only);
    await page.screenshot({ path: path.join(output, 'review-mobile.png') });

    // Upcoming page: nearest confirmed date first, and the soonest rows highlighted.
    await page.setViewportSize({ width: 1440, height: 1000 });
    await page.goto(`${base}/upcoming.html`);
    const upcomingOrder = await page.locator(`${TABLE} tbody tr`).evaluateAll(rows => rows
      .map(row => row.id)
      .filter(id => id));
    const dated = JSON.parse(fs.readFileSync(path.join(root, 'data/upcoming_order.json'), 'utf8'));
    assert.deepEqual(upcomingOrder.slice(0, dated.length), dated, 'Upcoming is not nearest-first');
    assert((await page.locator(`${TABLE} tbody tr.soon`).count()) >= 1, 'No soonest-date highlight');
    // Mobile: each entry becomes a labelled card instead of a horizontally scrolling row.
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${base}/index.html`);
    const cellDisplay = await page.locator(`${TABLE} tbody td`).first().evaluate(el => getComputedStyle(el).display);
    assert.equal(cellDisplay, 'grid', 'Mobile table did not switch to the card layout');
    const headHidden = await page.locator(`${TABLE} thead`).first().evaluate(el => getComputedStyle(el).position);
    assert.equal(headHidden, 'absolute', 'Mobile table header should be visually hidden but present');
    assert(await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1), 'Mobile overflow on index');
    await page.screenshot({ path: path.join(output, 'index-mobile-cards.png') });
    await page.goto(`${base}/upcoming.html`);
    await page.screenshot({ path: path.join(output, 'upcoming-mobile.png') });
    await page.goto(`${base}/free.html`);
    await page.screenshot({ path: path.join(output, 'free-mobile.png') });
    assert.deepEqual(errors, [], 'Console/runtime/asset failures');

    const plain = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1280, height: 900 } });
    const nojs = await plain.newPage();

    await nojs.goto(`${base}/index.html`);
    assert.equal(await nojs.locator(`${TABLE} tbody tr`).count(), stats.listed);
    assert.equal(await nojs.locator(`${TABLE} tbody tr:not([hidden])`).count(), stats.listed);
    assert.equal(await nojs.locator('#table-tools').isVisible(), false);
    assert((await nojs.locator('#b-ferry-plaza-farmers-market a.official').count()) >= 1);
    const result = { browser: await browser.version(), viewports: ['1440×1000', '390×844'], pages: pages.length, directoryRows: stats.listed, heldRows: stats.review_only, reviewRows: stats.candidates, assertions: 'navigation, source links, evidence anchors, filters/reset/empty state, blank cells, cost badges, upcoming date order, mobile card layout, mobile overflow, JavaScript-disabled HTML, zero runtime/asset errors' };
    result.automatedAccessibility = accessibility;
    fs.writeFileSync(path.join(output, 'browser-result.json'), JSON.stringify(result, null, 2) + '\n');
    console.log('PASS:', JSON.stringify(result));
    await plain.close();
    await context.close();
  } finally {
    await browser.close();
  }
})().catch(error => { console.error(error); process.exitCode = 1; }).finally(() => { if (server) server.kill('SIGTERM'); });
