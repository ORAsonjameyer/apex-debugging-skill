#!/usr/bin/env python3
"""Fail-closed probe: can a separate Codex run see the existing VS Code APEX browser?"""
import argparse
import json
import subprocess
import sys
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model', required=True, help='Codex model ID to test')
    parser.add_argument('--codex', default='codex')
    parser.add_argument('--timeout', type=int, default=120)
    args = parser.parse_args()
    if args.timeout < 1:
        parser.error('timeout must be positive')
    prompt = (
        'Read-only capability check. Use the computer-use tool to inspect the existing '
        'VS Code app com.microsoft.VSCode. Do not click, type, navigate, change any '
        'settings, run SQL or call any other service. Report whether the opened VS Code '
        'window contains the APEX browser. Never quote URLs, session IDs or credentials.'
    )
    cmd = [args.codex, 'exec', '--json', '--model', args.model, '--sandbox', 'read-only',
           '--skip-git-repo-check', '--ephemeral',
           '-c', 'mcp_servers.sqlcl.enabled=false', '-c', 'mcp_servers.github.enabled=false',
           '-c', 'mcp_servers.node_repl.enabled=false', '-c', 'mcp_servers.codex_app.enabled=false', '-']
    start = time.monotonic()
    try:
        proc = subprocess.run(cmd, input=prompt, text=True, capture_output=True, timeout=args.timeout)
    except (subprocess.TimeoutExpired, OSError) as exc:
        print(json.dumps({'status': 'blocked', 'reason': type(exc).__name__,
                          'elapsed_seconds': round(time.monotonic()-start, 2)}))
        return 2
    success, denied, saw_apex = False, False, False
    for line in proc.stdout.splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        item = event.get('item') or {}
        if event.get('type') != 'item.completed' or item.get('type') != 'mcp_tool_call' or item.get('server') != 'cua_repl':
            continue
        arguments = item.get('arguments') or {}
        code = arguments.get('code', '')
        content = (item.get('result') or {}).get('content') or []
        observed = '\n'.join(str(x.get('text', '')) for x in content if isinstance(x, dict))
        if 'cua.getApp' not in code or 'com.microsoft.VSCode' not in code:
            continue
        if item.get('status') == 'completed' and 'Window:' in observed:
            success = True
            saw_apex = 'APEX' in observed.upper() or 'localhost:7002' in observed
        elif 'not approved' in observed.lower() or 'not authorized' in observed.lower():
            denied = True
    if proc.returncode != 0:
        status, reason = 'blocked', f'Codex process failed with exit code {proc.returncode}.'
    elif success and saw_apex:
        status, reason = 'ready', 'VS Code with APEX was visible in the separate model session.'
    elif denied:
        status, reason = 'blocked', 'Computer Use was not approved to use Code in the separate model session.'
    else:
        status, reason = 'blocked', 'VS Code with APEX was not independently verified.'
    print(json.dumps({'status': status, 'reason': reason, 'model': args.model,
                      'elapsed_seconds': round(time.monotonic()-start, 2)}, ensure_ascii=False))
    return 0 if status == 'ready' else 2


if __name__ == '__main__':
    sys.exit(main())
