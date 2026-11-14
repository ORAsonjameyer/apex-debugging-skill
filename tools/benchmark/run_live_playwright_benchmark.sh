#!/usr/bin/env bash
set -euo pipefail

# Playwright-only live benchmark driver.
# It attaches to an existing browser and never launches a new login session.

SESSION_NAME="${PLAYWRIGHT_SESSION_NAME:-apex-benchmark}"
BENCHMARK_URL="${APEX_BENCHMARK_URL:-http://localhost:7002/ords/r/oracle/apex-debug-bench/automatic}"
CDP_ENDPOINT="${PLAYWRIGHT_CDP_ENDPOINT:-}"
BROWSER_EXTENSION="${PLAYWRIGHT_EXTENSION:-}"
POLL_TIMEOUT_SECONDS="${BENCHMARK_TIMEOUT_SECONDS:-1800}"
PWCLI="${PWCLI:-/Users/SOMEYER/.codex/skills/playwright/scripts/playwright_cli.sh}"
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ARTIFACT_DIR="${PLAYWRIGHT_ARTIFACT_DIR:-$REPO_ROOT/output/playwright/live-benchmark}"

usage() {
  cat <<'EOF'
Usage:
  run_live_playwright_benchmark.sh --cdp-endpoint URL
  run_live_playwright_benchmark.sh --extension chrome

The browser must already contain the authenticated APEX session. The script
does not launch a new browser, request credentials, open DevTools, inspect
source files, retry failed cases, or change the application/database.

Options:
  --cdp-endpoint URL  Attach to an existing browser CDP endpoint.
  --extension NAME    Attach through an installed Playwright browser extension.
  --session NAME      Playwright CLI session name.
  --url URL           APEX automatic benchmark page.
  --timeout SECONDS   Maximum wait for the result table (default: 1800).
EOF
}

while (($#)); do
  case "$1" in
    --cdp-endpoint)
      [[ $# -ge 2 ]] || { echo "Missing value for --cdp-endpoint" >&2; exit 2; }
      CDP_ENDPOINT="$2"
      shift 2
      ;;
    --extension)
      [[ $# -ge 2 ]] || { echo "Missing value for --extension" >&2; exit 2; }
      BROWSER_EXTENSION="$2"
      shift 2
      ;;
    --session)
      [[ $# -ge 2 ]] || { echo "Missing value for --session" >&2; exit 2; }
      SESSION_NAME="$2"
      shift 2
      ;;
    --url)
      [[ $# -ge 2 ]] || { echo "Missing value for --url" >&2; exit 2; }
      BENCHMARK_URL="$2"
      shift 2
      ;;
    --timeout)
      [[ $# -ge 2 ]] || { echo "Missing value for --timeout" >&2; exit 2; }
      POLL_TIMEOUT_SECONDS="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -x "$PWCLI" ]] || { echo "Playwright CLI wrapper not executable: $PWCLI" >&2; exit 2; }
[[ "$POLL_TIMEOUT_SECONDS" =~ ^[0-9]+$ ]] || { echo "--timeout must be an integer" >&2; exit 2; }
[[ -n "$CDP_ENDPOINT" || -n "$BROWSER_EXTENSION" ]] || {
  echo "Refusing to launch a new browser: provide --cdp-endpoint or --extension." >&2
  exit 2
}

mkdir -p "$ARTIFACT_DIR"
cd "$ARTIFACT_DIR"

if [[ -n "$CDP_ENDPOINT" ]]; then
  "$PWCLI" --session "$SESSION_NAME" attach --cdp --endpoint "$CDP_ENDPOINT"
else
  "$PWCLI" --session "$SESSION_NAME" attach --extension="$BROWSER_EXTENSION"
fi

# Navigation is performed only inside the attached, already-authenticated browser.
"$PWCLI" --session "$SESSION_NAME" goto "$BENCHMARK_URL"
"$PWCLI" --session "$SESSION_NAME" snapshot >/dev/null

FLOW_CODE=$(cat <<'EOF'
const bodyText = await page.locator('body').innerText();
if (/\b(log\s*in|sign\s*in|anmelden)\b/i.test(bodyText.slice(0, 2500))) {
  throw new Error('The attached browser is not authenticated; no login was attempted.');
}

const readTable = async (table) => table.locator('tr').evaluateAll((rows) => rows
  .map((row) => Array.from(row.querySelectorAll('th,td'))
    .map((cell) => (cell.textContent || '').replace(/\s+/g, ' ').trim())
    .filter(Boolean))
  .filter((cells) => cells.length > 0));

const modelTable = page.locator('table').filter({ hasText: /Benchmark-Status/i }).first();
if (await modelTable.count() === 0) {
  throw new Error('The available-model table was not found.');
}
const modelRows = await readTable(modelTable);
const models = modelRows
  .filter((cells) => cells.length >= 3 && cells[0].toLowerCase() !== 'modell')
  .map((cells) => cells[0]);
if (models.length === 0) {
  throw new Error('No available models were visible.');
}

const start = page.getByRole('button', { name: /Benchmark starten/i });
if (await start.count() !== 1) {
  throw new Error('Expected exactly one "Benchmark starten" button.');
}
await start.click();

const expectedRows = models.length * 3;
const deadline = Date.now() + Number(process.env.BENCHMARK_POLL_TIMEOUT_MS || 1800000);
let latest = [];
while (Date.now() < deadline) {
  const runTable = page.locator('table').filter({ hasText: /Use Case/i }).first();
  if (await runTable.count() > 0) {
    latest = (await readTable(runTable))
      .filter((cells) => cells.length >= 3 && cells[0].toLowerCase() !== 'modell');
    const counts = new Map();
    for (const cells of latest) counts.set(cells[0], (counts.get(cells[0]) || 0) + 1);
    const completeShape = latest.length >= expectedRows && models.every((model) => counts.get(model) === 3);
    const stillRunning = latest.some((cells) => /queued|running|in progress|warteschlange|läuft|aktiv|gestartet/i.test(cells.join(' ')));
    if (completeShape && !stillRunning) {
      console.log(JSON.stringify({ models, expected_use_cases_per_model: 3, rows: latest }));
      return;
    }
  }
  await page.waitForTimeout(1000);
}

throw new Error(`Timed out waiting for exactly three terminal use-case rows per model. Last rows: ${JSON.stringify(latest)}`);
EOF
)

BENCHMARK_POLL_TIMEOUT_MS=$((POLL_TIMEOUT_SECONDS * 1000)) \
  "$PWCLI" --session "$SESSION_NAME" run-code "$FLOW_CODE"
