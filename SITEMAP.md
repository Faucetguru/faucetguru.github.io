# Repository Map

This is a structural overview of the Faucetguru_site repository.

## Root Directory
- [index.html](./index.html) - Main entry point.
- [app.js](./app.js) - Main application logic.
- [style.css](./style.css) - Styling.
- [js/](./js/) - Data management.
  - [faucets.js](./js/faucets.js) - Primary data source.
  - [parsed-sites.json](./js/parsed-sites.json) - Processed data.
- [blog/](./blog/) - Blog content management.
  - [sitemap.md](./blog/sitemap.md) - Blog specific sitemap.
  - [markdown/](./blog/markdown/) - Individual blog posts.
  - [blogger-export/](./blog/blogger-export/) - Exports for Blogger.
- [tools/](./tools/) - Utility scripts.
  - [validate-faucets.js](./tools/validate-faucets.js) - Data validator.
  - [weekly_site_check.py](./tools/weekly_site_check.py) - Referral link checker.
  - [generate-blogger-xml.js](./tools/generate-blogger-xml.js) - Blogger export generator.
  - [generate-markdown-templates.js](./tools/generate-markdown-templates.js) - Template generator.
  - [interlink_script.py](./tools/interlink_script.py) - Internal linking tool.
  - [audit-content.js](./tools/audit-content.js) - Content auditor.
  - [generate-blogger-html-posts.js](./tools/generate-blogger-html-posts.js) - HTML generator.
  - [parse-xml-to-json.js](./tools/parse-xml-to-json.js) - Parser.
- [agents/](./agents/) - Agent-specific configuration.
- [site-status-weekly.md](./site-status-weekly.md) - Weekly status report.
- [WORKPLAN.md](./WORKPLAN.md) - Project work plan.
- [AGENTS.md](./AGENTS.md) - Agent instructions.
- [about-instructions.md](./about-instructions.md) - Project information.
- [generate_links.py](./generate_links.py) - Script to generate links.
- [check_blog_content.py](./check_blog_content.py) - Content checker.
- [check_content.js](./check_content.js) - JavaScript content checker.
- [open.sh](./open.sh) - Helper script.
