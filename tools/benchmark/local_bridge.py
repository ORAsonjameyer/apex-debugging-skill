#!/usr/bin/env python3
"""Loopback bridge for a fixed Codex snapshot benchmark configuration."""
import argparse
import hmac
import json
import secrets
import subprocess
import sys
import threading
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlsplit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--models', nargs='+', required=True)
    parser.add_argument('--output-root', type=Path, required=True)
    parser.add_argument('--apex-origin', required=True, help='Exact APEX origin, e.g. http://localhost:7002')
    parser.add_argument('--port', type=int, default=8765)
    parser.add_argument('--timeout', type=int, default=300)
    args = parser.parse_args()
    cases = args.cases.resolve(strict=True)
    entries = json.loads(cases.read_text(encoding='utf-8'))
    if not isinstance(entries, list) or len(entries) != 3:
        parser.error('exactly three case snapshots are required')
    origin = urlsplit(args.apex_origin)
    if origin.scheme not in ('http', 'https') or not origin.netloc or origin.path not in ('', '/') or origin.query or origin.fragment or origin.username:
        parser.error('apex-origin must be an exact HTTP(S) origin without path')
    allowed_origin = f'{origin.scheme}://{origin.netloc}'
    root = args.output_root.resolve()
    root.mkdir(parents=True, exist_ok=True)
    token = secrets.token_urlsafe(24)
    state = {'process': None, 'output': None}
    lock = threading.Lock()
    runner = Path(__file__).with_name('run_codex_benchmark.py').resolve()

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *unused):
            pass

        def headers_common(self, status):
            self.send_response(status)
            self.send_header('Access-Control-Allow-Origin', allowed_origin)
            self.send_header('Vary', 'Origin')
            self.send_header('Access-Control-Allow-Headers', 'X-Benchmark-Token, Content-Type')
            self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
            self.send_header('Access-Control-Allow-Private-Network', 'true')
            self.send_header('Cache-Control', 'no-store')
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()

        def send_json(self, status, data):
            self.headers_common(status)
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode())

        def permitted(self):
            return (self.headers.get('Origin') == allowed_origin and
                    hmac.compare_digest(self.headers.get('X-Benchmark-Token', ''), token))

        def do_OPTIONS(self):
            if self.headers.get('Origin') != allowed_origin:
                return self.send_json(403, {'error': 'Origin not allowed'})
            self.headers_common(204)

        def do_POST(self):
            if not self.permitted():
                return self.send_json(403, {'error': 'Origin or token invalid'})
            if self.path != '/start':
                return self.send_json(404, {'error': 'Unknown endpoint'})
            with lock:
                if state['process'] is not None and state['process'].poll() is None:
                    return self.send_json(409, {'error': 'A run is already active'})
                name = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
                output = root / name
                cmd = [sys.executable, str(runner), '--cases', str(cases), '--models', *args.models,
                       '--timeout', str(args.timeout), '--output', str(output)]
                try:
                    state['process'] = subprocess.Popen(cmd, stdin=subprocess.DEVNULL,
                                                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                    state['output'] = output
                except OSError:
                    return self.send_json(500, {'error': 'Could not start runner'})
            self.send_json(202, {'status': 'started'})

        def do_GET(self):
            if not self.permitted():
                return self.send_json(403, {'error': 'Origin or token invalid'})
            if self.path != '/status':
                return self.send_json(404, {'error': 'Unknown endpoint'})
            with lock:
                process, output = state['process'], state['output']
                if process is None:
                    return self.send_json(200, {'status': 'idle', 'results': []})
                result_file = output / 'results.json'
                rows = json.loads(result_file.read_text(encoding='utf-8')) if result_file.exists() else []
                result = process.poll()
                if result is None:
                    status = 'running'
                elif result == 0:
                    status = 'completed'
                else:
                    status = 'execution_error'
                self.send_json(200, {'status': status, 'results': rows})

    server = ThreadingHTTPServer(('127.0.0.1', args.port), Handler)
    print(f'Lokale Benchmark-Brücke: http://127.0.0.1:{args.port}', flush=True)
    print(f'APEX-Origin: {allowed_origin}', flush=True)
    print(f'Einmaliger Sitzungsschlüssel: {token}', flush=True)
    print('Nur freigegebene Fälle und Modell-IDs aus dem Startbefehl werden ausgeführt.', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == '__main__':
    main()
