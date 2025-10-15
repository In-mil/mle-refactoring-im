#!/usr/bin/env bash
set -euo pipefail

# --- Ensure nbcommands/nbgrep is available ---
if ! command -v nbgrep >/dev/null 2>&1; then
  echo "nbcommands is not installed. Installing..."
  pip install nbcommands
fi

# --- Paths ---
OUT_DIR="./.github/workflows/testing"
PYTHON_FILE="${OUT_DIR}/test_import_libraries.py"
mkdir -p "${OUT_DIR}"
rm -f "${PYTHON_FILE}"

# --- One regex for BOTH notebooks and .py files ---
# - Multiline, handles parenthesized lists (optional trailing comma), aliases, relative imports
# - Inline comments stripped safely via #[^\n]*
NB_REGEX='(?m)^\s*(?:from\s+\.*(?:[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*)?\s+import\s+\(?\s*(\*|[A-Za-z_]\w*(?:\s+as\s+[A-Za-z_]\w*)?(?:\s*,\s*[A-Za-z_]\w*(?:\s+as\s+[A-Za-z_]\w*)?)*\s*,?)\s*\)?|import\s+[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\s+as\s+[A-Za-z_]\w*)?(?:\s*,\s*[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*(?:\s+as\s+[A-Za-z_]\w*)?)*)\s*(?:#[^\n]*)?$'

# --- Search for *.ipynb and *.py, skipping common virtual-env folders ---
find . \
  -type d \( -name '.venv' -o -name 'venv' -o -name 'env' -o -name '.env' \) -prune -false \
  -o -type f \( -name '*.ipynb' -o -name '*.py' \) -print0 |
while IFS= read -r -d '' file; do
  if [[ "$file" == *.ipynb ]]; then
    # Use nbgrep; tolerate "no matches"
    nbgrep "$NB_REGEX" "$file" \
      | grep -v 'nbgrep:' \
      | awk -F ':' '{sub(/^[^:]*:[^:]*:line [0-9]+:/, " ", $0)}1' \
      | sed -E 's/^[[:space:]]+//' \
      | sed -E 's/[[:space:]]*#[^\n]*$//' \
      | grep -E '^(from|import)[[:space:]]' || true
  else
    # Same regex on .py via Python re (supports multiline)
    python - "$file" "$NB_REGEX" <<'PY'
import re, sys, pathlib
path = pathlib.Path(sys.argv[1])
pattern = sys.argv[2]
try:
    text = path.read_text(encoding="utf-8", errors="ignore")
except Exception:
    sys.exit(0)
rx = re.compile(pattern, re.MULTILINE | re.DOTALL)
for m in rx.finditer(text):
    line = m.group(0).strip()
    line = re.sub(r"[ \t]*\n[ \t]*", " ", line)  # flatten (...) blocks
    line = re.sub(r"\s+#.*$", "", line)          # strip inline comment
    if line.startswith(("import ", "from ")):
        print(line)
PY
  fi
done |
# Squeeze spaces/tabs only; keep newlines (BSD/macOS safe)
sed -E 's/[[:blank:]]+/ /g' |
# Drop comment-only and empty lines
sed -E '/^[[:space:]]*#/d' |
sed -E '/^[[:space:]]*$/d' |
sort -u > "$PYTHON_FILE"

echo "<<<<<<< All extracted import statements from notebooks and Python scripts >>>>>>"
cat "$PYTHON_FILE"

# --- Build the pytest file (discover code roots dynamically; star-imports best-effort) ---
{
  cat <<'PY'
import os, sys, importlib
from typing import List

THIS_DIR = os.path.dirname(__file__)
REPO_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir, os.pardir, os.pardir))

# Discover top-level "code roots" automatically (folder-name agnostic).
# We consider any first-level directory under REPO_ROOT that contains at least one .py file.
IGNORE_DIRS = {
    ".git", ".github", ".vscode", ".idea", ".mypy_cache", ".pytest_cache", ".ruff_cache",
    "__pycache__", "build", "dist", "node_modules", "data", "notebooks", "docs",
    "venv", ".venv", "env", ".env"
}

def _discover_code_roots(repo_root: str) -> List[str]:
    roots: List[str] = []
    try:
        for name in os.listdir(repo_root):
            p = os.path.join(repo_root, name)
            if not os.path.isdir(p): 
                continue
            if name in IGNORE_DIRS or name.startswith('.'):
                continue
            # quick scan for any .py file inside this top-level dir
            found_py = False
            for r, dnames, fnames in os.walk(p):
                # prune common noise/venvs
                dnames[:] = [d for d in dnames if d not in IGNORE_DIRS and d != "__pycache__"]
                if any(f.endswith(".py") for f in fnames):
                    found_py = True
                    break
            if found_py:
                roots.append(p)
    except Exception:
        pass
    return roots

CODE_ROOTS = _discover_code_roots(REPO_ROOT)

# Put repo root and discovered code roots on sys.path (front) so imports resolve.
for root in [REPO_ROOT] + CODE_ROOTS:
    if root not in sys.path:
        sys.path.insert(0, root)

def _import_local_if_present(modname: str) -> None:
    """
    For 'from X import *' lines (illegal inside a function), best-effort import:
    - Try the module name as-is.
    - Also try with/without a leading 'src.' (covers src-layout vs flat layout).
    - Only import if the module path actually exists under any discovered code root.
    - If exists but import fails, let the exception bubble up to fail the test.
    - If not present locally, skip silently.
    """
    candidates = [modname]
    if modname.startswith("src."):
        candidates.append(modname[4:])
    else:
        candidates.append(f"src.{modname}")

    # Build a filesystem existence check against discovered roots
    fs_candidates = []
    for m in candidates:
        rel = m[4:] if m.startswith("src.") else m
        rel_path = os.path.join(*rel.split(".")) if rel else ""
        fs_candidates.append((m, rel_path))

    # Check presence under any code root; import first that exists
    for m, rel_path in fs_candidates:
        for base in CODE_ROOTS:
            py_file = os.path.join(base, rel_path + ".py")
            pkg_dir = os.path.join(base, rel_path)
            if os.path.isfile(py_file) or os.path.isfile(os.path.join(pkg_dir, "__init__.py")) or os.path.isdir(pkg_dir):
                importlib.import_module(m)
                return
    # Not present in this repo; skip.
    return

def test_import_libraries():
    try:
        pass  # keeps the try-block valid even if no imports found
PY

  # Emit imports; rewrite only star-imports to best-effort local import
  grep -E '^(from|import)[[:space:]]' "$PYTHON_FILE" \
    | sed -E 's/^from[[:space:]]+([A-Za-z_][A-Za-z0-9_\.]*)[[:space:]]+import[[:space:]]+\*$/_import_local_if_present("\1")/' \
    | sed 's/^/        /' || true

  cat <<'PY'
    except Exception as e:
        assert False, f"Failed to import library: {e}"

    assert True
PY
} > "${PYTHON_FILE}.tmp"

mv "${PYTHON_FILE}.tmp" "${PYTHON_FILE}"
echo
echo "Generated ${PYTHON_FILE}:"
echo "----------------------------------------"
cat "${PYTHON_FILE}"
echo "----------------------------------------"
