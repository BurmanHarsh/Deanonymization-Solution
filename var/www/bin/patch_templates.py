#!/usr/bin/env python3
"""
Systematically patch AIL templates so they pick up the dark modern-ui theme.
Two passes:
  1) Strip inline `body { background-color: #f4f7fb; }` (and similar) overrides.
  2) Add modern-ui.css link to any page that loads bootstrap4.min.css but not
     modern-ui.css, and ensure modern-ui.css loads AFTER every other CSS so
     its overrides win.
"""
import os
import re
import glob

TEMPLATES_ROOT = "/home/alpha/Deanonymization-Solution/var/www/templates"

LIGHT_BODY_PATTERNS = [
    re.compile(r"body\s*\{\s*background-color\s*:\s*#f4f7fb\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background\s*:\s*#f4f7fb\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background-color\s*:\s*#f8f9fb\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background-color\s*:\s*#f8f9fc\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background-color\s*:\s*#f5f5f5\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background-color\s*:\s*#f9fbfd\s*;?\s*\}", re.IGNORECASE),
    re.compile(r"body\s*\{\s*background\s*:\s*#fff\s*;?\s*\}", re.IGNORECASE),
]

MODERN_UI_LINK = '<link href="{{ url_for(\'static\', filename=\'css/modern-ui.css\') }}" rel="stylesheet">'


def patch_file(path: str) -> bool:
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    original = content

    # 1) Strip light body overrides inside inline <style> blocks
    for pat in LIGHT_BODY_PATTERNS:
        content = pat.sub("", content)

    # 2) Ensure modern-ui.css link is present after bootstrap4.min.css
    if "modern-ui.css" not in content and "bootstrap4.min.css" in content:
        content = content.replace(
            '<link href="{{ url_for(\'static\', filename=\'css/bootstrap4.min.css\') }}" rel="stylesheet">',
            '<link href="{{ url_for(\'static\', filename=\'css/bootstrap4.min.css\') }}" rel="stylesheet">\n  '
            '<link href="{{ url_for(\'static\', filename=\'css/modern-ui.css\') }}" rel="stylesheet">',
            1,
        )

    if content != original:
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main() -> None:
    changed = []
    for path in glob.glob(os.path.join(TEMPLATES_ROOT, "**", "*.html"), recursive=True):
        if patch_file(path):
            changed.append(path)
    print(f"Patched {len(changed)} templates:")
    for p in changed:
        print(f"  - {p}")


if __name__ == "__main__":
    main()
