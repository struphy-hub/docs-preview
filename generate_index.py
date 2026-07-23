#!/usr/bin/env python3
"""Regenerate index.html by scanning top-level pr-* directories."""

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PR_DIR_RE = re.compile(r"^pr-(\d+)$")

REPO_SLUG = "struphy-hub/docs-preview"


def find_pr_dirs():
    prs = []
    for entry in ROOT.iterdir():
        if not entry.is_dir():
            continue
        match = PR_DIR_RE.match(entry.name)
        if match:
            prs.append((int(match.group(1)), entry.name))
    prs.sort(key=lambda pr: pr[0], reverse=True)
    return prs


def render(prs):
    rows = "\n".join(
        f'''      <li class="pr-row">
        <a class="pr-link" href="./{name}/">
          <span class="pr-number">#{number}</span>
          <span class="pr-path">{name}/</span>
        </a>
      </li>'''
        for number, name in prs
    )

    if not prs:
        rows = '      <li class="empty">No preview builds yet.</li>'

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Struphy docs previews</title>
<style>
  :root {{
    color-scheme: light dark;
    --bg: #f7f7f8;
    --fg: #1a1a1a;
    --card-bg: #ffffff;
    --border: #e2e2e5;
    --accent: #6e56cf;
    --muted: #6b6b70;
  }}
  @media (prefers-color-scheme: dark) {{
    :root {{
      --bg: #17181c;
      --fg: #eaeaec;
      --card-bg: #1f2025;
      --border: #303138;
      --accent: #9b8afb;
      --muted: #9a9aa2;
    }}
  }}
  * {{ box-sizing: border-box; }}
  body {{
    margin: 0;
    padding: 3rem 1.5rem;
    background: var(--bg);
    color: var(--fg);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
    display: flex;
    justify-content: center;
  }}
  main {{
    width: 100%;
    max-width: 640px;
  }}
  h1 {{
    font-size: 1.5rem;
    margin: 0 0 0.25rem;
  }}
  p.subtitle {{
    color: var(--muted);
    margin: 0 0 2rem;
    font-size: 0.95rem;
  }}
  ul {{
    list-style: none;
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    gap: 0.6rem;
  }}
  .pr-row .pr-link {{
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.9rem 1.1rem;
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 10px;
    text-decoration: none;
    color: var(--fg);
    transition: border-color 0.15s ease, transform 0.15s ease;
  }}
  .pr-row .pr-link:hover {{
    border-color: var(--accent);
    transform: translateY(-1px);
  }}
  .pr-number {{
    font-weight: 600;
    color: var(--accent);
    min-width: 3.5rem;
  }}
  .pr-path {{
    color: var(--muted);
    font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
    font-size: 0.9rem;
  }}
  li.empty {{
    color: var(--muted);
    padding: 0.9rem 1.1rem;
  }}
  footer {{
    margin-top: 2.5rem;
    color: var(--muted);
    font-size: 0.8rem;
  }}
</style>
</head>
<body>
<main>
  <h1>Struphy docs previews</h1>
  <p class="subtitle">Auto-generated list of open preview builds in <a href="https://github.com/{REPO_SLUG}">{REPO_SLUG}</a>.</p>
  <ul>
{rows}
  </ul>
  <footer>Regenerated automatically by generate_index.py on every push.</footer>
</main>
</body>
</html>
"""


def main():
    prs = find_pr_dirs()
    html = render(prs)
    out_path = ROOT / "index.html"
    out_path.write_text(html)
    print(f"Wrote {out_path} with {len(prs)} preview link(s).")


if __name__ == "__main__":
    main()
