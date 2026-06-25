#!/usr/bin/env python3
import os, json, re, datetime, sys
from pathlib import Path
import subprocess

# Load faucets data via Node VM (reuse existing approach)
def load_data():
    import json, subprocess, textwrap, shlex, sys
    js_path = Path(__file__).resolve().parents[1] / 'js' / 'faucets.js'
    # Execute a small node snippet that prints JSON of window.faucetsData
    node_code = textwrap.dedent('''
        const fs = require('fs');
        const vm = require('vm');
        const path = require('path');
        const src = fs.readFileSync(process.argv[1], 'utf8');
        const sandbox = {window:{}};
        vm.createContext(sandbox);
        vm.runInContext(src, sandbox);
        console.log(JSON.stringify(sandbox.window.faucetsData));
    ''')
    proc = subprocess.run(['node', '-e', node_code, str(js_path)],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        print('Failed to load faucets data:', proc.stderr, file=sys.stderr)
        sys.exit(1)
    return json.loads(proc.stdout)

def check_site(url):
    try:
        # Use curl for simplicity, follow redirects, timeout 10s, silent output, get HTTP code and body
        result = subprocess.run(['curl', '-Ls', '-m', '15', '-A', 'Mozilla/5.0', '-o', '-', '-w', '%{http_code}', url],
                                 capture_output=True, text=True)
        http_code = int(result.stdout[-3:]) if result.stdout[-3:].isdigit() else 0
        body = result.stdout[:-3]
        # Simple scam warning detection
        scam_keywords = ['scam', 'warning', 'fraud', 'blocked', 'report']
        body_lower = body.lower()
        scam_found = any(k in body_lower for k in scam_keywords)
        return http_code, scam_found, body
    except Exception as e:
        return 0, False, ''

def main():
    data = load_data()
    now = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')
    lines = []
    lines.append(f'# Weekly Site Status Report ({now})')
    lines.append('')
    lines.append('| ID | Name | Referral Link | HTTP Code | Status |')
    lines.append('|----|------|---------------|-----------|--------|')
    for entry in data:
        if not entry.get('id'):
            continue  # skip missing id as requested
        link = (entry.get('referralLink') or '').strip()
        # skip placeholder links
        if not link or link == '#' or 'TU_ID' in link:
            continue
        http_code, scam, _ = check_site(link)
        if http_code == 0:
            status = 'DOWN'
        elif scam:
            status = 'SCAM WARNING'
        elif http_code >= 200 and http_code < 400:
            status = 'OK'
        else:
            status = f'HTTP {http_code}'
        lines.append(f"| {entry['id']} | {entry['name']} | {link} | {http_code} | {status} |")
    out_path = Path(__file__).resolve().parents[1] / 'site-status-weekly.md'
    out_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f'Summary written to {out_path}')

if __name__ == '__main__':
    main()
