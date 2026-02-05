# Careti Agent Benchmark

[English](README.en.md) | [한국어](README.ko.md) | [日本語](README.ja.md) | [中文](README.zh.md) | [Français](README.fr.md) | [Deutsch](README.de.md) | [Русский](README.ru.md)

---

**Système de benchmark mesurant les performances réelles des agents de codage IA**

## Résultats en direct

**[Voir les résultats du benchmark](https://careti.ai/fr/benchmark)**

## Démarrage rapide

```bash
# Cloner le dépôt
git clone https://github.com/caretive-ai/careti-benchmark.git
cd careti-benchmark

# Vérifier l'intégrité des données
python3 scripts/verify-data.py

# Exemple d'utilisation
python3 scripts/example-usage.py
```

## Pourquoi ce benchmark ?

### Limites des benchmarks existants

| Benchmark | Limite |
|-----------|--------|
| **HumanEval** | Mesure uniquement la génération de fonctions simples, déconnecté du développement réel |
| **SWE-bench** | Mesure la résolution de problèmes GitHub, mais ne reflète pas l'utilisation d'outils par l'agent |
| **MBPP** | Problèmes Python simples, pas de support pour les tâches multi-fichiers complexes |

**Problème central** : Les benchmarks existants ne mesurent que la "capacité de génération de code". Mais les vrais agents de codage IA (Cline, Cursor, Careti, etc.) **utilisent des outils, voient les erreurs et les corrigent, et font plusieurs tentatives**.

### Ce que ce benchmark mesure

```
Traditionnel : Problème → Modèle → Code → Note (1 fois)
Careti :       Problème → Agent → Code → Test → [Feedback d'erreur] → Nouvelle tentative → ... → Résultat final
```

## Derniers résultats (Hard Suite 100)

| Rang | Modèle | 1ère réussite | Réussite finale | Tentatives moy. | Coût |
|------|--------|---------------|-----------------|-----------------|------|
| #1 | Gemini 2.5 Flash | 70-92% | **98%** | 1.11-1.44 | $0.05-0.13 |
| #2 | GLM-4.7 | 89-92% | **97-98%** | 1.11-1.15 | $0.18 |
| #3 | Gemini 3 Pro (Preview) | 66-67% | **92-93%** | 1.53-1.57 | $0.60 |
| #4 | Solar Pro2 | 61-64% | **81-86%** | 1.82-1.87 | $0.75-0.87 |
| #5 | Solar Pro3 | 70% | **75%** | 1.71 | $1.35 |
| #6 | HyperCLOVA X | 1-2% | **1-2%** | 3.03-3.06 | $0.22-0.31 |

## Métriques clés

| Métrique | Signification | Pourquoi c'est important ? |
|----------|---------------|---------------------------|
| **Taux de réussite 1ère tentative** | Taux de succès au premier essai | "L'intuition" de l'agent - détermine le temps d'attente utilisateur |
| **Taux de réussite final** | Taux de succès incluant les nouvelles tentatives | "La capacité de résolution" de l'agent |
| **Tentatives moyennes** | Moyenne d'essais par problème | Indicateur d'efficacité |
| **Coût** | Coût total API | Faisabilité économique |

## Conditions de terminaison

| Condition | Description |
|-----------|-------------|
| `success` | Test réussi |
| `max_attempts` | Nombre max de tentatives atteint (5) |
| `timeout` | Délai dépassé (300s) |
| `oscillation` | Motif d'oscillation A↔B détecté |
| `same_error` | Même erreur répétée 3 fois |

## Données brutes

Le répertoire `results/` contient les données complètes du benchmark au format JSON.

### Structure des données

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

### Consultation des problèmes originaux

Les problèmes Hard Suite sont inclus dans `problems/hard-suite.json` :

```python
import json
import urllib.request

# Télécharger les problèmes
url = "https://raw.githubusercontent.com/caretive-ai/careti-benchmark/main/problems/hard-suite.json"
problems = json.loads(urllib.request.urlopen(url).read())

# Trouver un problème par ID
problem = next(p for p in problems if p["id"] == "h01-longest-substring")
print(problem["prompt"])
print(problem["test_code"])
```

## Structure des fichiers

```
problems/
  hard-suite.json       # 100 problèmes avec prompts et code de test

results/2026-02-hard-suite/
  results.json          # 2100 résultats de tests individuels
  summary.json          # Statistiques agrégées par modèle

scripts/
  verify-data.py        # Vérification de l'intégrité des données
  example-usage.py      # Scripts d'analyse exemples
```

## Licence

MIT

---

**Made by [Caretive](https://caretive.ai)** - Développeurs de l'agent de codage IA Careti
