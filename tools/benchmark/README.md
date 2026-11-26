# Automatische APEX-Fallanalysen zeitlich vergleichen

## Vorprüfung für einen Live-Lauf

Der Snapshot-Runner unten führt **keine Live-Browser-Läufe** durch. Für einen künftigen Live-Runner muss jede eigenständige Modellsitzung den bereits geöffneten VS-Code-Browser über Computer Use erreichen können. Die Vorprüfung startet einen lesenden Modelllauf und prüft den tatsächlichen Werkzeugaufruf, ohne die Browserausgabe oder Sitzungs-URLs zu speichern:

```sh
python3 tools/benchmark/check_live_access.py --model gpt-5.6-luna
```

Bei `blocked` darf kein Live-Benchmark als ausgeführt oder erfolgreich dargestellt werden. Ein separater Codex-Prozess kann eine eigene Computer-Use-Freigabe benötigen; der Zugriff des aktuellen Chats wird nicht automatisch übernommen. Die Vorprüfung allein ist noch kein vollständiger Live-Benchmark: Orchestrierung, Auswertung, APEX-Anbindung und Speicherung in `AIBENCH_RUNS` fehlen weiterhin.

Der Runner startet für jeden Fall, jedes angegebene Codex-Modell und jede Wiederholung eine frische, nicht persistierte Codex-CLI-Sitzung und misst die verstrichene Zeit. Er verwendet ausschließlich bereitgestellte, redigierte Evidenz-Snapshots. Er nutzt keine Live-Browser-Sitzung, keine MCP-Verbindung und keine Skills; er misst damit die Analyse vorgegebener Hinweise, nicht die Dauer eines vollständigen Live-Debuggings. Modell-ID, Fall und Wiederholung stehen in der Ergebnisdatei; Antworten müssen fachlich geprüft werden. Ein abgeschlossener Prozess bedeutet keine korrekte Diagnose.

1. Für die drei realen Use Cases jeweils die aktuell tatsächlich sichtbaren Symptome und relevanten redigierten Hinweise zusammentragen. Keine Lösungsnamen, Passwörter, Session-IDs oder anderen Geheimnisse in die Fallbeschreibung schreiben. Die Fälle müssen reproduzierbar und für alle Modelle identisch sein. Der dritte Fall muss zunächst konkret vorbereitet und geprüft werden; dessen Ursache ist nicht automatisch bekannt.
2. Eine JSON-Datei mit drei Einträgen anlegen, z. B. `[{"id":"case-1","title":"MLE-Fehler","evidence":"..."}]`. `id`, `title` und `evidence` sind Pflichtfelder. Keine Antwortschlüssel in die Datei aufnehmen.
3. Tatsächlich für die eigene Codex-Umgebung freigeschaltete Modell-IDs einsetzen. Verfügbarkeit und Anbieter sind nicht durch den Runner garantiert. Läufe können Zeit und Kosten verursachen.

```sh
python3 tools/benchmark/run_codex_benchmark.py \
  --cases /pfad/zu/redigierte-faelle.json \
  --models MODEL_ID_1 MODEL_ID_2 \
  --repetitions 3 --timeout 300 \
  --output .logs/benchmark-lauf-01
```

Das Ausgabeverzeichnis muss neu sein. Es enthält `run.json` (einschließlich SHA-256 der Fall-Datei), `results.csv`, `results.json`, Antworten und gegebenenfalls Diagnosen. Inhalte können vertrauliche Informationen enthalten und sollen lokal bleiben. Die CLI-Ausführungszeit umfasst Start, ggf. Warteschlange und Antwort; fehlgeschlagene Läufe und Timeouts werden separat gekennzeichnet. Keine Token- oder Kostenmessung wird behauptet. Der Runner schreibt keine Daten in die APEX-App. Für Live-Debugging wären isolierte zurücksetzbare Umgebungen, gleiche Werkzeuge/Skill-Versionen, ein sicherer Ausführungsrahmen und ein eigener Evaluator notwendig.

Während eines Laufs zeigen `results.json` und `results.csv` den aktiven Fall mit Status `running`; nach Abschluss stehen dort Dauer und Endstatus. Die Dateien werden beim Aktualisieren atomar ersetzt. Bei einem unerwarteten Abbruch kann der letzte Eintrag `running` stehen bleiben; das ist kein Nachweis für einen noch aktiven Prozess.

## Start aus APEX

Die lokale Brücke stellt ausschließlich den konfigurierten Runner auf `127.0.0.1:8765` bereit. Sie akzeptiert Anfragen nur vom angegebenen APEX-Origin und mit dem beim Start erzeugten Sitzungsschlüssel. Sie nimmt keine Befehle, Modelllisten oder Pfade aus dem Browser entgegen. Für jeden Lauf muss die Brücke eingeschaltet bleiben.

```sh
python3 tools/benchmark/local_bridge.py \
  --cases /pfad/zu/redigierte-faelle.json \
  --models gpt-6.1-sol gpt-6.1-terra \
  --apex-origin http://localhost:7002 \
  --output-root .logs/benchmark-runs
```

Genau drei Fälle sind für die Brücke erforderlich. Den einmaligen Schlüssel aus dem Terminal auf der Benchmark-Seite eingeben und den Button drücken. Modelle werden nacheinander abgearbeitet, jeweils alle drei Fälle pro Modell. Die Tabelle zeigt Warteschlange, aktiven Fall, technischen Abschluss oder Fehler und gemessene Zeit. Dies ist keine Bewertung der Diagnosequalität. Die Datei mit den Antworten bleibt lokal. `Ctrl+C` beendet die Brücke; ein bereits gestarteter Runner kann weiterlaufen. Browser-Sicherheitsrichtlinien, HTTPS/Mixed Content, Private-Network-Access und die Content-Security-Policy der konkreten APEX-Instanz können die Verbindung zu `127.0.0.1` verhindern; vor Einsatz live testen.

## Playwright-Live-Runner

`run_live_playwright_benchmark.sh` steuert die sichtbare APEX-Benchmark-Seite über Playwright. Der Runner hängt ausschließlich an einen bereits laufenden Browser mit authentifizierter APEX-Session an: entweder über einen vorhandenen CDP-Endpunkt oder eine bereits installierte Playwright-Browser-Extension. Er startet keinen neuen Login, öffnet keine DevTools, untersucht keine lokalen APEX-Quellen und führt keine Retries oder Änderungen aus.

Nach dem Attach öffnet er die automatische Benchmark-Seite, drückt einmal `Benchmark starten`, wartet auf die Ergebnistabelle und beendet sich erst, wenn sie genau drei terminale Use-Case-Zeilen je sichtbarem Modell enthält. Fehlerzeilen werden als Ergebnis übernommen und nicht erneut ausgeführt. Snapshots werden unter `output/playwright/live-benchmark/` abgelegt.

Beispiele:

```sh
tools/benchmark/run_live_playwright_benchmark.sh \
  --cdp-endpoint "$PLAYWRIGHT_CDP_ENDPOINT"

tools/benchmark/run_live_playwright_benchmark.sh \
  --extension chrome
```

Ohne CDP-Endpunkt oder installierte Extension bricht der Runner fail-closed ab, statt eine neue, nicht authentifizierte Session zu öffnen.
