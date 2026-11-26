#!/usr/bin/env python3
"""Time independent, offline Codex analyses of user-supplied incident snapshots."""
import argparse
import csv
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time


def write_results(output, results):
    json_tmp = output / 'results.json.tmp'
    json_tmp.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding='utf-8')
    os.replace(json_tmp, output / 'results.json')
    csv_tmp = output / 'results.csv.tmp'
    with csv_tmp.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    os.replace(csv_tmp, output / 'results.csv')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True, help='JSON array of {id, title, evidence}, containing redacted incident snapshots')
    parser.add_argument('--models', nargs='+', required=True, help='Actual model IDs accepted by the local Codex CLI')
    parser.add_argument('--repetitions', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=300, help='Maximum seconds per analysis')
    parser.add_argument('--output', type=Path, required=True, help='New output directory')
    parser.add_argument('--codex', default='codex', help='Codex executable')
    args = parser.parse_args()
    if args.repetitions < 1 or args.timeout < 1:
        parser.error('repetitions and timeout must be positive')
    cases = json.loads(args.cases.read_text(encoding='utf-8'))
    if not isinstance(cases, list) or not cases:
        parser.error('cases must be a non-empty JSON array')
    ids = set()
    for case in cases:
        if not isinstance(case, dict) or not all(isinstance(case.get(k), str) and case[k].strip() for k in ('id', 'title', 'evidence')):
            parser.error('each case needs nonempty string id, title, and evidence')
        if case['id'] in ids:
            parser.error('case IDs must be unique')
        ids.add(case['id'])
    executable = shutil.which(args.codex)
    if not executable:
        parser.error('Codex executable not found')
    args.output.mkdir(parents=True, exist_ok=False)
    source_hash = hashlib.sha256(args.cases.read_bytes()).hexdigest()
    metadata = {'cases_sha256': source_hash, 'models': args.models, 'repetitions': args.repetitions,
                'timeout_seconds': args.timeout, 'mode': 'offline evidence snapshots; no live browser or MCP',
                'created_utc': dt.datetime.now(dt.timezone.utc).isoformat()}
    (args.output / 'run.json').write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding='utf-8')
    results = [{'case_id': case['id'], 'case_title': case['title'], 'model': model,
                'repetition': repeat, 'elapsed_seconds': None, 'status': 'queued',
                'detail': '', 'answer_file': ''}
               for model in args.models for case in cases
               for repeat in range(1, args.repetitions + 1)]
    write_results(args.output, results)
    with tempfile.TemporaryDirectory(prefix='apex-benchmark-') as isolated:
        index = 0
        for model in args.models:
            for case in cases:
                for repeat in range(1, args.repetitions + 1):
                    row = results[index]
                    index += 1
                    response = args.output / f'{index:04d}-antwort.txt'
                    prompt = ("Analysiere diesen APEX-Vorfall ausschließlich anhand der folgenden anonymisierten "
                              "Evidenz. Nutze keine Werkzeuge oder externen Quellen und führe keine Änderungen aus. "
                              "Nenne Beobachtung, mögliche Ursache, entscheidende Belege, Unsicherheiten und den "
                              "nächsten lesenden Prüfschritt. Behaupte keine nicht belegten Fakten.\n\n"
                              f"Fall: {case['title']}\nEvidenz:\n{case['evidence']}\n")
                    cmd = [executable, 'exec', '--ignore-user-config', '--sandbox', 'read-only',
                           '--ephemeral', '--skip-git-repo-check', '--model', model,
                           '--cd', isolated, '--output-last-message', str(response.resolve()), '-']
                    row['status'] = 'running'
                    write_results(args.output, results)
                    print(f'[{index}] {model} / {case["id"]} / {repeat}', flush=True)
                    start = time.monotonic()
                    try:
                        run = subprocess.run(cmd, input=prompt, text=True, capture_output=True,
                                             timeout=args.timeout, cwd=isolated)
                        elapsed = time.monotonic() - start
                        status = 'completed' if run.returncode == 0 and response.is_file() and response.stat().st_size else 'execution_error'
                        detail = '' if status == 'completed' else f'exit code {run.returncode}; see diagnostic file'
                        if status != 'completed':
                            (args.output / f'{index:04d}-diagnose.txt').write_text(run.stderr[-8000:], encoding='utf-8')
                    except subprocess.TimeoutExpired:
                        elapsed = time.monotonic() - start
                        status, detail = 'timeout', 'time limit reached'
                    row.update(elapsed_seconds=round(elapsed, 3), status=status, detail=detail,
                               answer_file=response.name if response.exists() else '')
                    write_results(args.output, results)
    print(f'Ergebnisse: {args.output}')
    return 1 if any(row['status'] != 'completed' for row in results) else 0


if __name__ == '__main__':
    sys.exit(main())
