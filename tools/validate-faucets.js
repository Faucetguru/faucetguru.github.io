#!/usr/bin/env node
const fs = require('fs');
const vm = require('vm');
const path = require('path');

const filePath = path.resolve(__dirname, '../js/faucets.js');
const source = fs.readFileSync(filePath, 'utf8');

const sandbox = { window: {} };
vm.createContext(sandbox);
vm.runInContext(source, sandbox, { filename: 'faucets.js' });

const data = sandbox.window.faucetsData;
if (!Array.isArray(data)) {
  console.error('ERROR: window.faucetsData is not an array');
  process.exit(1);
}

const errors = [];
const warnings = [];
const typeCounts = {};

const isHttpUrl = (u) => typeof u === 'string' && /^https?:\/\//i.test(u.trim());

for (const [i, item] of data.entries()) {
  const idx = i + 1;
  const id = item?.id || `(index:${idx})`;

  if (!item?.id) errors.push(`${idx}: missing id`);
  if (!item?.name) errors.push(`${id}: missing name`);
  if (!item?.type) errors.push(`${id}: missing type`);
  if (!item?.summary) warnings.push(`${id}: empty summary`);

  if (item?.type) typeCounts[item.type] = (typeCounts[item.type] || 0) + 1;

  const link = String(item?.referralLink || '').trim();
  if (!link) {
    errors.push(`${id}: empty referralLink`);
  } else if (link === '#') {
    warnings.push(`${id}: referralLink is #`);
  } else if (link.includes('TU_ID')) {
    warnings.push(`${id}: referralLink contains placeholder TU_ID`);
  } else if (!isHttpUrl(link)) {
    warnings.push(`${id}: referralLink is not http/https (${link})`);
  }

  const image = String(item?.image || '').trim();
  if (!image) {
    warnings.push(`${id}: missing image`);
  } else if (!isHttpUrl(image)) {
    warnings.push(`${id}: image is not http/https (${image})`);
  }

  const score = Number(item?.trustScore);
  if (!Number.isFinite(score) || score < 0 || score > 5) {
    warnings.push(`${id}: trustScore out of range 0-5 (${item?.trustScore})`);
  }
}

console.log('Faucets dataset validation');
console.log('--------------------------');
console.log(`Items: ${data.length}`);
console.log(`Types: ${Object.keys(typeCounts).length}`);
console.log('Type counts:', typeCounts);
console.log('');

if (warnings.length) {
  console.log(`Warnings (${warnings.length}):`);
  for (const w of warnings) console.log(`- ${w}`);
  console.log('');
}

if (errors.length) {
  console.error(`Errors (${errors.length}):`);
  for (const e of errors) console.error(`- ${e}`);
  process.exit(1);
}

console.log('No blocking errors found.');
