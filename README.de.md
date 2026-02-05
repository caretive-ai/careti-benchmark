# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Benchmark-System zur Messung der realen Leistung von KI-Coding-Agenten**

## Live-Ergebnisse

**[Benchmark-Ergebnisse ansehen](https://careti.ai/de/benchmark)**

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
| #1 | Gemini 2.5 Flash | 62-67% | **98%** | 1.36-1.44 | $0.09-0.13 |
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
  "problem_id": "he000-has_close_elements",
  "model": "Gemini 2.5 Flash",
  "success": true,
  "attempts": 1,
  "first_attempt_success": true,
  "total_time_ms": 5348,
  "cost_usd": 0.00018,
  "input_tokens": 161,
  "output_tokens": 264,
  "prompt_mode": "careti",
  "termination_reason": "success",
  "attempt_history": [...]
}
```

### Originalprobleme nachschlagen

HumanEval-Probleme können aus dem Hugging Face Dataset abgerufen werden:

```python
from datasets import load_dataset

ds = load_dataset("openai/openai_humaneval")
problem = ds["test"][0]  # he000 → Problem 0
print(problem["prompt"])
```

**Hugging Face**: [openai/openai_humaneval](https://huggingface.co/datasets/openai/openai_humaneval)

## Lizenz

MIT

---

**Made by [Caretive](https://caretive.ai)** - Entwickler des KI-Coding-Agenten Careti
