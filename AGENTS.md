# AGENTS.md – FaucetGuru Site

## Project

Static single-page site (no build step, no framework). Open `index.html` directly in a browser.

## File map

| File/Directory | Role |
|---|---|
| `index.html` | Main HTML shell – loads `js/faucets.js` then `js/app.js` (order matters). |
| `js/app.js` | Renders faucet cards, filters by `type`, detail view. |
| `js/faucets.js` | **Data file** – `window.faucetsData` array with faucet objects. |
| `js/blogger-client.js` | Blogger API client for post management. |
| `js/parsed-sites.json` | Parsed sites data. |
| `css/style.css` | Dark theme, CSS vars in `:root`, responsive grid. |
| `blog/` | Blog pages – `index.html`, `posts/`, `template-post.html`, `sitemap.md`. |
| `blogger-export/` | Generated Blogger XML exports. |
| `seo-tools/` | SEO utilities (e.g., `seo-tools/seo-gen.js`). |
| `tools/` | Python/Node.js automation scripts. |
| `blog/posts/` | Individual HTML blog posts. |

## Commands

```bash
node tools/validate-faucets.js   # validate faucets.js schema before committing
python3 tools/weekly_site_check.py  # check all referral links, updates site-status-weekly.md
node tools/generate-blogger-html-posts.js # generate individual HTML posts for Blogger
python3 tools/sync-blogger-posts.py # sync Blogger posts with local files
python3 tools/send-to-blogger.py    # publish posts to Blogger
python3 tools/validate-seo-posts.py    # validate HTML posts for SEO
```

## Git Conventions

- Always use `--no-gpg-sign` for all `git commit` commands in this repository.
- No npm, no bundler, no dev server. Just open `index.html`.

## Kilo Configuration

- Config file: `kilo.json`
- MCP servers configured: `blogger` (uses `mcp-blogger` package)

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
- The blog section (`showBlog()`) links to `blog/index.html`.

## Tools Reference

### Faucet Data Management
- `tools/validate-faucets.js` – validates schema for `js/faucets.js`
- `tools/weekly_site_check.py` – curls referral links, writes `site-status-weekly.md`

### Blog Posts (Blogger)
- `tools/sync-blogger-posts.py` – sync Blogger API posts with local files
- `tools/send-to-blogger.py` – publish HTML posts via email
- `tools/list-blogger-posts.py` – list Blogger posts
- `tools/update-blogger-post.py` – update existing Blogger posts
- `tools/update-blogger-metadata.py` – update SEO metadata
- `tools/post-to-blogger.py` – post management
- `tools/send-unposted-to-blogger.py` – send unposted articles
- `tools/send-2-pending.py` – send posts to pending status

### SEO & Content
- `tools/validate-seo-posts.py` – validate HTML posts (H1, meta description 70-160 chars, keywords min 3, content min 300 chars, images with alt)
- `tools/audit-content.js` – content auditing
- `tools/seo-blog-posts.js` – SEO optimization for blog posts
- `tools/interlink_script.py` – interlink generation
- `tools/generate-blog-index.js` – generate blog index

### Translation & Updates
- `tools/translate-post.py` – translate posts
- `tools/update-post-spanish.py` – update Spanish posts
- `tools/update-post-js.js` – update posts via JS

### Utilities
- `tools/generate-blogger-html-posts.js` – generate HTML posts
- `tools/generate-blogger-xml.js` – generate Blogger XML
- `tools/generate-token-from-code.py` – generate OAuth token
- `tools/get-blogger-token.py` – get Blogger token
- `tools/remove-anchors.py` – remove anchor tags from posts
- `tools/parse-xml-to-json.js` – parse XML to JSON
- `tools/generate-markdown-templates.js` – generate markdown templates
- `tools/batch-post-blogs.py` – batch process posts
- `tools/git-push.sh` – git push utility

### Authentication
- `tools/credentials.json` – Blogger API credentials
- `tools/oauth-client.html` – OAuth client
- `tools/oauth-url.txt` – OAuth URL