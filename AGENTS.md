# AGENTS.md – FaucetGuru Site

## Project

Static single-page site (no build step, no framework). Open `index.html` directly in a browser.

## File map

| File | Role |
|---|---|
| `js/faucets.js` | **Only data file** – `window.faucetsData` array. Every site is an object here. |
| `app.js` | Renders cards, filters by `type`, detail view, blog placeholder. |
| `style.css` | Dark theme, CSS vars in `:root`, responsive grid. |
| `index.html` | Shell – loads `faucets.js` then `app.js` (order matters). |
| `tools/validate-faucets.js` | Node validator for `faucets.js` schema. |
| `tools/weekly_site_check.py` | Python script that curls every referral link, writes `site-status-weekly.md`. |
| `blogger-export/` | Generated Blogger XML exports (not used by the site). |

## Commands

```bash
node tools/validate-faucets.js   # validate faucets.js schema before committing
python3 tools/weekly_site_check.py  # check all referral links, updates site-status-weekly.md
node tools/generate-blogger-html-posts.js # generate individual HTML posts for Blogger
```

## Git Conventions

- Always use `--no-gpg-sign` for all `git commit` commands in this repository.

No npm, no bundler, no dev server. Just open `index.html`.

## Adding a new site

Append an object to `js/faucets.js` (inside the `window.faucetsData` array). Required fields:

- `id` (unique slug), `name`, `type`, `trustScore` (0-5), `summary`, `referralLink`
- Optional: `bonus`, `image`, `strategies`, `script`, `reviews[]`

**Conventions:**
- Use `#` for `referralLink` if unavailable; use `referralLink: "https://.../ref/TU_ID"` only as a temporary placeholder (validator will warn).
- `script: "N/A"` when no script applies.
- `reviews: []` is valid if no reviews yet.
- New `type` values auto-generate nav filter buttons (labels defined in `app.js` `TYPE_LABELS`).

## Validation rules (from `tools/validate-faucets.js`)

- `id`, `name`, `type` are required (blocking errors if missing).
- `referralLink` must be non-empty; `#` and `TU_ID` trigger warnings.
- `trustScore` must be a number 0-5.
- Run validator before committing: `node tools/validate-faucets.js` exits 1 on errors.

## Architecture notes

- **No framework** – vanilla JS DOM manipulation via `innerHTML`.
- All user-facing text is escaped via `escapeHtml()` in `app.js`.
- URLs are sanitized by `safeUrl()` – only `http://`/`https://` pass; `#`, empty, and `TU_ID` are blocked.
- External links use `rel="noopener noreferrer"`.
- Nav filter buttons are dynamically generated from unique `type` values in the data.
- The blog section (`showBlog()`) should link  blog/blogger-export/html-posts/

## Weekly check

`tools/weekly_site_check.py` requires `node` and `curl`. It parses `faucets.js` via Node VM, then curls each referral link with a 15s timeout. Results overwrite `site-status-weekly.md`. Many sites show "SCAM WARNING" due to keyword detection in page body – this is heuristic, not definitive.
