#!/bin/bash
# SessionStart hook: make a fresh container able to run every check in CLAUDE.md.
#
# The container is rebuilt from a clean clone each session, and node_modules is
# gitignored, so without this the four browser smoke suites fail on a fresh session
# with "Cannot find module 'playwright'" and nothing says why.
#
# It also installs the document toolchain. LibreOffice ships here as core plus common
# with no Writer module, which fails in a confusing way: soffice exists, reports a
# version, and then refuses every document with "source file could not be loaded",
# including a plain .txt, because text to PDF goes through Writer too.
#
# Idempotent and non-interactive. Remote only: a local machine has its own setup.
set -uo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

cd "${CLAUDE_PROJECT_DIR:-$(pwd)}"
problems=""

# Chromium is preinstalled; the smoke suites all read CHROMIUM_PATH. Exporting it here
# means they can be run exactly as written in CLAUDE.md, with no wrapper.
CHROMIUM="$(ls -d /opt/pw-browsers/chromium-*/chrome-linux/chrome 2>/dev/null | head -1 || true)"
if [ -n "$CHROMIUM" ] && [ -n "${CLAUDE_ENV_FILE:-}" ]; then
  # SessionStart also fires on resume and clear, so do not stack duplicate exports.
  if ! grep -q '^export CHROMIUM_PATH=' "$CLAUDE_ENV_FILE" 2>/dev/null; then
    {
      echo "export CHROMIUM_PATH=\"$CHROMIUM\""
      echo "export PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers"
      echo "export PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1"
    } >> "$CLAUDE_ENV_FILE"
  fi
fi

# Playwright, for smoke_items / smoke_consent / smoke_billing / smoke_offline and the
# headless validation CLAUDE.md requires before shipping. The browser is already on
# disk, so the postinstall download is skipped rather than refetched.
if ! node -e "require.resolve('playwright')" >/dev/null 2>&1; then
  echo "installing playwright"
  if ! PLAYWRIGHT_SKIP_BROWSER_DOWNLOAD=1 npm install --no-save --no-fund --no-audit playwright@1.63.0; then
    problems="$problems playwright"
  fi
fi

# Document toolchain: rendering a .docx to look at it, reading one back, validating it.
export DEBIAN_FRONTEND=noninteractive
NEED=""
[ -f /usr/lib/libreoffice/program/libswlo.so ] || NEED="$NEED libreoffice-writer"
command -v pdftoppm >/dev/null 2>&1 || NEED="$NEED poppler-utils"
command -v pandoc   >/dev/null 2>&1 || NEED="$NEED pandoc"
if [ -n "$NEED" ]; then
  echo "installing apt:$NEED"
  apt-get update -qq >/dev/null 2>&1 || true
  if ! apt-get install -y -qq --no-install-recommends $NEED >/dev/null 2>&1; then
    problems="$problems$NEED"
  fi
fi

# defusedxml and lxml are what the docx skill's validate.py imports; python-docx and
# openpyxl read Office files directly. Note the import: "import importlib" alone does
# NOT give you importlib.util, and getting that wrong fails silently into a || true.
python3 - <<'PY'
import importlib.util, subprocess, sys
want = (('defusedxml', 'defusedxml'), ('lxml', 'lxml'),
        ('docx', 'python-docx'), ('openpyxl', 'openpyxl'))
missing = [pkg for mod, pkg in want if importlib.util.find_spec(mod) is None]
if missing:
    print('installing python:', ' '.join(missing))
    r = subprocess.run([sys.executable, '-m', 'pip', 'install', '--quiet',
                        '--break-system-packages'] + missing)
    sys.exit(r.returncode)
PY
[ $? -eq 0 ] || problems="$problems python-modules"

if [ -n "$problems" ]; then
  echo "session-start: finished, but these did not install:$problems"
else
  echo "session-start: ready"
fi
exit 0
