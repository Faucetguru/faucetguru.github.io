#!/usr/bin/env node
/*
 * litecoinfarm_autoclaim.js
 * Intenta reclamar LTC en https://litecoinfarm.online/index.php
 * usando un Chrome real (Playwright) con movimiento de mouse humanoide.
 *
 * ESTRATEGIA: Turnstile en modo checkbox visible -> se prueba resolver
 * con un click humano-like (sin solver de pago). Si el token aparece,
 * se envia el form y se espera redireccion a mine.php.
 *
 * Uso:
 *   node tools/litecoinfarm_autoclaim.js [--headed] [--email=tu@mail.com]
 *
 * Nota: si Turnstile pide desafio de imagen o da "Invalid token",
 * el click solo no alcanza y hay que meter un solver (2Captcha/CapMonster).
 */

const { chromium } = require('playwright');

const SITE = 'https://litecoinfarm.online/index.php';
const EMAIL = process.argv.find(a => a.startsWith('--email='))?.split('=')[1] || 'polakenfold@gmail.com';
const HEADED = process.argv.includes('--headed');

// Movimiento de mouse humanoide: varios pasos con jitter, no linea recta.
async function humanMove(page, target) {
  const box = await target.boundingBox();
  if (!box) throw new Error('No boundingBox for target');
  const start = { x: 10, y: 10 };
  const tx = box.x + box.width / 2;
  const ty = box.y + box.height / 2;
  const steps = 18 + Math.floor(Math.random() * 10);
  for (let i = 1; i <= steps; i++) {
    const t = i / steps;
    const e = t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
    const x = start.x + (tx - start.x) * e + (Math.random() - 0.5) * 6;
    const y = start.y + (ty - start.y) * e + (Math.random() - 0.5) * 6;
    await page.mouse.move(x, y);
    await page.waitForTimeout(8 + Math.random() * 14);
  }
  await page.mouse.move(tx, ty);
  await page.waitForTimeout(60 + Math.random() * 120);
}

function log(...a) { console.log(`[${new Date().toISOString()}]`, ...a); }

(async () => {
  log('Iniciando Chrome...');
  const browser = await chromium.launch({
    headless: !HEADED,
    executablePath: process.env.CHROME_BIN || '/usr/bin/google-chrome-stable',
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
      '--disable-dev-shm-usage',
    ],
  });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    viewport: { width: 420, height: 800 },
    locale: 'en-US',
  });
  // ocultar navigator.webdriver
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  const page = await context.newPage();
  page.on('console', m => { if (m.type() === 'error') log('PAGE-ERR:', m.text()); });
  page.on('requestfailed', r => log('REQ-FAIL:', r.url(), r.failure()?.errorText));

  log('Navegando a', SITE);
  await page.goto(SITE, { waitUntil: 'domcontentloaded', timeout: 30000 });
  await page.waitForTimeout(4000); // Turnstile carga

  // 1) email
  const emailSel = 'input[name="faucet_email"]';
  await page.waitForSelector(emailSel, { timeout: 10000 });
  await page.fill(emailSel, EMAIL);
  log('Email ingresado:', EMAIL);

  // 2) buscar el checkbox del Turnstile (puede estar en iframe)
  log('Buscando widget Turnstile...');
  let turnstileFrame = null;
  let checkbox = null;

  // El checkbox suele estar dentro de un iframe de challenges.cloudflare.com
  const frames = page.frames();
  for (const f of frames) {
    try {
      const cb = await f.$('input[type="checkbox"], #checkbox, .ctp-checkbox, label');
      if (cb) { turnstileFrame = f; checkbox = cb; break; }
    } catch {}
  }
  if (!checkbox) {
    // fallback: el div .cf-turnstile mismo
    checkbox = await page.$('.cf-turnstile');
    log('No se encontro iframe de Turnstile; usando div .cf-turnstile');
  }

  if (checkbox) {
    log('Click humanoide en Turnstile...');
    if (turnstileFrame) {
      await humanMoveFrame(turnstileFrame, checkbox);
    } else {
      await humanMove(page, checkbox);
    }
    await page.mouse.down();
    await page.waitForTimeout(40 + Math.random() * 60);
    await page.mouse.up();
    log('Click realizado. Esperando resolucion...');
  } else {
    log('WARN: no se localizo el widget del captcha');
  }

  // esperar a que aparezca el token cf-turnstile-response
  let token = null;
  for (let i = 0; i < 20; i++) {
    token = await page.$eval('input[name="cf-turnstile-response"]', el => el.value).catch(() => null);
    if (token && token.length > 10) break;
    await page.waitForTimeout(1000);
  }

  if (!token || token.length <= 10) {
    log('RESULT: Turnstile NO resolvio solo (token ausente). El click no alcanza -> hace falta solver.');
    // diagnostico: estado del widget
    const diag = await page.evaluate(() => {
      const w = document.querySelector('.cf-turnstile');
      return {
        turnstileHTML: w ? w.outerHTML.slice(0, 200) : 'no .cf-turnstile',
        hasResponseInput: !!document.querySelector('input[name="cf-turnstile-response"]'),
      };
    }).catch(e => ({ err: String(e) }));
    log('DIAG:', JSON.stringify(diag));
    await browser.close();
    process.exit(2);
  }

  log('RESULT: Turnstile RESUELTO. Token len =', token.length);

  // 3) enviar el form (click en boton Claim)
  const claimBtn = await page.$('button[type="submit"]');
  if (claimBtn) {
    await humanMove(page, claimBtn);
    await claimBtn.click();
    log('Claim enviado. Esperando respuesta...');
  } else {
    // fallback: submit del form
    await page.evaluate(() => document.querySelector('form')?.requestSubmit?.());
    log('Form submit (fallback) disparado.');
  }

  // esperar redireccion o mensaje
  try {
    await page.waitForURL('**/mine.php', { timeout: 8000 });
    log('RESULT: REDIRIGIDO a mine.php -> CLAIM EXITOSO');
  } catch {
    const url = page.url();
    const bodyTxt = await page.evaluate(() => document.body.innerText.slice(0, 300)).catch(() => '');
    log('RESULT: no redirigio. URL actual:', url);
    log('BODY:', bodyTxt.replace(/\n+/g, ' ').trim());
  }

  await browser.close();
  process.exit(0);
})().catch(e => { console.error('FATAL:', e); process.exit(1); });

// helper para mover mouse dentro de un frame (usa coordenadas del frame)
async function humanMoveFrame(frame, elementHandle) {
  const box = await elementHandle.boundingBox();
  if (!box) return;
  const tx = box.x + box.width / 2;
  const ty = box.y + box.height / 2;
  // page.mouse se mueve en coordenadas de viewport; para iframe usamos click directo
  // (los iframes de turnstile suelen ser pequeños y centrados)
  await elementHandle.click({ trial: false });
}
