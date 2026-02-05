# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Benchmark-System zur Messung der realen Leistung von KI-Coding-Agenten**

## Live-Ergebnisse

**[Benchmark-Ergebnisse ansehen](https://careti.ai/de/benchmark)**

## Schnellstart

```bash
# Repository klonen
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# Datenintegrität prüfen
python3 scripts/verify-data.py

# Beispielverwendung
python3 scripts/example-usage.py
```

## Warum dieser Benchmark?

### Grenzen bestehender Benchmarks

| Benchmark | Einschränkung |
|-----------|---------------|
| **HumanEval** | Misst nur Einzelfunktionsgenerierung, von realer Entwicklung entkoppelt |
| **SWE-bench** | Misst GitHub-Issue-Lösung, spiegelt aber nicht die Tool-Nutzung des Agenten wider |
| **MBPP** | Einfache Python-Probleme, keine Unterstützung für komplexe Multi-Datei-Aufgaben |

**Kernproblem**: Bestehende Benchmarks messen nur die "Codegenerierungsfähigkeit". Aber echte KI-Coding-Agenten (Cline, Cursor, Careti usw.) **nutzen Tools, sehen Fehler und beheben sie, und machen mehrere Versuche**.

### Was dieser Benchmark misst

```
Traditionell: Problem → Modell → Code → Bewertung (1 Mal)
Careti:       Problem → Agent → Code → Test → [Fehler-Feedback] → Erneut versuchen → ... → Endergebnis
```

## Neueste Ergebnisse (Hard Suite 100)

| Rang | Modell | 1. Versuch | Endgültig | Ø Versuche | Kosten |
|------|--------|------------|-----------|------------|--------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## Wichtige Metriken

| Metrik | Bedeutung | Warum wichtig? |
|--------|-----------|----------------|
| **Erfolgsrate 1. Versuch** | Erfolgsrate beim ersten Versuch | "Intuition" des Agenten - bestimmt Benutzerwartezeit |
| **Endgültige Erfolgsrate** | Erfolgsrate einschließlich Wiederholungen | "Problemlösungsfähigkeit" des Agenten |
| **Durchschnittliche Versuche** | Mittelwert der Versuche pro Problem | Effizienzindikator |
| **Kosten** | Gesamte API-Kosten | Wirtschaftliche Machbarkeit |

## Beendigungsbedingungen

| Bedingung | Beschreibung |
|-----------|--------------|
| `success` | Test bestanden |
| `max_attempts` | Maximale Versuche erreicht (5) |
| `timeout` | Zeitlimit überschritten (300s) |
| `oscillation` | A↔B-Oszillationsmuster erkannt |
| `same_error` | Gleicher Fehler 3 Mal wiederholt |

## Rohdaten

Das Verzeichnis `results/` enthält vollständige Benchmark-Daten im JSON-Format.

### Datenstruktur

```json
{
  "problem_id": "h01-longest-substring",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 2,
  "first_attempt_success": false,
  "total_time_ms": 9599,
  "cost_usd": 0.00094,
  "input_tokens": 4330,
  "output_tokens": 484,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [
    {
      "attempt": 1,
      "success": false,
      "latency_ms": 6229,
      "error": "SyntaxError: invalid syntax"
    },
    {
      "attempt": 2,
      "success": true,
      "latency_ms": 3370
    }
  ]
}
```

### Originalprobleme nachschlagen

Hard Suite Probleme sind in `problems/hard-suite.json` enthalten:

```python
import json
import urllib.request

# Probleme herunterladen
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# Problem nach ID finden
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## Dateistruktur

```
problems/
  hard-suite.json       # 100 Probleme mit Prompts und Testcode

results/2026-02-hard-suite/
  results.json          # 2100 individuelle Testergebnisse
  summary.json          # Aggregierte Statistiken pro Modell

scripts/
  verify-data.py        # Datenintegritätsprüfung
  example-usage.py      # Beispiel-Analyseskripte
```

## Lizenz

MIT

---

**Made by [Caretive](https://caretive.ai)** - Entwickler des KI-Coding-Agenten Careti
